# Storytelling MCP Server

Model Context Protocol (MCP) integration for the Storytelling package. Exposes AI-powered narrative generation as composable MCP tools and resources.

## Overview

The Storytelling MCP Server enables LLM agents and CLI assistants (like Claude, ChatGPT, or GitHub Copilot) to:

- **Generate complete stories** from prompts using advanced orchestration
- **Manage sessions** - list, retrieve info, resume, migrate interrupted generations
- **Configure & validate** - comprehensive configuration reference and validation
- **Setup knowledge bases** - RAG-aware story generation with your documents
- **Choose models wisely** - provider listing and model recommendations
- **Access workflow resources** - understand each stage of story generation
- **Explore advanced features** - translation, IAIP, content checking, debugging

## Installation

### As MCP Server

```bash
# Install storytelling-mcp from PyPI
pip install storytelling-mcp

# Or with all storytelling features
pip install storytelling[all]
```

### Configure for Claude Desktop

Add to `~/.config/claude_app/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "storytelling": {
      "command": "python",
      "args": ["-m", "storytelling_mcp"]
    }
  }
}
```

### Configure for GitHub Copilot

```bash
# Make the server available as a tool
export MCP_STORYTELLING=python://storytelling_mcp.server
```

## Available Tools (16 Total)

### Story Generation (1 tool)

#### `generate_story`

Generate a complete, multi-chapter story from a prompt.

**Parameters:**
- `prompt_file` (required): Path to prompt file containing story concept
- `output_file` (optional): Where to save the generated story (auto-generated if omitted)
- `initial_outline_model`: LLM for initial outline (default: `google://gemini-2.5-flash`)
- `chapter_outline_model`: LLM for chapter planning
- `chapter_s1_model` through `chapter_s4_model`: LLMs for individual scenes
- `chapter_revision_model`: LLM for chapter revision
- `revision_model`: LLM for final story revision
- `knowledge_base_path` (optional): Path to knowledge base for context-aware generation
- `embedding_model` (optional): Embedding model for semantic retrieval
- `expand_outline` (boolean): Whether to expand outline with details (default: true)
- `chapter_max_revisions` (integer): Maximum revisions per chapter (default: 3)
- `debug` (boolean): Enable debug logging

**Returns:** Generation result with status, session ID, and output path

**Example:**
```
generate_story(
  prompt_file="/path/to/prompt.txt",
  output_file="/path/to/story.md",
  initial_outline_model="ollama://mistral@localhost:11434"
)
```

### Session Management (5 tools)

#### `list_sessions`

List all available story generation sessions with their status and metadata.

**Returns:** Table of sessions with IDs, timestamps, and status

#### `get_session_info`

Retrieve detailed information about a specific session.

**Parameters:**
- `session_id` (required): The session ID to query

**Returns:** Full session details including generation state, checkpoints, and history

#### `resume_session`

Resume an interrupted story generation session.

**Parameters:**
- `session_id` (required): Session ID to resume
- `resume_from_node` (optional): Specific LangGraph node to resume from (if omitted, resumes from last checkpoint)

**Returns:** Continuation result and updated story content

#### `migrate_session` (NEW)

Migrate old session format to new format for compatibility.

**Parameters:**
- `session_id` (required): Session ID to migrate

**Returns:** Migration result and success status

### Configuration & Validation (3 tools)

#### `validate_model_uri`

Validate and provide guidance for model URI formats.

**Parameters:**
- `model_uri` (required): URI string to validate (e.g., `google://gemini-2.5-flash`)

**Returns:** Validation result with supported schemes and format examples

**Valid Schemes:**
- `google://` - Google GenAI models (Gemini, PaLM)
- `ollama://` - Local Ollama models (format: `model-name@host:port`)
- `openrouter://` - OpenRouter community models
- `myflowise://` - Custom Flowise endpoints

#### `validate_configuration` (NEW)

Validate storytelling configuration before generation.

**Parameters:**
- `models_config`: Configuration type (default, quality, balanced, custom)
- `knowledge_base_path` (optional): Path to knowledge base directory

**Returns:** Validation results and capability checks

#### `get_config_reference` (NEW)

Get complete configuration parameter reference with examples.

**Returns:** Comprehensive guide to all 30+ configuration parameters with usage examples

### Configuration & Model Selection (2 tools)

#### `list_model_providers` (NEW)

List available LLM providers and their recommended models.

**Returns:** 
- Google Gemini (cloud)
- Ollama (local)
- OpenRouter (community)
- Custom endpoints
Plus model recommendations by use case

#### `suggest_model_combination` (NEW)

Get recommended LLM model combinations for different story types.

**Parameters:**
- `story_type`: Type of story (general, fantasy, scifi, mystery, romance)
- `speed_priority` (boolean): Prioritize speed over quality

**Returns:** Recommended models for each workflow stage with rationale

### Workflow Understanding (2 tools)

#### `describe_workflow`

Get a comprehensive overview of the entire story generation workflow with all 6 stages.

**Returns:** Detailed explanation of each workflow stage, typical duration, and configuration options

#### `get_workflow_stage_info`

Get detailed information about a specific workflow stage.

**Parameters:**
- `stage_name` (required): One of: `story_elements`, `initial_outline`, `chapter_planning`, `scene_generation`, `chapter_revision`, `final_revision`

**Returns:** Stage-specific details including inputs, outputs, duration, and review criteria

**Example Stages:**
- `story_elements` - Analyze prompt and extract story preferences
- `initial_outline` - Create comprehensive story structure
- `chapter_planning` - Break outline into chapters with scenes
- `scene_generation` - Write individual scenes
- `chapter_revision` - Polish chapters for consistency
- `final_revision` - Final story-level polish

### Prompt Guidance & Examples (2 tools)

#### `get_prompt_examples`

Get example story prompts for different genres and best practices.

**Returns:** 4+ example prompts (fantasy, sci-fi, historical, thriller) with guidelines on what works well

**Example Use:**
```
You: "I don't know what prompt to write for a mystery story"
Claude uses: get_prompt_examples()
Claude shows examples and recommends structure
```

### RAG & Knowledge Base (2 tools)

#### `setup_knowledge_base` (NEW)

Initialize and configure knowledge base for RAG-aware story generation.

**Parameters:**
- `kb_path` (required): Path to knowledge base directory
- `embedding_model` (optional): Embedding model type (ollama, sentence-transformers, openai)

**Returns:** Setup guide with configuration examples and next steps

**Example Use:**
```
You: "How do I use my own knowledge base for stories?"
Claude uses: setup_knowledge_base(kb_path="./knowledge_base")
Claude provides setup instructions and configuration examples
```

#### `get_rag_capabilities` (NEW)

Get detailed information about RAG (Retrieval-Augmented Generation) features.

**Returns:**
- Feature overview
- Embedding model options
- Configuration parameters
- Performance considerations
- Troubleshooting guide

### Advanced Features (1 tool)

#### `get_advanced_features` (NEW)

Get information about advanced storytelling features.

**Returns:**
- IAIP (Indigenous AI Integrated Practices) integration
- Content translation capabilities
- Content checking & evaluation
- Debug mode setup
- Mock mode for testing
- Langfuse integration for analytics

## Available Resources (10 total)

Resources provide context and documentation for the storytelling workflow.

### Workflow Stages (5 resources)

#### `storytelling://workflow/initial-outline`
Overview of the initial outline generation stage—the first step transforming a prompt into structured narrative foundation.

#### `storytelling://workflow/chapter-planning`
Details on how outline sections are expanded into individual chapters with dedicated outlines.

#### `storytelling://workflow/scene-generation`
Explanation of per-chapter scene generation—creating 4 distinct, coherent scenes for each chapter.

#### `storytelling://workflow/chapter-revision`
How the system revises completed chapters for internal consistency and narrative flow.

#### `storytelling://workflow/final-revision`
The final story-level revision stage ensuring global coherence and polish.

### Configuration Resources (3 resources)

#### `storytelling://config/model-uris`
Complete guide to specifying model URIs for all supported LLM providers with examples.

#### `storytelling://config/model-providers` (NEW)
List of available LLM providers (Google, Ollama, OpenRouter, custom) with model details and recommendations.

#### `storytelling://prompts/guide` (NEW)
Guidelines and best practices for writing effective story prompts.

### Advanced Features Resources (2 resources)

#### `storytelling://features/rag` (NEW)
Knowledge base and retrieval-augmented generation setup guide.

#### `storytelling://features/advanced` (NEW)
Documentation on IAIP, translation, content checking, debugging, and logging features.

## Usage Examples

### Generate a Story via Claude

```
You: "Generate a mystery story about a hidden library using the storytelling tools"

Claude uses: generate_story(
  prompt_file="/tmp/mystery_prompt.txt",
  initial_outline_model="google://gemini-2.5-flash"
)
```

### Get Workflow Information

```
You: "How does the storytelling system work?"

Claude uses: describe_workflow()

Claude explains the 6 stages and their purposes
```

### Understand a Specific Stage

```
You: "Tell me about the scene generation stage"

Claude uses: get_workflow_stage_info(stage_name="scene_generation")

Claude explains inputs, outputs, and typical duration
```

### Get Prompt Ideas

```
You: "I want to write a mystery story but don't know what to prompt"

Claude uses: get_prompt_examples()

Claude shows 4 examples and explains what works well
```

### Find Optimal Models for Your Story

```
You: "I'm writing a fantasy story and want it done quickly"

Claude uses: suggest_model_combination(story_type="fantasy", speed_priority=true)

Claude recommends: Flash for all stages (fast) with reasoning
```

### Resume an Interrupted Session

```
You: "What sessions do I have?"

Claude uses: list_sessions()

Claude uses: resume_session(session_id="xyz-123")
```

### Validate Configuration

```
You: "Can I use ollama://llama2@localhost:11434?"

Claude uses: validate_model_uri(model_uri="ollama://llama2@localhost:11434")
```

## Architecture

### Server Implementation

- **Framework**: Python MCP SDK
- **Location**: `mcp/server.py`
- **Entry Point**: `mcp/__init__.py`

### Integration Points

The MCP server bridges these components:

- **storytelling.cli**: CLI command execution
- **storytelling.session_manager**: Session state and checkpoints
- **storytelling.graph**: LangGraph workflow orchestration
- **storytelling.config**: Configuration and validation
- **storytelling.llm_providers**: Model URI parsing and provider selection

### Tool Registration Flow

1. `create_server()` - Initializes MCP Server
2. `register_*_tools()` - Registers tool functions (generation, sessions, config, workflows, prompts)
3. Tools leverage subprocess to call `storytelling` CLI
4. Results returned as TextContent MCP types

## Configuration

### Environment Variables

```bash
# LLM Provider credentials
GOOGLE_API_KEY=...
OPENAI_API_KEY=...

# Ollama endpoint (if using local models)
OLLAMA_BASE_URL=http://localhost:11434

# Optional: Langfuse integration for tracing
LANGFUSE_PUBLIC_KEY=...
LANGFUSE_SECRET_KEY=...
LANGFUSE_HOST=...

# Optional: Knowledge base
KB_PATH=/path/to/knowledge/base
```

### Runtime Configuration

Tools accept model URIs that override defaults:

```
generate_story(
  prompt_file="story.txt",
  initial_outline_model="ollama://neural-chat@localhost:11434",
  revision_model="google://gemini-pro"
)
```

## Extending the MCP Server

### Adding New Tools

Edit `mcp/server.py`:

```python
def register_custom_tools(server: Server) -> None:
    @server.call_tool()
    async def my_custom_tool(param: str) -> list[TextContent]:
        # Implementation
        return [TextContent(type="text", text="result")]
    
    server.register_tool(
        Tool(
            name="my_custom_tool",
            description="What this tool does",
            inputSchema={...}
        ),
        my_custom_tool,
    )
```

Then add the registration in `create_server()`:

```python
register_custom_tools(server)
```

### Adding Resources

```python
def register_custom_resources(server: Server) -> None:
    resource = Resource(
        uri="storytelling://custom/resource",
        name="Resource Name",
        description="What this provides",
        mimeType="text/markdown",
    )
    server.register_resource(resource)
```

## Troubleshooting

### Server Won't Start

```bash
# Check if storytelling CLI is installed
storytelling --help

# Verify Python version (3.9+)
python --version

# Check MCP dependencies
python -c "from mcp.server import Server; print('MCP OK')"
```

### Tools Return Errors

- Ensure `storytelling` command is in PATH
- Check LLM provider credentials in environment
- Verify model URIs match supported schemes
- Enable debug logging: `debug=true` in tool parameters

### Session Resume Fails

- Verify session ID with `list_sessions()`
- Check session storage directory has correct permissions
- Ensure checkpoint files haven't been deleted
- Review logs in `.storytelling/logs/`

## Performance Considerations

### Typical Generation Times

- **Initial Outline**: 2-5 minutes
- **Chapter Planning**: 1-3 minutes per chapter
- **Scene Generation**: 3-5 minutes per scene (4 per chapter)
- **Revision Stages**: 2-4 minutes per stage

Total for a 3-chapter story: 30-60 minutes depending on model complexity.

### Optimization Tips

1. Use faster models for intermediate stages (e.g., `gemini-flash` vs `gemini-pro`)
2. Disable `chapter_max_revisions` for faster generation
3. Disable `expand_outline` for leaner outputs
4. Use local Ollama models to avoid API latency

## Security Notes

- Never commit API keys to version control
- Use environment variables or `.env` files (add to `.gitignore`)
- MCP server runs with same permissions as calling process
- Validate file paths to prevent directory traversal
- Respect rate limits of LLM providers

## Related Documentation

- **Main README**: [`../README.md`](../README.md)
- **Project Specifications**: [`../rispecs/`](../rispecs/)
- **RISE Framework**: [`../rispecs/RISE_Spec.md`](../rispecs/RISE_Spec.md)
- **Configuration Options**: [`../rispecs/Configuration.md`](../rispecs/Configuration.md)
- **LLM Providers**: [`../rispecs/LLM_Provider_Specification.md`](../rispecs/LLM_Provider_Specification.md)
- **CLI Reference**: See `storytelling --help`
