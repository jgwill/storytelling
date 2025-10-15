# WillWrite Application Logic Overview

This document describes the high-level logical workflow of the `WillWrite` application for generating a story. It is not tied to any specific implementation details. For the exact text of the prompts mentioned, see `Prompts.md`.

## 1. Initialization and Configuration

The process begins by configuring the story generation pipeline. This involves setting various parameters that control the behavior of the application, such as:

*   The models to be used for different tasks (e.g., outline generation, chapter writing, revision).
*   The quality thresholds and revision limits for the outline and chapters.
*   Optional features to be enabled or disabled, such as expanding the outline, performing a final edit pass, scrubbing the chapters, and translating the story.

## 2. Outline Generation and Refinement

Once the application is configured, it generates the story outline. This is a multi-step process:

1.  **Prompt Analysis**: The initial user prompt is analyzed to extract any important context or constraints that are not part of the story itself (e.g., desired chapter length, overall tone). This is done using the `GET_IMPORTANT_BASE_PROMPT_INFO` prompt.
2.  **Story Element Generation**: The core elements of the story are generated, including characters, setting, plot, theme, and conflict.
3.  **Initial Outline Generation**: An initial outline is generated based on the story elements and the user's prompt, using the `INITIAL_OUTLINE_PROMPT`.
4.  **Outline Refinement Loop**: The outline enters a feedback loop:
    *   The `CRITIC_OUTLINE_PROMPT` is used to get feedback on the current outline.
    *   The `OUTLINE_COMPLETE_PROMPT` is used to check if the outline meets the quality standards.
    *   If the outline is not complete, the `OUTLINE_REVISION_PROMPT` is used to revise it based on the feedback.
    *   This loop continues until the outline is complete or the maximum number of revisions is reached.

## 3. Chapter Generation

With a finalized outline, the application proceeds to generate the chapters of the story. This is an iterative process that can be broken down as follows:

1.  **Chapter Detection**: The number of chapters in the story is determined from the outline using the `CHAPTER_COUNT_PROMPT`.
2.  **Chapter Outline Expansion (Optional)**: If enabled, a more detailed outline is generated for each chapter using the `CHAPTER_OUTLINE_PROMPT`.
3.  **Iterative Chapter Writing**: The application iterates through each chapter and generates the content. This is a multi-stage process for each chapter:
    *   **Plot Generation**: The initial plot of the chapter is written using the `CHAPTER_GENERATION_STAGE1` prompt.
    *   **Character Development**: Character development is added to the plot using the `CHAPTER_GENERATION_STAGE2` prompt.
    *   **Dialogue Addition**: Dialogue is added to the chapter using the `CHAPTER_GENERATION_STAGE3` prompt.
    *   **Revision Loop**: The generated chapter is critiqued and revised:
        *   The `CRITIC_CHAPTER_PROMPT` is used to get feedback on the chapter.
        *   The `CHAPTER_COMPLETE_PROMPT` is used to check if the chapter meets the quality standards.
        *   If the chapter is not complete, the `CHAPTER_REVISION` prompt is used to revise it based on the feedback.
        *   This loop continues until the chapter is complete or the maximum number of revisions is reached.

## 4. Post-Processing

After all the chapters have been generated, the story goes through a series of optional post-processing steps:

1.  **Final Edit Pass (Optional)**: The entire novel is edited for consistency and flow using the `CHAPTER_EDIT_PROMPT`.
2.  **Scrubbing (Optional)**: The generated chapters are cleaned to remove any leftover artifacts from the generation process, using the `CHAPTER_SCRUB_PROMPT`.
3.  **Translation (Optional)**: The entire novel is translated into a specified language using the `CHAPTER_TRANSLATE_PROMPT`.

## 5. Final Output

The final step is to generate the output files:

1.  **Story Info Generation**: The title, summary, and tags for the story are generated using the `STATS_PROMPT`.
2.  **File Creation**:
    *   A Markdown file is created containing the final story, along with statistics and the story outline.
    *   A JSON file is created containing all the information about the story, including the outline, story elements, and generated chapters.