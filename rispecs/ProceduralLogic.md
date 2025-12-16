# WillWrite Procedural Logic

**Status**: ✅ IMPLEMENTED

This document provides a detailed, step-by-step procedural description of the `WillWrite` application's logic. It serves as a bridge between the high-level specifications and the actual implementation in `storytelling/graph.py` and related modules, detailing the "glue" code that connects the various stages and LLM calls.

## Main Application Flow

**Objective:** To execute the end-to-end story generation pipeline based on user configuration.

**Procedure:**

1.  **Initialize:**
    *   Start a timer to measure total generation time.
    *   Parse all configuration parameters as defined in `Configuration.md`.
    *   Initialize the logging system according to the `Logging_And_Traceability_Specification.md`, creating the unique session directory.
    *   For each model parameter in the configuration, parse the provider URI string according to `LLM_Provider_Specification.md` to initialize and configure the corresponding LLM client. Store these clients for use in the application.
    *   Execute the **Initialize Knowledge Base** procedure.

2.  **Load and Prepare Prompt:**
    *   Read the content of the file specified by the `-Prompt` parameter.
    *   **Conditional Logic:** If the `-TranslatePrompt` parameter is set, call the **Translate Prompt** procedure.

3.  **Generate Story Foundation:**
    *   Execute the **Generate Outline** procedure, which returns the final `Outline`, `StoryElements`, and `BaseContext`.

4.  **Generate Chapters:**
    *   Execute the **Generate All Chapters** procedure, which returns a list of all generated chapter texts.

5.  **Post-Process Novel:**
    *   Initialize an empty string for the final `StoryBodyText`.
    *   Initialize a dictionary `StoryInfoJSON` and populate it with the `Outline`, `StoryElements`, and `BaseContext`.
    *   **Conditional Logic:** If `-EnableFinalEditPass` is true, execute the **Final Edit Pass** procedure.
    *   **Conditional Logic:** If `-NoScrubChapters` is false, execute the **Scrub Novel** procedure.
    *   **Conditional Logic:** If `-Translate` is set, execute the **Translate Novel** procedure.
    *   Concatenate all processed chapters into the `StoryBodyText` variable, separated by newlines.

6.  **Finalize and Save:**
    *   Execute the **Generate Story Info** procedure to get the `Title`, `Summary`, and `Tags`.
    *   Update the `StoryInfoJSON` dictionary with this information.
    *   Calculate total word count and generation time statistics.
    *   Format a `StatsString` containing all statistics and configuration details.
    *   Determine the output file name based on the `-Output` parameter or the generated `Title`.
    *   Save the final story to a `.md` file, combining the `StatsString`, `Title`, `StoryBodyText`, and `Outline`.
    *   Save the `StoryInfoJSON` dictionary to a `.json` file.

---
*This document will be expanded with detailed procedures for each sub-process.*

---

## Sub-Procedures

### Initialize Knowledge Base

1.  **Conditional Logic:** If `-KnowledgeBasePath` is provided:
    a. Use a `DirectoryLoader` to load all `.md` files from the specified path.
    b. Use a `RecursiveCharacterTextSplitter` to split the loaded documents into chunks.
    c. Use the specified `-EmbeddingModel` to create vector embeddings for each chunk.
    d. Store these embeddings in an in-memory vector store (e.g., FAISS or Chroma).
    e. Create a `Retriever` object from the vector store.
    f. Store this `Retriever` in the application's state for later use.

### Generate Outline

**Implementation**: `generate_initial_outline_node()` in `storytelling/graph.py`

1.  Call the LLM with the `STORY_ELEMENTS_PROMPT` to manifest the foundational story elements.
2.  Initialize an empty string for `RetrievedContext`.
3.  **Conditional Logic:** If a `Retriever` is available and `outline_rag_enabled` is true:
    a. Call `retrieve_outline_context()` from `storytelling/rag.py` to find document chunks relevant to the user's prompt and story elements.
    b. Uses configuration parameters: `outline_context_max_tokens`, `outline_rag_top_k`, and `outline_rag_similarity_threshold`.
    c. Store the formatted context in `RetrievedContext`.
    d. Inject `RetrievedContext` into the `INITIAL_OUTLINE_PROMPT`.
4.  Call the LLM with the `INITIAL_OUTLINE_PROMPT` to create the initial `Outline`.
5.  **Loop** for a number of iterations between `outline_min_revisions` and `outline_max_revisions`:
    a. **Conditional Logic:** If `RetrievedContext` is not empty, inject it into the `CRITIC_OUTLINE_PROMPT`.
    b. Call the LLM with the `CRITIC_OUTLINE_PROMPT` to receive structural enhancement opportunities.
    c. Call the LLM with the `OUTLINE_COMPLETE_PROMPT` and its corresponding `DataSchema` to evaluate completion.
    d. **Conditional Logic:** If the outline is complete and the minimum revisions have been met, **break** the loop.
    e. **Conditional Logic:** If `RetrievedContext` is not empty, inject it into the `OUTLINE_REVISION_PROMPT`.
    f. Call the LLM with the `OUTLINE_REVISION_PROMPT`, passing the current `Outline` and enhancement opportunities, to advance the `Outline`.
6.  Return the final `Outline`, `StoryElements`, and `BaseContext`.

### Generate All Chapters

1.  Call the LLM with the `CHAPTER_COUNT_PROMPT` and its `DataSchema` to get the `NumChapters`.
2.  Initialize an empty list to store `ChapterOutlines`.
3.  **Conditional Logic:** If `-ExpandOutline` is true:
    *   **Loop** from 1 to `NumChapters`:
        *   Call the LLM with the `CHAPTER_OUTLINE_PROMPT` to generate a detailed outline for the current chapter.
        *   Append the result to the `ChapterOutlines` list.
4.  Initialize an empty list to store the final `Chapters`.
5.  **Loop** from 1 to `NumChapters`:
    a. Execute the **Generate Single Chapter** procedure for the current chapter number.
    b. Prepend a markdown header (e.g., `### Chapter X`) to the returned chapter text.
    c. Append the formatted chapter to the `Chapters` list.
    d. **Error Handling:** Implement a retry loop (e.g., 3 attempts) in case of failure. If all retries fail, append a placeholder failure message and continue.
6.  Return the `Chapters` list.

### Generate Single Chapter

1.  Extract the specific outline for the current chapter.
2.  **Conditional Logic:** If previous chapters exist, generate a summary of the last chapter to provide context.
3.  Initialize an empty string for `RetrievedContext`.
4.  **Conditional Logic:** If a `Retriever` is available in the application state:
    a. Use the `Retriever` to find document chunks relevant to the current chapter's outline.
    b. Store this in `RetrievedContext`.
    c. Inject `RetrievedContext` into the chapter generation prompts.
5.  **Conditional Logic:** Based on the `-SceneGenerationPipeline` flag:
    *   **If true (Scene-by-Scene):**
        i. Call LLM with `CHAPTER_TO_SCENES` prompt.
        ii. Call LLM with `SCENES_TO_JSON` prompt and its `DataSchema` to get a list of scene outlines.
        iii. Initialize an empty string for the `RoughChapter`.
        iv. **Loop** through each scene outline in the list:
            - Call LLM with `SCENE_OUTLINE_TO_SCENE` prompt to generate the full scene text.
            - Append the scene text to the `RoughChapter`.
        v. The `RoughChapter` becomes the initial version of the chapter to be refined.
    *   **If false (Staged Generation):**
        i. **Stage 1 (Plot):** Call LLM with `CHAPTER_GENERATION_STAGE1` prompt.
        ii. **Stage 2 (Character Dev):** Call LLM with `CHAPTER_GENERATION_STAGE2` prompt, passing the output of Stage 1.
        iii. **Stage 3 (Dialogue):** Call LLM with `CHAPTER_GENERATION_STAGE3` prompt, passing the output of Stage 2. The result is the initial version of the chapter.
6.  **Conditional Logic:** If `-NoChapterRevision` is false, enter the refinement loop:
    a. **Loop** for a number of iterations between `-ChapterMinRevisions` and `-ChapterMaxRevisions`:
        i. **Conditional Logic:** If `RetrievedContext` is not empty, inject it into the `CRITIC_CHAPTER_PROMPT`.
        ii. Call LLM with `CRITIC_CHAPTER_PROMPT` to get `Feedback`.
        iii. Call LLM with `CHAPTER_COMPLETE_PROMPT` and its `DataSchema` to check for completion.
        iv. **Conditional Logic:** If the chapter is complete and minimum revisions are met, **break** the loop.
        v. **Conditional Logic:** If `RetrievedContext` is not empty, inject it into the `CHAPTER_REVISION` prompt.
        vi. Call LLM with `CHAPTER_REVISION` prompt to update the chapter text.
7.  Return the final chapter text.
