# RISPECS.md: Handoff to Copilot Agent for `storytelling` Project Specifications

## Structural Tension
- **Desired Outcome**: The `rispecs/` directory accurately and comprehensively reflects the current implementation status and future vision of the `storytelling` package, fully aligned with the RISE Framework and Creative Orientation principles.
- **Current Reality**: The existing `rispecs/` contain a mix of implemented, proposed, and under-revision specifications, with some discrepancies between documentation and code, and a lack of consistent RISE framework application.
- **Natural Progression**: A systematic update of all `rispecs/` documents, guided by this handoff, to achieve complete synchronization with the codebase and full adherence to Creative Orientation principles.

## Executive Summary

This document serves as a comprehensive handoff to the Copilot Agent for updating the `rispecs/` directory within the `storytelling` project. The `storytelling` package is an AI-powered narrative generation system that leverages advanced LLM orchestration, RAG, and session management to empower users in creating coherent and polished narratives.

The primary goal of this task is to bring all specifications in `rispecs/` up-to-date, ensuring they accurately reflect the current state of the `storytelling` codebase, align with the principles of the RISE Framework, and adhere to the Creative Orientation Operating Guide.

## Current State of `storytelling` Package

The `storytelling` package (also known as `WillWrite` or `specforge`) is a Python application with the following key features and architectural components:

*   **Core Functionality**: Narrative generation pipeline using `pydantic`, `langchain`, and `langgraph`.
*   **Session Management**: Robust checkpointing and resume capabilities (`SessionManager`, `SessionCheckpoint`, `SessionInfo`).
*   **Multi-Source RAG**: Production-ready Retrieval-Augmented Generation system integrating web content, CoAiAPy fuse, and local files. Supports Ollama, OpenAI, and HuggingFace embedding models. Scene-level RAG is implemented.
*   **LLM Provider Abstraction**: URI-based configuration for `ollama`, `google`, and `openrouter` models.
*   **Logging and Traceability**: Enhanced logging with Langfuse integration and local fallback.
*   **IAIP Integration**: Optional modules for Indigenous-AI Collaborative Platform practices (`iaip_bridge`, `ceremonial_diary`).
*   **Tiered Package Architecture**: Designed for flexible installations based on user needs (Core, Knowledge-Enhanced, Specialized).

## RISE Framework Overview

The RISE Framework (Reverse-engineer, Intent-extract, Specify, Export) is central to this project's development philosophy. It emphasizes:

*   **Creative Orientation**: Focusing on what applications enable users to *create* and *achieve*, rather than merely eliminating issues.
*   **Structural Tension**: Leveraging the dynamic relationship between Current Reality and Desired Outcome to drive natural progression.
*   **Advancing Patterns**: Designing systems that consistently move towards desired outcomes, avoiding oscillating behaviors.
*   **"Create-Language"**: Preferring generative verbs (create, manifest, build, enable, stabilize) over problem-elimination phrasing (fix, mitigate, eliminate, solve).

All updates to the `rispecs/` must embody these principles.

## Detailed Analysis of `rispecs/` and Required Updates

The following is a file-by-file analysis of the `rispecs/` directory, detailing its current status, alignment with RISE, and specific instructions for the Copilot Agent.

---

### 1. `AGENT_INSTRUCTIONS.md`
*   **Current Status**: Up-to-date in its general directives.
*   **RISE Alignment**: Explicitly references `Creative_Orientation_Operating_Guide.md` and RISE principles.
*   **Required Updates**:
    *   Ensure the "PROPOSED" tag for "Creative Orientation Operating Rules" is removed if `Creative_Orientation_Operating_Guide.md` is updated to `✅ IMPLEMENTED`.
    *   Verify all references to `specifications/` are correct.

### 2. `ApplicationLogic.md`
*   **Current Status**: High-level overview, but lacks detail on LangGraph nodes and edges.
*   **RISE Alignment**: Describes workflow in terms of "multi-step process" and "feedback loop," which can be reframed as advancing patterns.
*   **Required Updates**:
    *   Update the document to explicitly describe the workflow in terms of LangGraph nodes and edges, aligning with `storytelling/graph.py`.
    *   Integrate the concept of "Creative Advancement Scenarios" from `RISE_Spec.md` into the description of each major stage.
    *   Refine language to consistently use "create-language" and avoid problem-elimination phrasing.
    *   Update the status to `✅ IMPLEMENTED`.

### 3. `Architect_Agent_Specification.md`
*   **Current Status**: Well-defined role for an Architect Agent.
*   **RISE Alignment**: Strongly aligned, explicitly mentioning "creative archaeology" and RISE framework.
*   **Required Updates**:
    *   Update the status to `✅ IMPLEMENTED` if the Architect Agent's workflow is fully operational.
    *   Ensure consistency with the updated `RISE_Spec.md` and `Creative_Orientation_Operating_Guide.md`.

### 4. `CO_Lint_Spec.md`
*   **Current Status**: `PROPOSED`.
*   **RISE Alignment**: Excellent, as it directly enforces Creative Orientation governance.
*   **Required Updates**:
    *   **Crucial**: Implement the `co-lint` tool as described.
    *   Update the status to `✅ IMPLEMENTED` once the linter is functional and integrated into the CI/CD pipeline (e.g., via `pre-commit` hooks or GitHub Actions).
    *   Remove all "PROPOSED" tags once implemented.

### 5. `Configuration.md`
*   **Current Status**: `✅ UPDATED` for RAG, but missing several new parameters from `storytelling/config.py` and `Outline_Level_RAG_Integration_SpecificationV3.md`.
*   **RISE Alignment**: Defines parameters that enable various creative workflows.
*   **Required Updates**:
    *   **Critical**: Synchronize all configuration parameters with the `WillWriteConfig` class in `src/storytelling/config.py`. This includes:
        *   Adding `mock_mode` parameter.
        *   Adding `outline_dynamic_rag_enabled`, `outline_critique_context_max_tokens`, `outline_semantic_adaptation_model`, `outline_rise_prioritization_enabled`, and `outline_rise_tag_model` from `Outline_Level_RAG_Integration_SpecificationV3.md`.
        *   Adding `ScratchpadFile`, `CoAiAPyDatasets`, `CoAiAPyPrompts`, `ExistingKnowledgeDirs`, `WebCacheTTL` from `Enhanced_Multi_Source_RAG_Specification.md`.
    *   Update the status to `✅ IMPLEMENTED` once fully synchronized.

### 6. `Creative_Environment_Serialization.md`
*   **Current Status**: `✅ SPECIFICATION COMPLETE`, but implementation phases are marked `⏳`.
*   **RISE Alignment**: Directly addresses "perfect creative consciousness fidelity" and "advancing pattern architecture."
*   **Required Updates**:
    *   Update the implementation phases (`⏳`) to `✅ IMPLEMENTED` as they are completed in `storytelling/session_manager.py`.
    *   Verify that the `SessionCheckpoint` structure in `DataSchemas.md` and `storytelling/session_manager.py` matches the enhanced structure described here.
    *   Update the overall status to `✅ IMPLEMENTED` once all phases are complete.

### 7. `Creative_Orientation_Operating_Guide.md`
*   **Current Status**: `PROPOSED`.
*   **RISE Alignment**: Core document for operationalizing Creative Orientation.
*   **Required Updates**:
    *   Remove all "PROPOSED" tags once the principles are fully integrated and enforced (e.g., by `CO_Lint_Spec.md`).
    *   Update the status to `✅ IMPLEMENTED`.

### 8. `DataSchemas.md`
*   **Current Status**: `✅ IMPLEMENTED` for Session Management, but needs to reflect the enhanced `SessionCheckpoint` from `Creative_Environment_Serialization.md`.
*   **RISE Alignment**: Defines the structured data that supports creative workflows.
*   **Required Updates**:
    *   Update the `SessionCheckpoint` schema to include `creative_environment: CreativeEnvironmentState` and define `CreativeEnvironmentState`, `RAGState`, and `ModelState` dataclasses.
    *   Add schemas for any new data structures introduced by the enhanced RAG or IAIP integration.
    *   Update the status to `✅ IMPLEMENTED` once fully synchronized.

### 9. `Enhanced_Multi_Source_RAG_Specification.md`
*   **Current Status**: `✅ PRODUCTION-READY`.
*   **RISE Alignment**: Excellent, explicitly uses RISE framework application and identifies Advancing Patterns.
*   **Required Updates**:
    *   Ensure all implementation details (e.g., `Web Content Fetcher`, `CoAiAPy Fuse Integration`, `Enhanced RAG System`) are fully reflected in the code (`storytelling/web_fetcher.py`, `storytelling/coaia_fuse.py`, `storytelling/enhanced_rag.py`).
    *   Verify that the "Future Enhancements" section is still relevant or has been integrated into other specs.
    *   Update the status to `✅ IMPLEMENTED`.

### 10. `ImplementationNotes.md`
*   **Current Status**: `✅ IMPLEMENTED` for RAG, but needs to be updated for other sections.
*   **RISE Alignment**: Provides practical guidance for implementing creative-oriented architecture.
*   **Required Updates**:
    *   Update sections 1-4 to reflect the current implementation status and specific modules used (e.g., `storytelling/config.py`, `storytelling/data_models.py`, `storytelling/llm_providers.py`, `storytelling/graph.py`, `storytelling/prompts.py`).
    *   Ensure the `Logging and Traceability` section reflects the `✅ UPDATED` status from `Logging_And_Traceability_Specification.md`.
    *   Update the status to `✅ IMPLEMENTED`.

### 11. `KnowledgeBase_Extension.md`
*   **Current Status**: `✅ IMPLEMENTED` and `✅ COMPLETE`.
*   **RISE Alignment**: Focuses on empowering the agent to create consistent stories.
*   **Required Updates**:
    *   Verify that the `⚠️ PLANNED` status for "Outline-Level Retrieval" has been updated based on the progress in `Outline_Level_RAG_Integration_SpecificationV3.md`.
    *   Ensure consistency with `Enhanced_Multi_Source_RAG_Specification.md` and `RAG_Implementation_Specification.md`.
    *   Update the status to `✅ IMPLEMENTED`.

### 12. `LLM_Provider_Specification.md`
*   **Current Status**: `✅ NEW` for Google Model Variants.
*   **RISE Alignment**: Defines the tools for creative manifestation.
*   **Required Updates**:
    *   Update the status of `myflowise` provider scheme from "not yet implemented" to reflect its current status in `storytelling/llm_providers.py`. If it's still not implemented, explicitly state that.
    *   Update the status to `✅ IMPLEMENTED`.

### 13. `Logging_And_Traceability_Specification.md`
*   **Current Status**: `✅ UPDATED` with Langfuse integration.
*   **RISE Alignment**: Ensures full traceability of the creative process.
*   **Required Updates**:
    *   Verify that the `WillWriteTracer` class is indeed in `src/storytelling/__main__.py` or update the path to its actual location (e.g., `src/storytelling/logger.py` if integrated there).
    *   Update the status to `✅ IMPLEMENTED`.

### 14. `Outline_Level_RAG_Integration_SpecificationV1.md`
*   **Current Status**: "Ready for Implementation," but superseded by `V3`.
*   **RISE Alignment**: Aims to provide knowledge-aware story foundation.
*   **Required Updates**:
    *   **Deprecate or Merge**: This document should either be deprecated in favor of `V3` or its implemented aspects should be merged into `V3`.
    *   If deprecated, update its status accordingly. If merged, remove this file.

### 15. `Outline_Level_RAG_Integration_SpecificationV3.md`
*   **Current Status**: "Under Revision."
*   **RISE Alignment**: Highly aligned, integrating "Event-Driven Adaptive RAG" with "Unified Creative Orientation Framework."
*   **Required Updates**:
    *   **Critical**: Update the implementation status of all phases (`⏳`) to `✅ IMPLEMENTED` as they are completed in the codebase.
    *   Ensure all new configuration parameters are added to `Configuration.md` and `storytelling/config.py`.
    *   Ensure all new functions (`retrieve_and_transpose_outline_context`, `apply_semantic_adaptation_layer`, `prioritize_rise_docs`) are implemented in `storytelling/rag.py` or `storytelling/enhanced_rag.py`.
    *   Update prompt templates in `Prompts.md` to reflect the enhanced RAG context and advanced prompting strategies.
    *   Update the overall status to `✅ IMPLEMENTED` once all phases are complete.

### 16. `Outline_Stage_RAG_Injection.md`
*   **Current Status**: `PROPOSED`.
*   **RISE Alignment**: Defines criteria for RAG injection.
*   **Required Updates**:
    *   Merge its content into `Outline_Level_RAG_Integration_SpecificationV3.md` as it's a more detailed and advanced specification for outline RAG.
    *   Update its status to `DEPRECATED` or remove the file after merging.

### 17. `ProceduralLogic.md`
*   **Current Status**: Detailed, but needs to reflect LangGraph implementation more explicitly.
*   **RISE Alignment**: Describes the step-by-step progression of the creative process.
*   **Required Updates**:
    *   Update the "Generate Outline" sub-procedure to explicitly reference the `retrieve_outline_context` function and the `outline_rag_enabled` config parameter.
    *   Ensure the LangGraph nodes and edges are clearly mapped to the procedures described.
    *   Update the status to `✅ IMPLEMENTED`.

### 18. `Prompts.md`
*   **Current Status**: Contains prompt texts, but needs to reflect enhanced RAG context and IAIP integration.
*   **RISE Alignment**: Direct input for LLM calls, shaping creative output.
*   **Required Updates**:
    *   Update `INITIAL_OUTLINE_PROMPT` and `CRITIC_OUTLINE_PROMPT` to use the `rag_context` placeholder as defined in `Outline_Level_RAG_Integration_SpecificationV3.md`.
    *   Add any new prompts introduced by IAIP integration (e.g., `CEREMONIAL_INTENTION_PROMPT`, `TWO_EYED_SEEING_PROMPT`, `NORTH_DIRECTION_REFLECTION_PROMPT`, `STORYTELLING_CIRCLE_PROMPT`, `CEREMONIAL_DIARY_ENTRY_PROMPT`, `ANCESTRAL_WISDOM_INTEGRATION_PROMPT`).
    *   Update the status to `✅ IMPLEMENTED`.

### 19. `RAG_Implementation_Specification.md`
*   **Current Status**: `✅ UPDATED` and `✅ PRODUCTION-READY`.
*   **RISE Alignment**: Explicitly uses RISE framework application and identifies Advancing Patterns.
*   **Required Updates**:
    *   Ensure consistency with `Enhanced_Multi_Source_RAG_Specification.md`.
    *   Update the "Future Enhancements" section to reflect any implemented features or new plans.
    *   Update the status to `✅ IMPLEMENTED`.

### 20. `Resume_Current_Session_Semantics.md`
*   **Current Status**: `✅ IMPLEMENTED` and `✅ PHOENIX_WEAVE COMPLETE`.
*   **RISE Alignment**: Focuses on seamless resume behavior and narrative forking.
*   **Required Updates**:
    *   Update the "Standardized Checkpoint Format (PROPOSED)" and "Re-hydration for Narrative Forking (PROPOSED)" sections to `✅ IMPLEMENTED` if these features are now in the codebase.
    *   Ensure the `SessionCheckpoint` schema matches `DataSchemas.md` and `Creative_Environment_Serialization.md`.
    *   Update the status to `✅ IMPLEMENTED`.

### 21. `RISE_Spec.md`
*   **Current Status**: `PROPOSED` for "Operating Governance" and states it "will be expanded."
*   **RISE Alignment**: This is the core document defining the application's purpose through RISE.
*   **Required Updates**:
    *   Remove the "PROPOSED" tag for "Operating Governance" if `Creative_Orientation_Operating_Guide.md` is updated to `✅ IMPLEMENTED`.
    *   **Critical**: Expand the "Creative Advancement Scenarios" section to include Scenario 4 ("Augmenting Creation with External Knowledge") and any other major advancements.
    *   Update the status to `✅ IMPLEMENTED`.

### 22. `Session_Management_Architecture.md`
*   **Current Status**: `✅ COMPLETE`.
*   **RISE Alignment**: Focuses on persistent creative sessions and resilient creative flow.
*   **Required Updates**:
    *   Ensure consistency with `Creative_Environment_Serialization.md` regarding enhanced `SessionCheckpoint` and environment-aware resume.
    *   Update the status to `✅ IMPLEMENTED`.

### 23. `Terms_of_Agreement.md`
*   **Current Status**: `PROPOSED`.
*   **RISE Alignment**: Defines core terms for RISE compliance.
*   **Required Updates**:
    *   Remove all "PROPOSED" tags once the definitions are finalized and consistently applied.
    *   Update the status to `✅ IMPLEMENTED`.

### 24. `TestPreset_3Chapter.md`
*   **Current Status**: `PROPOSED`.
*   **RISE Alignment**: Applies RISE principles to testing.
*   **Required Updates**:
    *   Update the status to `✅ IMPLEMENTED` if this test preset is now functional and integrated into the testing framework.

### 25. `Tiered_Package_Architecture.md`
*   **Current Status**: `✅ Specification Complete`, but `🔄 Implementation Required`.
*   **RISE Alignment**: Enables users to create workflows matching their resources.
*   **Required Updates**:
    *   **Critical**: Complete the `🔄 Implementation Required` tasks, including moving dependencies, updating `rag.py` and `config.py` for graceful degradation and tier awareness.
    *   Update the status to `✅ IMPLEMENTED`.

### New Specification Required: IAIP Integration
*   **Current Status**: Not present in `rispecs/`, but `IAIP_INTEGRATION` is enabled in `storytelling/__init__.py`.
*   **RISE Alignment**: This integration likely supports "Creative Advancement Scenarios" related to wisdom-keeping, reflection, and ceremonial practices.
*   **Required Updates**:
    *   **Critical**: Create a new specification file, e.g., `IAIP_Integration_Specification.md`, detailing the `NorthDirectionStoryteller`, `TwoEyedSeeingStorytellingAdapter`, `CeremonialPhase`, `DiaryEntry`, `CeremonialDiary`, and `DiaryManager` classes and their role in the `storytelling` workflow.
    *   Ensure this new spec includes Structural Tension blocks, Creative Advancement Scenarios, and uses "create-language."

---

## General Directives for Copilot Agent

1.  **Adherence to RISE Principles**: All updates must strictly follow the principles outlined in `llms-rise-framework.txt` and `llms-rise-framework-full.txt`.
2.  **Creative Orientation Operating Guide**: Apply the rules from `Creative_Orientation_Operating_Guide.md` (even if still `PROPOSED`) to all documentation updates, including:
    *   Using Structural Tension blocks.
    *   Neutral Observations.
    *   Structural Assessment (advancing/oscillating patterns).
    *   "Create-language" over "problem-elimination phrasing."
3.  **Terms of Agreement**: Ensure all terminology aligns with `Terms_of_Agreement.md`.
4.  **Code Synchronization**: Verify that all documented features and parameters are accurately reflected in the `storytelling` codebase, especially in `storytelling/config.py`, `storytelling/rag.py`, `storytelling/session_manager.py`, and `storytelling/llm_providers.py`.
5.  **Status Updates**: Update the `Status` tags (e.g., `PROPOSED`, `Under Revision`, `✅ IMPLEMENTED`, `✅ COMPLETE`) in each document to reflect its current state accurately.
6.  **Consistency**: Ensure cross-document consistency, especially for shared concepts like `SessionCheckpoint` and RAG parameters.
7.  **Deprecation/Removal**: Deprecate or remove outdated/merged specifications as instructed.

## Verification Steps for Copilot Agent

After making the updates, the Copilot Agent must perform the following verification:

1.  **Linting Check**: If `CO_Lint_Spec.md` is implemented, run the `co-lint` tool across all `rispecs/` to ensure compliance with Creative Orientation governance.
2.  **Code-Spec Alignment**: Manually (or with automated tools if available) verify that the updated specifications accurately reflect the current state of the `storytelling` codebase.
3.  **RISE Compliance**: Review each updated document to ensure it adheres to the RISE framework principles and uses "create-language" consistently.
4.  **Cross-Referencing**: Verify that all internal and external cross-references within `rispecs/` are correct and up-to-date.

This comprehensive update will ensure the `rispecs/` directory becomes a reliable and accurate source of truth for the `storytelling` project, fully embodying the principles of Creative Orientation and the RISE Framework.
