# Application Logic Diagrams

This document provides visual representations of the Storytelling package workflow using Mermaid diagrams.

## Current Implementation: Single-Pass Workflow

This diagram shows the currently implemented workflow in `storytelling/graph.py`:

```mermaid
graph TD
    Start([User Prompt]) --> Config[Initialize Configuration]
    Config --> RAG{RAG Enabled?}
    RAG -->|Yes| InitRAG[Initialize Knowledge Base]
    RAG -->|No| StoryElements
    InitRAG --> StoryElements
    
    StoryElements[Generate Story Elements<br/>generate_story_elements_node] --> Outline[Generate Initial Outline<br/>generate_initial_outline_node]
    
    Outline --> OutlineRAG{Outline RAG<br/>Enabled?}
    OutlineRAG -->|Yes| RetrieveOutline[Retrieve Outline Context<br/>retrieve_outline_context]
    OutlineRAG -->|No| ChapterCount
    RetrieveOutline --> ChapterCount
    
    ChapterCount[Determine Chapter Count<br/>determine_chapter_count_node] --> ChapterLoop{More<br/>Chapters?}
    
    ChapterLoop -->|Yes| GenChapter[Generate Chapter Scene-by-Scene<br/>generate_single_chapter_scene_by_scene_node]
    GenChapter --> SceneRAG{Scene RAG<br/>Available?}
    SceneRAG -->|Yes| RetrieveScene[Retrieve Scene Context]
    SceneRAG -->|No| IncrementChapter
    RetrieveScene --> IncrementChapter
    IncrementChapter[Increment Chapter Index<br/>increment_chapter_index_node] --> ChapterLoop
    
    ChapterLoop -->|No| FinalStory[Generate Final Story<br/>generate_final_story_node]
    
    FinalStory --> PostProcess{Post-Processing<br/>Options?}
    PostProcess -->|Edit Pass| EditPass[Final Edit Pass]
    PostProcess -->|Scrub| Scrub[Scrub Chapters]
    PostProcess -->|Translate| Translate[Translate Story]
    PostProcess -->|None| Output
    EditPass --> Output
    Scrub --> Output
    Translate --> Output
    
    Output[Save Story Files<br/>Markdown + JSON] --> End([Complete])
    
    style Start fill:#e1f5e1
    style End fill:#e1f5e1
    style StoryElements fill:#fff4e1
    style Outline fill:#fff4e1
    style GenChapter fill:#fff4e1
    style FinalStory fill:#fff4e1
```

## Envisioned Workflow: With Critique and Revision Loops

This diagram shows the intended workflow with critique and revision loops (specified but not yet implemented):

```mermaid
graph TD
    Start([User Prompt]) --> Config[Initialize Configuration]
    Config --> PromptAnalysis[Prompt Analysis<br/>GET_IMPORTANT_BASE_PROMPT_INFO<br/>⏳ NOT IMPLEMENTED]
    PromptAnalysis --> RAG{RAG Enabled?}
    RAG -->|Yes| InitRAG[Initialize Knowledge Base]
    RAG -->|No| StoryElements
    InitRAG --> StoryElements
    
    StoryElements[Generate Story Elements] --> InitOutline[Generate Initial Outline]
    
    InitOutline --> OutlineRAG{Outline RAG<br/>Enabled?}
    OutlineRAG -->|Yes| RetrieveOutline[Retrieve Outline Context]
    OutlineRAG -->|No| OutlineCritique
    RetrieveOutline --> OutlineCritique
    
    OutlineCritique[Critique Outline<br/>CRITIC_OUTLINE_PROMPT<br/>⏳ NOT IMPLEMENTED] --> OutlineComplete{Outline<br/>Complete?<br/>⏳ NOT IMPLEMENTED}
    OutlineComplete -->|No| OutlineRevision[Revise Outline<br/>OUTLINE_REVISION_PROMPT<br/>⏳ NOT IMPLEMENTED]
    OutlineRevision --> OutlineRevCount{Max Revisions<br/>Reached?}
    OutlineRevCount -->|No| OutlineCritique
    OutlineRevCount -->|Yes| ChapterCount
    OutlineComplete -->|Yes| ChapterCount
    
    ChapterCount[Determine Chapter Count] --> ChapterLoop{More<br/>Chapters?}
    
    ChapterLoop -->|Yes| GenChapter[Generate Chapter<br/>Multi-Stage Pipeline]
    GenChapter --> SceneRAG{Scene RAG<br/>Available?}
    SceneRAG -->|Yes| RetrieveScene[Retrieve Scene Context]
    SceneRAG -->|No| ChapterCritique
    RetrieveScene --> ChapterCritique
    
    ChapterCritique[Critique Chapter<br/>CRITIC_CHAPTER_PROMPT<br/>⏳ NOT IMPLEMENTED] --> ChapterComplete{Chapter<br/>Complete?<br/>⏳ NOT IMPLEMENTED}
    ChapterComplete -->|No| ChapterRevision[Revise Chapter<br/>CHAPTER_REVISION<br/>⏳ NOT IMPLEMENTED]
    ChapterRevision --> ChapterRevCount{Max Revisions<br/>Reached?}
    ChapterRevCount -->|No| ChapterCritique
    ChapterRevCount -->|Yes| IncrementChapter
    ChapterComplete -->|Yes| IncrementChapter
    
    IncrementChapter[Increment Chapter Index] --> ChapterLoop
    
    ChapterLoop -->|No| FinalStory[Generate Final Story]
    
    FinalStory --> PostProcess{Post-Processing<br/>Options?}
    PostProcess -->|Edit Pass| EditPass[Final Edit Pass]
    PostProcess -->|Scrub| Scrub[Scrub Chapters]
    PostProcess -->|Translate| Translate[Translate Story]
    PostProcess -->|None| Output
    EditPass --> Output
    Scrub --> Output
    Translate --> Output
    
    Output[Save Story Files<br/>Markdown + JSON] --> End([Complete])
    
    style Start fill:#e1f5e1
    style End fill:#e1f5e1
    style PromptAnalysis fill:#ffe1e1
    style OutlineCritique fill:#ffe1e1
    style OutlineComplete fill:#ffe1e1
    style OutlineRevision fill:#ffe1e1
    style ChapterCritique fill:#ffe1e1
    style ChapterComplete fill:#ffe1e1
    style ChapterRevision fill:#ffe1e1
```

## Node Comparison Table

| Node/Feature | Status | Implementation | Prompts Used |
|-------------|--------|----------------|--------------|
| **Initialize Configuration** | ✅ Implemented | `storytelling/config.py` | - |
| **Prompt Analysis** | ⏳ Not Implemented | - | `GET_IMPORTANT_BASE_PROMPT_INFO` |
| **Generate Story Elements** | ✅ Implemented | `generate_story_elements_node` | `STORY_ELEMENTS_PROMPT` |
| **Generate Initial Outline** | ✅ Implemented | `generate_initial_outline_node` | `INITIAL_OUTLINE_PROMPT` |
| **Critique Outline** | ⏳ Not Implemented | - | `CRITIC_OUTLINE_PROMPT` |
| **Check Outline Complete** | ⏳ Not Implemented | - | `OUTLINE_COMPLETE_PROMPT` |
| **Revise Outline** | ⏳ Not Implemented | - | `OUTLINE_REVISION_PROMPT` |
| **Determine Chapter Count** | ✅ Implemented | `determine_chapter_count_node` | `CHAPTER_COUNT_PROMPT` |
| **Generate Chapter** | ✅ Implemented | `generate_single_chapter_scene_by_scene_node` | `CHAPTER_GENERATION_STAGE1-4` |
| **Critique Chapter** | ⏳ Not Implemented | - | `CRITIC_CHAPTER_PROMPT` |
| **Check Chapter Complete** | ⏳ Not Implemented | - | `CHAPTER_COMPLETE_PROMPT` |
| **Revise Chapter** | ⏳ Not Implemented | - | `CHAPTER_REVISION` |
| **Generate Final Story** | ✅ Implemented | `generate_final_story_node` | `STATS_PROMPT` |

## Configuration Parameters Status

These parameters are defined in `storytelling/config.py` but not utilized due to missing critique/revision nodes:

- `outline_min_revisions` (default: 1) - ⏳ Not Used
- `outline_max_revisions` (default: 3) - ⏳ Not Used
- `chapter_min_revisions` (default: 1) - ⏳ Not Used
- `chapter_max_revisions` (default: 3) - ⏳ Not Used
- `no_chapter_revision` (default: False) - ⏳ Not Used

## Implementation Roadmap

To achieve the envisioned workflow with critique/revision loops:

1. **Add Prompt Analysis Node**: Create node that uses `GET_IMPORTANT_BASE_PROMPT_INFO` to extract context
2. **Add Outline Critique/Revision Nodes**: 
   - Create `critique_outline_node` using `CRITIC_OUTLINE_PROMPT`
   - Create `check_outline_complete_node` using `OUTLINE_COMPLETE_PROMPT`
   - Create `revise_outline_node` using `OUTLINE_REVISION_PROMPT`
   - Add conditional edges based on completion status and revision counts
3. **Add Chapter Critique/Revision Nodes**:
   - Create `critique_chapter_node` using `CRITIC_CHAPTER_PROMPT`
   - Create `check_chapter_complete_node` using `CHAPTER_COMPLETE_PROMPT`
   - Create `revise_chapter_node` using `CHAPTER_REVISION`
   - Add conditional edges based on completion status and revision counts
4. **Integrate Configuration Parameters**: Use `outline_min_revisions`, `outline_max_revisions`, `chapter_min_revisions`, `chapter_max_revisions` in loop control logic
5. **Test Iterative Refinement**: Validate that critique loops improve story quality

This roadmap would transform the current single-pass workflow into an iterative refinement system that advances stories through structured feedback loops.
