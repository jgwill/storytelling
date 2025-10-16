# WillWrite Configuration Specification

**Status**: ✅ IMPLEMENTED

This document details all the configuration parameters that control the behavior of the `WillWrite` application. These are typically set via command-line arguments.

## Core Parameters

-   **`-Prompt`**
    -   **Type:** `string`
    -   **Description:** The file path to the initial user prompt for the story.
    -   **Required:** Yes

-   **`-Output`**
    -   **Type:** `string`
    -   **Description:** An optional file path and name for the output files. If not provided, a name is generated automatically based on the story title.
    -   **Default:** `""`

## Model Selection

The application allows for the selection of different models for each stage of the generation process. Each model parameter expects a string formatted as a URI according to the `LLM_Provider_Specification.md` document.

-   **`-InitialOutlineModel`**: Model for the initial outline generation.
-   **`-ChapterOutlineModel`**: Model for the per-chapter outline expansion.
-   **`-ChapterS1Model`**: Model for chapter writing (Stage 1: Plot).
-   **`-ChapterS2Model`**: Model for chapter writing (Stage 2: Character Development).
-   **`-ChapterS3Model`**: Model for chapter writing (Stage 3: Dialogue).
-   **`-ChapterS4Model`**: Model for chapter writing (Stage 4: Final Pass).
-   **`-ChapterRevisionModel`**: Model for revising chapters based on feedback.
-   **`-RevisionModel`**: Model for generating constructive criticism (the "critic").
-   **`-EvalModel`**: Model for evaluating quality and completion (e.g., `IsComplete` JSON).
-   **`-InfoModel`**: Model for generating the final story metadata.
-   **`-ScrubModel`**: Model for cleaning and scrubbing the final text.
-   **`-CheckerModel`**: Model used for internal checks, like JSON validation.
-   **`-TranslatorModel`**: Model used for translation tasks.

## Enhanced Multi-Source RAG System ✅ **UPDATED**

### Core Knowledge Base Parameters

-   **`-KnowledgeBasePath`**
    -   **Type:** `string`
    -   **Description:** The file path to a directory containing Markdown files that make up the knowledge base. If not provided, this feature is disabled.
    -   **Default:** `""`
-   **`-EmbeddingModel`**
    -   **Type:** `string`
    -   **Description:** The model to be used for creating text embeddings. Supports multiple providers:
        - Ollama: `mxbai-embed-large:latest`, `nomic-embed-text:latest`
        - OpenAI: `text-embedding-ada-002`, `text-embedding-3-small`  
        - HuggingFace: `sentence-transformers/all-MiniLM-L6-v2`
    -   **Default:** `mxbai-embed-large:latest`

### Enhanced RAG Configuration ✅ **NEW**

-   **`-OutlineRagEnabled`**
    -   **Type:** `boolean`
    -   **Description:** Enable knowledge retrieval during outline generation phase for context-aware story structure.
    -   **Default:** `true`
-   **`-OutlineContextMaxTokens`**
    -   **Type:** `integer`
    -   **Description:** Maximum token limit for outline-level RAG context injection.
    -   **Default:** `1000`
-   **`-OutlineRagTopK`**
    -   **Type:** `integer`
    -   **Description:** Number of top knowledge base chunks to retrieve for outline context.
    -   **Default:** `5`
-   **`-OutlineRagSimilarityThreshold`**
    -   **Type:** `float`
    -   **Description:** Minimum similarity threshold for including knowledge in outline context.
    -   **Default:** `0.7`

### Multi-Source Knowledge Integration ✅ **NEW**

-   **`-ScratchpadFile`**
    -   **Type:** `string`
    -   **Description:** Path to markdown file containing URLs to fetch and integrate into knowledge base.
    -   **Default:** `""`
-   **`-CoAiAPyDatasets`**
    -   **Type:** `string`
    -   **Description:** Comma-separated list of Langfuse dataset names to retrieve via CoAiAPy fuse.
    -   **Default:** `""`
-   **`-CoAiAPyPrompts`**
    -   **Type:** `string`
    -   **Description:** Comma-separated list of Langfuse prompt names to retrieve via CoAiAPy fuse.
    -   **Default:** `""`
-   **`-ExistingKnowledgeDirs`**
    -   **Type:** `string`
    -   **Description:** Comma-separated list of additional directories to include in knowledge base.
    -   **Default:** `""`
-   **`-WebCacheTTL`**
    -   **Type:** `integer`
    -   **Description:** Time-to-live for web content cache in seconds (3600 = 1 hour).
    -   **Default:** `3600`

## Workflow Control

These parameters control the flow and logic of the story generation pipeline.

-   **`-ExpandOutline`**
    -   **Type:** `boolean`
    -   **Description:** If `true`, the system will generate a detailed, scene-by-scene outline for each chapter before writing the chapter's content.
    -   **Default:** `true`

-   **`-EnableFinalEditPass`**
    -   **Type:** `boolean`
    -   **Description:** If `true`, the system will perform a final editing pass on the entire novel after all chapters have been generated.
    -   **Default:** `false`

-   **`-NoScrubChapters`**
    -   **Type:** `boolean`
    -   **Description:** If `true`, disables the final scrubbing pass that removes prompt artifacts.
    -   **Default:** `false`

-   **`-SceneGenerationPipeline`**
    -   **Type:** `boolean`
    -   **Description:** If `true`, uses the newer, scene-by-scene generation pipeline for writing chapters.
    -   **Default:** `true`

## Revision and Quality Control

These parameters control the behavior of the feedback and revision loops.

-   **`-OutlineMinRevisions`**: Minimum number of revision loops for the main outline.
-   **`-OutlineMaxRevisions`**: Maximum number of revision loops for the main outline.
-   **`-ChapterMinRevisions`**: Minimum number of revision loops for each chapter.
-   **`-ChapterMaxRevisions`**: Maximum number of revision loops for each chapter.
-   **`-NoChapterRevision`**: If `true`, completely disables the chapter revision loop.

## Translation

-   **`-Translate`**
    -   **Type:** `string`
    -   **Description:** The target language for translating the final story (e.g., "French"). If empty, no translation is performed.
    -   **Default:** `""`

-   **`-TranslatePrompt`**
    -   **Type:** `string`
    -   **Description:** The target language for translating the initial user prompt. If empty, no translation is performed.
    -   **Default:** `""`

## Miscellaneous

-   **`-Seed`**
    -   **Type:** `integer`
    -   **Description:** The seed used for the language models to ensure reproducibility.
    -   **Default:** `12`

-   **`-SleepTime`**
    -   **Type:** `integer`
    -   **Description:** The time in seconds to wait between LLM API requests to avoid rate limiting.
    -   **Default:** `31`

-   **`-Debug`**
    -   **Type:** `boolean`
    -   **Description:** If `true`, prints system prompts and other debugging information to the console.
    -   **Default:** `false`

-   **`-MockMode`**
    -   **Type:** `boolean`
    -   **Description:** If `true`, uses mock responses instead of actual LLM calls for testing purposes.
    -   **Default:** `false`
