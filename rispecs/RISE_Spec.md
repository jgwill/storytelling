# WillWrite: A RISE-Based Specification

**Status**: ✅ IMPLEMENTED

> Operating Governance: This specification is governed by `rispecs/Creative_Orientation_Operating_Guide.md`. Include the following blocks in top-level docs and agent outputs: Structural Tension, Observations (neutral), Structural Assessment, and optional Advancing Moves.

**Structural Tension**
- Desired Outcome: Empower users to create complete, coherent narratives from simple prompts through advancing patterns.
- Current Reality: Users begin with unstructured ideas; the system provides robust multi-stage generation, RAG integration, and session management capabilities.
- Natural Progression: Continue to refine and enhance specifications that stabilize behavior while preserving Creative Orientation.

This document provides a creative-oriented specification for the `WillWrite` application, following the principles of the RISE Framework. It focuses on what the application empowers users to create, the structural dynamics that enable this creation, and the advancing patterns that guide the process from a simple idea to a fully realized story.

For details on the specific prompts, data structures, and configuration options, please refer to the following documents:
-   `Prompts.md`
-   `DataSchemas.md`
-   `Configuration.md`
-   `LLM_Provider_Specification.md`
-   `Logging_And_Traceability_Specification.md`
-   `ImplementationNotes.md`

## 1. Core Creative Intent

The fundamental purpose of `WillWrite` is to **empower a user to manifest a complete, coherent, and polished narrative from a nascent creative idea.**

It is a tool for creation, designed to transform a simple prompt or concept into a structured, multi-chapter story with well-defined characters, plot, and themes. It acts as a collaborative partner that handles the structural heavy lifting, allowing the user to focus on the creative vision.

## 2. The Central Structural Tension

The application's entire workflow is driven by the structural tension between the user's initial state and their desired outcome.

*   **Current Reality:** The user possesses a simple, often unstructured, creative prompt or idea. This idea has potential but lacks form, detail, and narrative structure.

*   **Desired Outcome:** The user wants to create a fully-formed, multi-chapter story that is internally consistent, engaging, and ready to be shared.

The `WillWrite` application is the system designed to resolve this tension. Every feature and workflow step is a component of the structure that enables the natural progression from `Current Reality` to `Desired Outcome`.

## 3. Creative Advancement Scenarios

The application resolves this tension through a series of advancing patterns, which can be described as Creative Advancement Scenarios. Each scenario represents a major stage in the journey from prompt to story.

---

### Scenario 1: Manifesting the Story Foundation

This scenario describes the process of transforming the user's initial, high-level prompt into a structured and detailed foundation for the narrative.

**Desired Outcome:** To create a comprehensive and coherent story outline, complete with well-defined characters, plot points, and thematic elements, that can serve as a reliable blueprint for writing the full narrative.

**Current Reality:** The user has a simple, unstructured text prompt containing the core idea for a story.

**Natural Progression:** The system is structured to guide the user's idea through a process of clarification and elaboration, naturally resolving the tension between the unstructured idea and the need for a structured plan.

**Resolution:** A detailed, multi-chapter outline and a set of story elements are generated and refined, providing a solid foundation for the subsequent chapter-writing phase.

**Advancement Pattern Steps:**

1.  **Clarifying the Vision:** The system first analyzes the user's prompt to extract the core creative vision and any high-level constraints (e.g., tone, style). This initial step ensures the subsequent process is aligned with the user's fundamental intent.
    *   **Supporting Prompt:** `GET_IMPORTANT_BASE_PROMPT_INFO` (see `Prompts.md`)

2.  **Structuring the Core Idea:** The system generates the foundational "Story Elements." This is a crucial step that transforms the abstract idea into a concrete set of narrative components (characters, plot, theme, etc.), providing the initial structure needed to resolve the tension.
    *   **Supporting Prompt:** `STORY_ELEMENTS_PROMPT` (see `Prompts.md`)

3.  **Generating the Narrative Blueprint:** Using the structured Story Elements, the system generates an initial, chapter-by-chapter outline. This creates the primary advancing pattern, a clear path from the beginning to the end of the story.
    *   **Supporting Prompt:** `INITIAL_OUTLINE_PROMPT` (see `Prompts.md`)

4.  **Refining the Foundation (Feedback Loop):** The system then enters a refinement loop. This is not a reactive "fixing" process, but a creative collaboration to enhance the structure.
    *   An AI critic provides feedback, not on "errors," but on opportunities to strengthen the narrative structure, pacing, and flow. This advances the outline towards a more robust state.
    *   The outline is revised based on this feedback, further resolving the tension towards the desired outcome of a complete and coherent blueprint.
    *   **Supporting Prompts:** `CRITIC_OUTLINE_PROMPT`, `OUTLINE_REVISION_PROMPT`, `OUTLINE_COMPLETE_PROMPT` (see `Prompts.md`)

---

### Scenario 2: Crafting the Narrative, Chapter by Chapter

This scenario describes the iterative process of transforming the foundational outline into the full text of the story, one chapter at a time.

**Desired Outcome:** To create a complete, well-written chapter that is consistent with the overall story outline and the previously written chapters, and that is ready for the final post-processing stages.

**Current Reality:** The system has a complete story outline and may have a set of previously written chapters. The current chapter exists only as a set of ideas in the outline.

**Natural Progression:** The system is structured to build upon the existing foundation (the outline and previous chapters), adding layers of detail and complexity in a structured way to naturally progress from a high-level plan to a fully realized chapter.

**Resolution:** A complete, multi-faceted chapter is generated and refined, ready to be added to the story.

**Advancement Pattern Steps:**

1.  **Establishing Chapter Context:** The system first establishes the context for the new chapter.
    *   It determines the total number of chapters to understand the current chapter's place in the overall narrative arc.
    *   It can optionally generate a detailed, scene-by-scene outline for the current chapter, creating a more granular advancing pattern.
    *   **Supporting Prompts:** `CHAPTER_COUNT_PROMPT`, `CHAPTER_OUTLINE_PROMPT` (see `Prompts.md`)

2.  **Staged Content Generation (Layered Creation):** The system then generates the chapter's content in a series of stages. This is not a linear process, but a layering of creative elements that builds complexity and depth.
    *   **Layer 1: Plot:** The fundamental plot of the chapter is written, creating the narrative backbone.
    *   **Layer 2: Character Development:** The characters' internal and external development is woven into the plot, adding emotional depth.
    *   **Layer 3: Dialogue:** Dialogue is added, bringing the characters to life and advancing the plot through interaction.
    *   **Supporting Prompts:** `CHAPTER_GENERATION_STAGE1`, `CHAPTER_GENERATION_STAGE2`, `CHAPTER_GENERATION_STAGE3` (see `Prompts.md`)

3.  **Alternative Path: Scene-by-Scene Generation:** As an alternative advancing pattern, the system can generate the chapter scene by scene. This provides a more modular and focused approach to chapter creation.

4.  **Refining the Chapter (Feedback Loop):** Similar to the outline generation, the chapter enters a refinement loop to ensure it aligns with the creative vision.
    *   An AI critic provides feedback on the chapter's narrative coherence, pacing, and characterization.
    *   The chapter is revised based on this feedback, ensuring it integrates seamlessly with the rest of the story.
    *   **Supporting Prompts:** `CRITIC_CHAPTER_PROMPT`, `CHAPTER_REVISION`, `CHAPTER_COMPLETE_PROMPT` (see `Prompts.md`)

---

### Scenario 3: Polishing and Finalizing the Story

This scenario describes the final stages of the writing process, where the generated chapters are polished, and the final story files are created.

**Desired Outcome:** To produce a complete, polished, and ready-to-share story in multiple formats, along with all the relevant metadata.

**Current Reality:** The system has a complete set of generated chapters, but they may contain artifacts from the generation process and have not yet been unified into a final product.

**Natural Progression:** The system is structured to take the raw output of the creative process and refine it through a series of optional, quality-enhancing steps, naturally progressing from a collection of chapters to a finished work.

**Resolution:** A polished, multi-format story is generated and saved to disk, completing the user's creative journey.

**Advancement Pattern Steps:**

1.  **Holistic Editing (Optional):** The system can perform a final edit pass of the entire novel. This step ensures consistency and flow across all chapters, unifying them into a single, cohesive narrative.
    *   **Supporting Prompt:** `CHAPTER_EDIT_PROMPT` (see `Prompts.md`)

2.  **Cleaning and Scrubbing (Optional):** The system can "scrub" the chapters to remove any leftover prompt fragments or other generation artifacts. This is a crucial step in advancing the story from a "generated" text to a "written" one.
    *   **Supporting Prompt:** `CHAPTER_SCRUB_PROMPT` (see `Prompts.md`)

3.  **Translation (Optional):** The system can translate the entire novel into another language, making the story accessible to a wider audience.
    *   **Supporting Prompt:** `CHAPTER_TRANSLATE_PROMPT` (see `Prompts.md`)

4.  **Generating Story Metadata:** The system generates the final metadata for the story, including the title, summary, and tags. This provides a concise and shareable overview of the created work.
    *   **Supporting Prompt:** `STATS_PROMPT` (see `Prompts.md`)

5.  **Final Output Generation:** The system generates the final output files:
    *   A Markdown file containing the complete, polished story, along with all the generated statistics and the original outline.
    *   A JSON file containing a structured representation of the entire story generation process, including the outline, story elements, and all generated chapters. This preserves the "creative history" of the work.

---

### Scenario 4: Augmenting Creation with External Knowledge

**Desired Outcome:** To create a story that is deeply and consistently woven into the fabric of a pre-existing creative universe, lore, or style guide.

**Current Reality:** The system has a creative prompt but lacks specific, deep knowledge of the user's unique world, characters, or stylistic requirements.

**Natural Progression:** The system is structured to seamlessly integrate external knowledge at key creative junctures (outline and chapter generation). By retrieving relevant context just-in-time, it resolves the tension between the general-purpose storyteller and the need for domain-specific expertise.

**Resolution:** A narrative is generated that not only fulfills the prompt but also adheres to the rules, lore, and style of the provided knowledge base, demonstrating a deeper level of creative partnership.

**Advancement Pattern Steps:**

1.  **Knowledge Ingestion:** The system first absorbs the user-provided knowledge base, transforming unstructured documents into a retrievable format. This establishes a foundation of expertise.
2.  **Context-Aware Outlining:** During outline generation, the system retrieves knowledge relevant to the core prompt. This ensures the foundational structure of the story is aligned with the established lore from the outset.
3.  **Context-Aware Chapter Generation:** As each chapter is crafted, the system retrieves specific details relevant to the scenes and characters involved. This injects fine-grained consistency and richness into the narrative, ensuring details like character backstories, location descriptions, and specific terminology are correctly applied.
