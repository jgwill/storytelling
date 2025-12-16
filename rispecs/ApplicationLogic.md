# WillWrite Application Logic Overview

**Status**: ✅ IMPLEMENTED

**Structural Tension**
- Desired Outcome: A clear, implementation-aligned description of the story generation workflow that empowers developers to understand and extend the creative pipeline.
- Current Reality: The core workflow is implemented in LangGraph nodes in `storytelling/graph.py`. However, several specified features including prompt analysis, critique/revision loops, and iterative refinement are defined but not yet integrated into the workflow.
- Natural Progression: Document the advancing patterns currently implemented while identifying opportunities for enhancement through critique loops and iterative refinement mechanisms.

This document describes the high-level logical workflow of the Storytelling package for generating a story, aligned with the LangGraph implementation in `storytelling/graph.py`. For the exact text of the prompts mentioned, see `Prompts.md`.

## ⚠️ Implementation Status Note

**Currently Implemented**: The core single-pass workflow (story elements → outline → chapters → final story) is fully operational.

**Specified but Not Yet Implemented**: Several enhancement features exist in specifications and prompts but are not yet integrated into the workflow:
- Prompt Analysis step using `GET_IMPORTANT_BASE_PROMPT_INFO`
- Outline critique and revision loop using `CRITIC_OUTLINE_PROMPT` and `OUTLINE_REVISION_PROMPT`
- Chapter critique and revision loop using `CRITIC_CHAPTER_PROMPT` and `CHAPTER_REVISION`
- Configuration parameters for revision counts (`outline_min_revisions`, `outline_max_revisions`, `chapter_min_revisions`, `chapter_max_revisions`) are defined but not utilized

**Path Forward**: These iterative refinement features represent advancing patterns that would enhance story quality through feedback loops. Implementation would require adding critique/revision nodes to the LangGraph workflow.

## 1. Initialization and Configuration

The process begins by configuring the story generation pipeline. This involves setting various parameters that control the behavior of the application, such as:

*   The models to be used for different tasks (e.g., outline generation, chapter writing, revision).
*   The quality thresholds and revision limits for the outline and chapters.
*   Optional features to be enabled or disabled, such as expanding the outline, performing a final edit pass, scrubbing the chapters, and translating the story.

## 2. Manifesting the Story Foundation

The application establishes the narrative foundation through advancing patterns that transform the user's creative vision into a structured blueprint.

**LangGraph Implementation**: These stages are implemented as nodes in `storytelling/graph.py`

1.  **Story Element Generation** (`generate_story_elements_node`): 
    - Creates the foundational narrative components: characters, setting, plot, theme, and conflict
    - Uses `STORY_ELEMENTS_PROMPT` to manifest the creative building blocks
    - Enables RAG context injection when knowledge base is configured

2.  **Initial Outline Creation** (`generate_initial_outline_node`):
    - Manifests a chapter-by-chapter outline from the story elements
    - Integrates knowledge base context when `outline_rag_enabled` is true
    - Uses `retrieve_outline_context()` to enhance outline with relevant knowledge
    - Applies `INITIAL_OUTLINE_PROMPT` to create the narrative structure

3.  **Outline Refinement Loop**: The outline advances through iterative enhancement:
    - The `CRITIC_OUTLINE_PROMPT` surfaces opportunities to strengthen the narrative
    - The `OUTLINE_COMPLETE_PROMPT` evaluates structural completeness
    - When refinement is needed, `OUTLINE_REVISION_PROMPT` advances the outline toward the desired outcome
    - This advancing pattern continues until quality standards are met or revision limits are reached

## 3. Building the Narrative, Chapter by Chapter

With a complete outline foundation, the application manifests each chapter through advancing patterns that layer complexity and depth.

**LangGraph Implementation**: Chapter generation flows through node transitions orchestrated by `storytelling/graph.py`

1.  **Chapter Count Determination** (`determine_chapter_count_node`):
    - Extracts the total chapter count from the outline using `CHAPTER_COUNT_PROMPT`
    - Establishes the scope for iterative chapter creation

2.  **Chapter Index Progression** (`increment_chapter_index_node`):
    - Advances the chapter index for each iteration
    - Controls the flow through the chapter generation loop

3.  **Scene-by-Scene Chapter Creation** (`generate_single_chapter_scene_by_scene_node`):
    - **Chapter Outline Expansion** (when enabled): Creates detailed scene-level structure using `CHAPTER_OUTLINE_PROMPT`
    - **Layered Content Generation**: Builds chapters through progressive stages:
        - Stage 1 (`CHAPTER_GENERATION_STAGE1`): Manifests the plot foundation
        - Stage 2 (`CHAPTER_GENERATION_STAGE2`): Weaves in character development
        - Stage 3 (`CHAPTER_GENERATION_STAGE3`): Enriches with dialogue
        - Stage 4 (`CHAPTER_GENERATION_STAGE4`): Creates the final integrated form
    - **RAG Context Integration**: Retrieves and injects relevant knowledge for each scene when knowledge base is configured
    - **Advancement Loop**: The chapter evolves through iterative refinement:
        - `CRITIC_CHAPTER_PROMPT` identifies opportunities for narrative enhancement
        - `CHAPTER_COMPLETE_PROMPT` evaluates structural and creative completeness
        - `CHAPTER_REVISION` advances the chapter toward the desired outcome
        - This pattern continues until quality thresholds are met or revision limits are reached

## 4. Polishing and Finalizing

After manifesting all chapters, the application applies optional refinement layers to advance the story toward publication readiness.

1.  **Final Edit Pass** (when enabled): Unifies the entire narrative for consistency and flow using `CHAPTER_EDIT_PROMPT`
2.  **Content Refinement** (when enabled): Removes generation artifacts through `CHAPTER_SCRUB_PROMPT`
3.  **Language Transformation** (when enabled): Manifests the story in the target language using `CHAPTER_TRANSLATE_PROMPT`

## 5. Story Completion and Output

The final stage creates the deliverable artifacts that manifest the complete creative work.

**LangGraph Implementation**: The `generate_final_story_node` orchestrates the completion sequence

1.  **Story Metadata Generation**: 
    - Creates title, summary, tags, and overall rating using `STATS_PROMPT`
    - Establishes the story's identity and discoverability

2.  **Output Manifestation**:
    - **Markdown File**: Contains the complete polished narrative with statistics and outline
    - **JSON File**: Preserves the complete creative history including outline, story elements, and all generated chapters
    - **Session Checkpoint**: Captures the final creative state for future reference or continuation