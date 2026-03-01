# WillWrite Enhanced Logging and Traceability Specification

**Status**: ✅ IMPLEMENTED (Core Features), ⏳ PLANNED (Langfuse Tracing)

This document defines the logging, session management, and observability features for the `WillWrite` application. The core principle is to ensure that every step of the creative process is recorded for debugging, analysis, and full transparency.

## 1. Core Principles

-   **Full Traceability:** Every interaction with an LLM, including the exact prompt, context, and response, must be captured and saved.
-   **Structured and Human-Readable:** Logs should be available in both machine-readable (JSON) and human-readable (Markdown, console output) formats.
-   **Session-Based:** All logs and artifacts for a single run of the application should be stored in a unique, timestamped directory to prevent collisions and ensure clear separation of runs.

## 2. Log Directory Structure

All output, including logs and the final story, must be saved within a main session directory.

-   **Root Directory:** `Logs/`
-   **Session Directory:** A unique directory should be created for each run, named with a timestamp prefix (e.g., `Generation_YYYY-MM-DD_HH-MM-SS/`).
-   **Traceability Subdirectory:** Inside the session directory, a subdirectory named `LangchainDebug/` must be created to store the detailed LLM interaction logs.

**Example Structure:**
```
Logs/
└── Generation_2025-08-05_10-30-00/
    ├── LangchainDebug/
    │   ├── 0_Main.GenerateOutline.json
    │   ├── 0_Main.GenerateOutline.md
    │   ├── 1_Main.GetFeedbackOnOutline.json
    │   └── 1_Main.GetFeedbackOnOutline.md
    ├── Main.log
    ├── Story.md
    └── Story.json
```

## 3. Enhanced Logging and Tracing Architecture ✅ **UPDATED**

### 3.1. Session-Based Logging ✅ IMPLEMENTED

**Purpose**: Comprehensive session management and logging for story generation.

**Implementation**: `Logger` class in `storytelling/logger.py` and `SessionManager` in `storytelling/session_manager.py`

**Features**:
- ✅ **Session Management**: Unique session IDs and directories for each generation run
- ✅ **Structured Logging**: Console and file-based logging with session context
- ✅ **LLM Interaction Tracing**: Detailed capture of prompts and responses in JSON/Markdown formats
- ✅ **Checkpoint Persistence**: Automatic state preservation at workflow boundaries
- ⏳ **Langfuse Integration** (Planned): Cloud-based tracing and observability

**Current Implementation**:
- Session-based directory structure (`Logs/Generation_{timestamp}/`)
- LLM interaction logging in `LangchainDebug/` subdirectory
- Checkpoint files for session resume capabilities
- Console logging with colored output and progress indicators

### 3.2. Logging Components ✅ IMPLEMENTED

**Console Logging** - Structured output with visual feedback
- Real-time progress updates with timestamps
- Color-coded log levels (INFO, DEBUG, WARNING, ERROR)
- Session information display
- Progress indicators for long-running operations

**Session Log Files** - Comprehensive session artifacts  
- **Main Session Log**: Complete execution record in `Main.log`
- **LLM Interaction Logs**: Detailed prompt/response pairs in `LangchainDebug/`
  - JSON format for machine processing
  - Markdown format for human readability
- **Story Outputs**: Generated narratives in both `Story.json` and `Story.md` formats
- **Checkpoint Files**: Session state preservation for resume capabilities

### 3.3. Future Enhancements ⏳ PLANNED

**Advanced Observability with Langfuse**:
- Cloud-based trace aggregation and analytics
- Multi-run comparison and performance tracking
- Token usage and cost analysis
- Advanced debugging and replay capabilities

**CoAiAPy Integration Option**:
The `coaiapy` package (`pip install coaiapy`) provides a `coaia fuse` command that could enable optional Langfuse tracing at the session level. This would complement the existing Logger class by adding:
- Automatic trace creation for storytelling sessions
- Step-by-step observation tracking (events, spans, generations)
- Internal state observations at workflow boundaries
- Cloud-based trace persistence and analysis

This integration would be optional and configurable, allowing users to enable Langfuse tracing without requiring code changes to the core Logger implementation.

## 4. Final Artifacts

The final generated story and its associated JSON data are the ultimate artifacts of the process and are also part of the traceability record.

-   **Story File (`.md`):** The final, polished story.
-   **Story Data File (`.json`):** The structured JSON object containing the outline, story elements, raw chapters, and final metadata.
-   **Location:** These files should be saved both in the session directory and, optionally, to a user-specified output path.

## 5. Narrative Intelligence Tracing ⏳ PLANNED

When Narrative Intelligence features are enabled (see `Narrative_Aware_Story_Graph_Specification.md`), additional tracing captures the narrative-aware generation process:

### 5.1 NarrativeTracingHandler

**Purpose**: Handle Langfuse tracing for narrative-aware generation.

**Trace Structure**:
```
Story Generation Trace
├── setup_story
│   ├── character_initialization (per character)
│   └── theme_setup
├── generate_beat (repeated)
│   ├── context_building
│   ├── llm_generation
│   └── beat_parsing
├── analyze_beat (repeated)
│   ├── character_analysis
│   ├── emotional_analysis
│   ├── thematic_analysis
│   └── enrichment (if triggered)
├── track_character (repeated)
│   └── arc_point_recording
└── finalize_story
    ├── metrics_calculation
    └── story_compilation
```

### 5.2 Narrative Metrics Captured

- **Beat Quality History**: Quality scores for each generated beat
- **Enrichment Events**: When and how beats were enriched
- **Character Arc Progress**: Arc points recorded per character
- **Gap Analysis Results**: Quality gaps identified and addressed
- **Phase Transitions**: Dramatic phase changes through narrative

See related specifications:
- `Narrative_Intelligence_Integration_Specification.md`
- `Analytical_Feedback_Loop_Specification.md`
- `Character_Arc_Tracking_Specification.md`
