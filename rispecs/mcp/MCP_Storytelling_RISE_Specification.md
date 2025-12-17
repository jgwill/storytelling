# MCP Storytelling - RISE Specification

**Document Status**: Active Specification
**Version**: 0.1.0
**Framework**: RISE (Reverse-Engineering, Intent, Specifications, Exportation)
**Date**: December 17, 2025

---

## 1. REVERSE-ENGINEERING: What Does This Do?

### 1.1 Core Purpose

`mcp-storytelling` wraps the storytelling Python package as a Model Context Protocol (MCP) server, enabling LLMs to:
- **Orchestrate** multi-stage story generation workflows
- **Manage** narrative sessions with checkpoint/resume capabilities
- **Configure** LLM models across 9 generation stages (outline → 4-scene chapters → revisions)
- **Access** workflow metadata and configuration guidance

### 1.2 System Architecture

```
User/LLM Agent
    ↓
MCP Client (Claude, etc.)
    ↓
MCP Server: mcp-storytelling
    ├── Tool Layer: Story generation commands
    ├── Resource Layer: Workflow stages & config guides
    └── Backend: storytelling CLI (subprocess execution)
    ↓
storytelling Package (WillWrite)
    ├── Config validation (WillWriteConfig)
    ├── Session management (LangGraph)
    ├── RAG pipeline (FAISS + knowledge base)
    └── LLM provider routing (Google/Ollama/OpenRouter)
    ↓
Model URIs: google://gemini-2.5-flash | ollama://model | openrouter://model
```

### 1.3 Workflow Stages

The storytelling system generates narratives through 5 distinct phases:

1. **Initial Outline** - Produces story structure from prompt
2. **Chapter Planning** - Breaks outline into chapters
3. **Scene Generation** - Creates 4 scenes per chapter (s1, s2, s3, s4)
4. **Chapter Revision** - Polishes each chapter (configurable iterations)
5. **Final Revision** - Story-level coherence pass

---

## 2. INTENT: Why This Design?

### 2.1 Creative Orientation vs Problem-Solving

**Design Intent**: Enable LLMs to become creative orchestrators, not task-checkers.

- **NOT**: "Execute step 1, then step 2..." (linear problem-solving)
- **YES**: "Here are narrative generation capabilities. What story should we create?" (creative agency)

The MCP respects user autonomy while providing infrastructure for sophisticated workflows.

### 2.2 Model URI Abstraction

**Design Intent**: Decouple model selection from workflow logic.

```
Drawback of: --model=gemini-2.5-flash
Problem: Tightly couples to specific provider, no flexibility

Benefit of: --initial-outline-model=google://gemini-2.5-flash
Solution: URI scheme allows easy model swapping:
  - google://gemini-pro
  - ollama://qwen@localhost:11434
  - openrouter://openai/gpt-4
```

### 2.3 Session Management

**Design Intent**: Support interrupted workflows in complex creative projects.

- Large stories may take hours or days
- Network interruptions, resource constraints are real
- Sessions enable:
  - Checkpoint at each stage
  - Resume from specific node
  - Preserve context and partial outputs
  - Progress inspection

### 2.4 RAG Integration

**Design Intent**: Ground narrative generation in domain knowledge.

Optional knowledge base integration allows:
- Story generation informed by source materials
- Consistent world-building from reference docs
- Automated consistency checking

---

## 3. SPECIFICATIONS: What Are the APIs?

### 3.1 Tools

#### Tool: `generate_story`

**Purpose**: Initiate complete story generation workflow.

**Parameters**:
```
prompt_file (string, required)
  The starting prompt/creative brief for story generation
  - Can be markdown with narrative direction
  - Can include character descriptions, plot seeds, world-building notes

output_file (string, optional)
  Where to save the generated story
  Auto-generates timestamped filename if omitted

Model Selection (all optional, default: google://gemini-2.5-flash):
  initial_outline_model
    - First outline generation from prompt
  chapter_outline_model
    - Individual chapter planning
  chapter_s1_model, chapter_s2_model, chapter_s3_model, chapter_s4_model
    - 4 scenes per chapter (Act 1, 2, 3, climax/resolution)
  chapter_revision_model
    - Per-chapter revision and polish
  revision_model
    - Final story-level revision

knowledge_base_path (string, optional)
  Directory containing markdown files for RAG context
  - Files automatically indexed and embedded
  - Context injected into outline generation stage

embedding_model (string, optional)
  Model for creating embeddings (required if using knowledge_base_path)
  - Default uses local embedding if available
  - Can be: "sentence-transformers/all-MiniLM-L6-v2" or similar

expand_outline (boolean, default: true)
  Whether to expand outline with more granular chapter details

chapter_max_revisions (integer, default: 3)
  Maximum revision iterations per chapter (quality vs speed tradeoff)

debug (boolean, default: false)
  Enable verbose logging and intermediate output inspection
```

**Returns**:
```
TextContent with:
- Success: ✓ Story generation completed
  - Session ID for resumption
  - Output file location
  - Generation summary

- Failure: ✗ Generation failed
  - Error details
  - Stderr from storytelling process
```

**Model URI Format Examples**:
```
google://gemini-2.5-flash           ✓ Google Gemini
google://gemini-pro                 ✓ Alternative Google model
ollama://qwen@localhost:11434       ✓ Local Ollama
ollama://llama2@gpu-server:11434    ✓ Remote Ollama
openrouter://openai/gpt-4           ✓ OpenRouter proxy
openrouter://anthropic/claude-opus  ✓ Different providers
```

**Example Usage**:
```
Tool: generate_story
Args:
  prompt_file: "/stories/the-keeper-chronicles/PROMPT_001.md"
  output_file: "/stories/generated/keeper_001_INITIATION.md"
  initial_outline_model: "google://gemini-2.5-flash"
  chapter_outline_model: "google://gemini-2.5-flash"
  chapter_s1_model: "google://gemini-2.5-flash"
  chapter_s2_model: "google://gemini-2.5-flash"
  chapter_s3_model: "google://gemini-2.5-flash"
  chapter_s4_model: "google://gemini-2.5-flash"
  chapter_revision_model: "google://gemini-2.5-flash"
  revision_model: "google://gemini-2.5-flash"
  chapter_max_revisions: 3
```

---

#### Tool: `list_sessions`

**Purpose**: View all available story generation sessions.

**Parameters**: None

**Returns**: Formatted list of sessions with:
- Session ID
- Creation timestamp
- Current status (completed, in_progress, failed, interrupted)
- Associated prompt file
- Number of checkpoints
- Last checkpoint node

**Example Output**:
```
✅ session-2025-12-17-001
   Created: 2025-12-17 16:30:00
   Status: completed
   Prompt: /stories/PROMPT_001.md
   Checkpoints: 5
   Last checkpoint: revision_stage

🔄 session-2025-12-17-002
   Created: 2025-12-17 17:45:00
   Status: in_progress
   Prompt: /stories/PROMPT_002.md
   Checkpoints: 3
   Last checkpoint: chapter_generation_s2
```

---

#### Tool: `get_session_info`

**Purpose**: Inspect detailed information about specific session.

**Parameters**:
```
session_id (string, required)
  Session identifier from list_sessions output
```

**Returns**:
- Full session metadata
- Complete checkpoint timeline
- Suggested resume point
- Resource usage (if available)

---

#### Tool: `resume_session`

**Purpose**: Continue interrupted story generation.

**Parameters**:
```
session_id (string, required)
  Session to resume

resume_from_node (string, optional)
  Specific workflow node to resume from
  - If omitted, auto-detects best resume point
  - Useful for: retrying failed nodes, skipping stages
```

**Returns**: Same format as `generate_story`

**Example**:
```
Tool: resume_session
Args:
  session_id: "session-2025-12-17-002"
  # Automatically resumes from last checkpoint

OR

Args:
  session_id: "session-2025-12-17-002"
  resume_from_node: "chapter_revision_stage"
  # Skips to specific node (useful if fixing model config)
```

---

#### Tool: `validate_model_uri`

**Purpose**: Verify model URI format before executing large generations.

**Parameters**:
```
model_uri (string, required)
  The URI to validate
```

**Returns**:
```
✓ Valid model URI: google://gemini-2.5-flash

✗ Invalid scheme 'azure'. Valid schemes:
  - google://gemini-2.5-flash
  - ollama://model@localhost:11434
  - openrouter://model-name
```

---

### 3.2 Resources

#### Resource: `storytelling://workflow/initial-outline`

**Type**: Text / Markdown
**Purpose**: Documentation of initial outline stage

Contains:
- What happens: Prompt → Story structure
- Model context injected
- Output format example
- Quality indicators

---

#### Resource: `storytelling://workflow/chapter-planning`

**Type**: Text / Markdown
**Purpose**: Documentation of chapter planning stage

---

#### Resource: `storytelling://workflow/scene-generation`

**Type**: Text / Markdown
**Purpose**: Documentation of 4-scene chapter generation stage

---

#### Resource: `storytelling://workflow/chapter-revision`

**Type**: Text / Markdown
**Purpose**: Documentation of chapter-level revision stage

---

#### Resource: `storytelling://workflow/final-revision`

**Type**: Text / Markdown
**Purpose**: Documentation of story-level final revision stage

---

#### Resource: `storytelling://config/model-uris`

**Type**: Text / Markdown
**Purpose**: Complete guide for model URI specification

Contains:
- Supported schemes (google, ollama, openrouter)
- URI format specification
- Provider-specific configuration
- Example URIs for each provider
- Troubleshooting URI issues

---

### 3.3 Prompts

None currently registered. Reserved for future LLM instruction templates.

---

## 4. EXPORTATION: How to Use This?

### 4.1 Installation

```bash
# Option 1: From source
git clone https://github.com/jgwill/storytelling.git
cd storytelling
pip install -e ".[mcp]"

# Option 2: As standalone MCP
pip install mcp-storytelling
```

### 4.2 MCP Server Configuration

Add to Claude or other MCP client config:

```json
{
  "mcpServers": {
    "storytelling": {
      "command": "python",
      "args": ["-m", "storytelling.mcp.server"]
    }
  }
}
```

### 4.3 Basic Workflow: Generate a Story

```
User: "I want to generate the first act of The Keeper Chronicles"

Claude (using MCP):
  1. Tool: generate_story
     - prompt_file: ".../PROMPT_001_THE_INITIATION.md"
     - all models: google://gemini-2.5-flash
     - output_file: ".../generated/KEEPER_001.md"

  2. Monitors execution
     - Polls session status
     - Reports progress
     - Handles interruptions

Result: Full story generated in .../generated/KEEPER_001.md
```

### 4.4 Advanced Workflow: Session Checkpoint & Resume

```
Scenario: Generation interrupted midway

Step 1: Original generation started
  Tool: generate_story (... config ...)
  Session created: "session-2025-12-17-abc123"
  Generation runs for 1 hour...
  Network failure during chapter revision

Step 2: Check what happened
  Tool: list_sessions
  → Shows "session-2025-12-17-abc123" status: interrupted

Step 3: Inspect session
  Tool: get_session_info
  Args: session_id="session-2025-12-17-abc123"
  → Shows: Last completed node was scene_generation_s4 of chapter 3

Step 4: Resume from checkpoint
  Tool: resume_session
  Args: session_id="session-2025-12-17-abc123"
  → Resumes chapter revision stage with existing chapter data

Result: Story completed without losing progress
```

### 4.5 Advanced Workflow: Mixed Model Configuration

```
Use case: Different models for different stages
(Outline with slow, powerful model; scenes with faster model)

Tool: generate_story
Args:
  prompt_file: "..."
  initial_outline_model: "google://gemini-2.5-flash"  # Best quality
  chapter_outline_model: "google://gemini-2.5-flash"
  chapter_s1_model: "ollama://qwen@localhost:11434"   # Faster, local
  chapter_s2_model: "ollama://qwen@localhost:11434"
  chapter_s3_model: "ollama://qwen@localhost:11434"
  chapter_s4_model: "ollama://qwen@localhost:11434"
  chapter_revision_model: "google://gemini-2.5-flash" # Quality
  revision_model: "google://gemini-2.5-flash"

Result: Balanced quality and speed
- Outlines: Google's best reasoning
- Scenes: Local fast generation
- Revisions: Google quality polish
```

### 4.6 Advanced Workflow: Knowledge-Base Grounded Generation

```
Use case: World-building consistency from reference materials

Setup:
  Create directory with world-building docs:
    /stories/keeper-knowledge/
      ├── world-setting.md
      ├── character-profiles.md
      ├── mythology.md
      └── historical-context.md

Tool: generate_story
Args:
  prompt_file: "PROMPT_001.md"
  knowledge_base_path: "/stories/keeper-knowledge"
  embedding_model: "sentence-transformers/all-MiniLM-L6-v2"

Effect:
  - Outline stage retrieves relevant docs
  - Context injected into LLM prompts
  - Scenes generated consistent with source material
  - Character voices aligned with profiles
```

---

## 5. EXTENSIBILITY & FUTURE

### 5.1 Potential Extensions

**Tool Expansion**:
- `analyze_story_quality` - Evaluate generated story
- `extract_story_metadata` - Parse characters, themes, timeline
- `transform_story_format` - Convert to different narrative structures
- `collaborative_editing` - Multi-author story development

**Resource Expansion**:
- Prompt templates per genre (fantasy, sci-fi, romance)
- Character archetype libraries
- World-building ontologies
- Narrative structure patterns

**Integration Possibilities**:
- Langfuse tracing (full generation telemetry)
- Vector DB persistence (long-term context)
- Multi-agent orchestration (editors, critics, collaborators)
- Publishing pipeline (docx, epub, print-ready formats)

### 5.2 Integration with Two-Eyed Seeing

This MCP is designed as a bridge between:
- **Western lens**: Computational efficiency, automation, system optimization
- **Indigenous lens**: Narrative as ceremony, stories as living entities, creative agency

The MCP should never force rigid workflows. It provides infrastructure while respecting:
- Natural story rhythms
- Creative intuition over metrics
- Relationship to narrative as sacred

---

## 6. QUALITY & VALIDATION

### 6.1 Testing Strategy

```
Unit Tests:
  - Model URI validation
  - Tool parameter parsing
  - Session state transitions

Integration Tests:
  - Full generation workflow
  - Session checkpoint/resume cycle
  - Knowledge base RAG injection
  - Multi-model configuration

User Acceptance:
  - Generate test stories with each model combo
  - Verify checkpoint integrity
  - Test interruption recovery
```

### 6.2 Known Limitations

- **Timeout**: 1 hour max generation (configurable)
- **Model Availability**: Requires valid API keys or local Ollama
- **Knowledge Base**: Currently FAISS (CPU) - GPU variant available
- **Concurrency**: Single MCP server, sequential generations

---

## 7. OPERATIONAL NOTES

### 7.1 Troubleshooting

**"Invalid scheme" error**:
- Check model URI format
- Tool: `validate_model_uri` to verify

**"Model not found"**:
- Verify Google API key (if using google://)
- Check Ollama is running (if using ollama://)
- Verify OpenRouter token (if using openrouter://)

**Session stuck in "in_progress"**:
- Check logs: `storytelling --session-info SESSION_ID`
- Manual recovery: `storytelling --resume SESSION_ID`

### 7.2 Performance Optimization

For faster generation:
- Use local Ollama model instead of cloud API
- Reduce `chapter_max_revisions` (default: 3, try 1-2)
- Disable `expand_outline` if not needed
- Omit `knowledge_base_path` for speed

For better quality:
- Increase `chapter_max_revisions` to 5+
- Use Google Gemini for all stages
- Enable `expand_outline`
- Provide rich `knowledge_base_path`

---

## END OF SPECIFICATION

**Last Updated**: December 17, 2025
**Maintainer**: jgwill/storytelling
**Repository**: https://github.com/jgwill/storytelling
