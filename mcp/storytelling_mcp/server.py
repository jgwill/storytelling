"""
MCP Server implementation for Storytelling package.

Exposes storytelling workflow as MCP tools and resources.
"""

import asyncio
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

from mcp.server import Server
from mcp.types import (
    Resource,
    Tool,
    TextContent,
    CallToolResult,
)


def create_server() -> Server:
    """Create and configure the Storytelling MCP Server."""
    server = Server("mcp-storytelling")

    # Register tools
    register_story_generation_tools(server)
    register_session_management_tools(server)
    register_configuration_tools(server)
    register_workflow_insight_tools(server)
    register_prompt_template_tools(server)
    register_advanced_features_tools(server)
    register_rag_tools(server)
    register_config_reference_tools(server)

    # Register resources
    register_workflow_resources(server)
    register_configuration_resources(server)
    register_prompt_resources(server)
    register_advanced_resources(server)

    return server


def register_story_generation_tools(server: Server) -> None:
    """Register story generation workflow tools."""

    @server.call_tool()
    async def generate_story(
        prompt_file: str,
        output_file: str | None = None,
        initial_outline_model: str = "google://gemini-2.5-flash",
        chapter_outline_model: str = "google://gemini-2.5-flash",
        chapter_s1_model: str = "google://gemini-2.5-flash",
        chapter_s2_model: str = "google://gemini-2.5-flash",
        chapter_s3_model: str = "google://gemini-2.5-flash",
        chapter_s4_model: str = "google://gemini-2.5-flash",
        chapter_revision_model: str = "google://gemini-2.5-flash",
        revision_model: str = "google://gemini-2.5-flash",
        knowledge_base_path: str | None = None,
        embedding_model: str | None = None,
        expand_outline: bool = True,
        chapter_max_revisions: int = 3,
        debug: bool = False,
    ) -> list[TextContent]:
        """
        Generate a story using the storytelling package.

        Args:
            prompt_file: Path to the prompt file (required)
            output_file: Output file path (optional, auto-generated if not provided)
            initial_outline_model: Model URI for initial outline
            chapter_outline_model: Model URI for chapter outline
            chapter_s1_model: Model URI for scene 1
            chapter_s2_model: Model URI for scene 2
            chapter_s3_model: Model URI for scene 3
            chapter_s4_model: Model URI for scene 4
            chapter_revision_model: Model URI for chapter revision
            revision_model: Model URI for story revision
            knowledge_base_path: Path to knowledge base (for RAG)
            embedding_model: Embedding model for RAG
            expand_outline: Whether to expand outline
            chapter_max_revisions: Max revisions per chapter
            debug: Enable debug mode

        Returns:
            Generation result with session ID and output file path
        """
        args = [
            "storytelling",
            "--prompt", prompt_file,
            "--initial-outline-model", initial_outline_model,
            "--chapter-outline-model", chapter_outline_model,
            "--chapter-s1-model", chapter_s1_model,
            "--chapter-s2-model", chapter_s2_model,
            "--chapter-s3-model", chapter_s3_model,
            "--chapter-s4-model", chapter_s4_model,
            "--chapter-revision-model", chapter_revision_model,
            "--revision-model", revision_model,
            "--chapter-max-revisions", str(chapter_max_revisions),
        ]

        if output_file:
            args.extend(["--output", output_file])

        if knowledge_base_path:
            args.extend(["--knowledge-base-path", knowledge_base_path])

        if embedding_model:
            args.extend(["--embedding-model", embedding_model])

        if expand_outline:
            args.append("--expand-outline")

        if debug:
            args.append("--debug")

        try:
            result = subprocess.run(
                args,
                capture_output=True,
                text=True,
                timeout=3600,  # 1 hour timeout
            )

            if result.returncode == 0:
                return [TextContent(
                    type="text",
                    text=f"✓ Story generation completed successfully\n\nStdout:\n{result.stdout}",
                )]
            else:
                return [TextContent(
                    type="text",
                    text=f"✗ Story generation failed with return code {result.returncode}\n\nStderr:\n{result.stderr}",
                )]
        except subprocess.TimeoutExpired:
            return [TextContent(
                type="text",
                text="✗ Story generation timed out (exceeded 1 hour)",
            )]
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"✗ Error running storytelling: {e}",
            )]

    server.register_tool(
        Tool(
            name="generate_story",
            description="Generate a complete story with the storytelling package using RISE framework",
            inputSchema={
                "type": "object",
                "properties": {
                    "prompt_file": {"type": "string", "description": "Path to prompt file"},
                    "output_file": {"type": "string", "description": "Output file path (optional)"},
                    "initial_outline_model": {"type": "string", "description": "Model URI for initial outline"},
                    "chapter_outline_model": {"type": "string", "description": "Model URI for chapter outline"},
                    "chapter_s1_model": {"type": "string", "description": "Model URI for scene 1"},
                    "chapter_s2_model": {"type": "string", "description": "Model URI for scene 2"},
                    "chapter_s3_model": {"type": "string", "description": "Model URI for scene 3"},
                    "chapter_s4_model": {"type": "string", "description": "Model URI for scene 4"},
                    "chapter_revision_model": {"type": "string", "description": "Model URI for chapter revision"},
                    "revision_model": {"type": "string", "description": "Model URI for story revision"},
                    "knowledge_base_path": {"type": "string", "description": "Path to knowledge base"},
                    "embedding_model": {"type": "string", "description": "Embedding model for RAG"},
                    "expand_outline": {"type": "boolean", "description": "Expand outline"},
                    "chapter_max_revisions": {"type": "integer", "description": "Max revisions per chapter"},
                    "debug": {"type": "boolean", "description": "Enable debug mode"},
                },
                "required": ["prompt_file"],
            }
        ),
        generate_story,
    )


def register_session_management_tools(server: Server) -> None:
    """Register session management tools."""

    @server.call_tool()
    async def list_sessions() -> list[TextContent]:
        """List all available sessions."""
        try:
            result = subprocess.run(
                ["storytelling", "--list-sessions"],
                capture_output=True,
                text=True,
                timeout=30,
            )
            return [TextContent(type="text", text=result.stdout or result.stderr)]
        except Exception as e:
            return [TextContent(type="text", text=f"Error listing sessions: {e}")]

    @server.call_tool()
    async def get_session_info(session_id: str) -> list[TextContent]:
        """Get information about a specific session."""
        try:
            result = subprocess.run(
                ["storytelling", "--session-info", session_id],
                capture_output=True,
                text=True,
                timeout=30,
            )
            return [TextContent(type="text", text=result.stdout or result.stderr)]
        except Exception as e:
            return [TextContent(type="text", text=f"Error getting session info: {e}")]

    @server.call_tool()
    async def resume_session(session_id: str, resume_from_node: str | None = None) -> list[TextContent]:
        """Resume a story generation session."""
        args = ["storytelling", "--resume", session_id]
        if resume_from_node:
            args.extend(["--resume-from-node", resume_from_node])

        try:
            result = subprocess.run(
                args,
                capture_output=True,
                text=True,
                timeout=3600,
            )
            return [TextContent(type="text", text=result.stdout or result.stderr)]
        except Exception as e:
            return [TextContent(type="text", text=f"Error resuming session: {e}")]

    server.register_tool(
        Tool(
            name="list_sessions",
            description="List all available story generation sessions",
            inputSchema={"type": "object", "properties": {}}
        ),
        list_sessions,
    )

    server.register_tool(
        Tool(
            name="get_session_info",
            description="Get detailed information about a specific session",
            inputSchema={
                "type": "object",
                "properties": {"session_id": {"type": "string", "description": "Session ID"}},
                "required": ["session_id"],
            }
        ),
        get_session_info,
    )

    server.register_tool(
        Tool(
            name="resume_session",
            description="Resume an interrupted story generation session",
            inputSchema={
                "type": "object",
                "properties": {
                    "session_id": {"type": "string", "description": "Session ID"},
                    "resume_from_node": {"type": "string", "description": "Node to resume from (optional)"},
                },
                "required": ["session_id"],
            }
        ),
        resume_session,
    )


def register_configuration_tools(server: Server) -> None:
    """Register configuration and validation tools."""

    @server.call_tool()
    async def validate_model_uri(model_uri: str) -> list[TextContent]:
        """Validate a model URI format."""
        valid_schemes = ["google", "ollama", "openrouter", "myflowise"]

        try:
            scheme = model_uri.split("://")[0]
            if scheme not in valid_schemes:
                return [TextContent(
                    type="text",
                    text=f"✗ Invalid scheme '{scheme}'. Valid schemes: {', '.join(valid_schemes)}"
                )]

            return [TextContent(
                type="text",
                text=f"✓ Valid model URI: {model_uri}\n\nSupported schemes:\n" +
                     f"  - google://gemini-2.5-flash\n" +
                     f"  - ollama://model-name@localhost:11434\n" +
                     f"  - openrouter://model-name"
            )]
        except Exception as e:
            return [TextContent(type="text", text=f"✗ Error validating URI: {e}")]

    server.register_tool(
        Tool(
            name="validate_model_uri",
            description="Validate a model URI format for use with storytelling",
            inputSchema={
                "type": "object",
                "properties": {"model_uri": {"type": "string", "description": "Model URI to validate"}},
                "required": ["model_uri"],
            }
        ),
        validate_model_uri,
    )


def register_workflow_resources(server: Server) -> None:
    """Register workflow stage resources."""

    workflow_stages = {
        "initial_outline": Resource(
            uri="storytelling://workflow/initial-outline",
            name="Initial Outline Generation",
            description="First stage: Generates the overall story outline from the prompt",
            mimeType="text/markdown",
        ),
        "chapter_planning": Resource(
            uri="storytelling://workflow/chapter-planning",
            name="Chapter Planning",
            description="Second stage: Breaks down outline into individual chapters",
            mimeType="text/markdown",
        ),
        "scene_generation": Resource(
            uri="storytelling://workflow/scene-generation",
            name="Scene Generation",
            description="Third stage: Generates 4 scenes per chapter (s1, s2, s3, s4)",
            mimeType="text/markdown",
        ),
        "chapter_revision": Resource(
            uri="storytelling://workflow/chapter-revision",
            name="Chapter Revision",
            description="Fourth stage: Revises completed chapters for coherence",
            mimeType="text/markdown",
        ),
        "final_revision": Resource(
            uri="storytelling://workflow/final-revision",
            name="Final Story Revision",
            description="Fifth stage: Final story-level revision and polish",
            mimeType="text/markdown",
        ),
    }

    for stage_key, resource in workflow_stages.items():
        server.register_resource(resource)


def register_configuration_resources(server: Server) -> None:
    """Register configuration and help resources."""

    model_uri_guide = Resource(
        uri="storytelling://config/model-uris",
        name="Model URI Format Guide",
        description="Guide for specifying model URIs in storytelling commands",
        mimeType="text/markdown",
    )

    server.register_resource(model_uri_guide)


def register_workflow_insight_tools(server: Server) -> None:
    """Register tools for understanding workflow and story structure."""

    @server.call_tool()
    async def describe_workflow() -> list[TextContent]:
        """Describe the complete story generation workflow and stages."""
        description = """# Storytelling Workflow

The storytelling system generates narratives through 6 major stages:

## 1. Story Elements Extraction
- Analyzes the user's prompt
- Identifies genre, theme, pacing, and style preferences
- Extracts important contextual information

## 2. Initial Outline Generation
- Creates comprehensive story outline with:
  - Story title and premise
  - Main characters with details
  - Plot structure (setup, conflict, climax, resolution)
  - Thematic elements
  - Chapter breakdown

## 3. Chapter Planning
- Breaks down outline into individual chapters
- For each chapter:
  - Creates detailed chapter outline
  - Plans 4 scenes with progression

## 4. Scene Generation
- Generates 4 scenes per chapter:
  - Scene 1: Establish/Introduce
  - Scene 2: Develop/Complicate
  - Scene 3: Intensify/Escalate
  - Scene 4: Resolve/Transition
- Each scene is 500-1000 words of polished prose

## 5. Chapter Revision (Up to 3 passes)
- Revises chapter for:
  - Internal consistency
  - Character coherence
  - Pacing and flow
  - Narrative continuity

## 6. Final Story Revision
- Story-level polish:
  - Global consistency checks
  - Thematic coherence
  - Narrative arc verification
  - Final prose refinement

## Configuration for Each Stage

Each stage can use different LLM models:
- Faster models (e.g., gemini-flash) for planning stages
- More capable models (e.g., gemini-pro) for prose generation
- Specialized models for revision tasks

## Session Management

Any stage can be interrupted and resumed:
- State is checkpointed after each stage
- Resume from any point with `resume_session`
- Full history maintained for recovery
"""
        return [TextContent(type="text", text=description)]

    @server.call_tool()
    async def get_workflow_stage_info(stage_name: str) -> list[TextContent]:
        """Get detailed information about a specific workflow stage."""
        stage_details = {
            "story_elements": """# Story Elements Stage

Extracts and structures information from the user's story prompt.

**Input**: Raw user prompt
**Output**: Structured story elements (genre, theme, pacing, style)

**Why This Matters**:
- Sets the tone for all subsequent generation
- Ensures the story remains true to user's vision
- Guides model selection for each stage

**Typical Duration**: 1-2 minutes
""",
            "initial_outline": """# Initial Outline Generation

Creates the foundational story structure from the prompt and story elements.

**Input**: Story elements, user prompt, optional knowledge base context
**Output**: Complete story outline including title, premise, characters, plot points

**Key Components**:
- Story title and tagline
- Protagonist and antagonist profiles
- Plot structure breakdown
- Thematic core
- Chapter-level summaries

**Typical Duration**: 2-5 minutes
""",
            "chapter_planning": """# Chapter Planning

Breaks down the story outline into individual chapters with detailed plans.

**Input**: Story outline
**Output**: Per-chapter outlines with 4-scene structure

**For Each Chapter**:
- Chapter number and title
- Chapter goal and arc
- Scene structure plan
- Key plot points and character moments

**Typical Duration**: 1-2 minutes per chapter
""",
            "scene_generation": """# Scene Generation

Generates polished prose for individual scenes.

**Input**: Chapter outline, scene specifications
**Output**: 4 complete scenes per chapter (500-1000 words each)

**Scene Types**:
- Scene 1: Establish/Introduce scene elements
- Scene 2: Develop conflict or complication
- Scene 3: Intensify drama or tension
- Scene 4: Resolve or transition forward

**Typical Duration**: 3-5 minutes per chapter (4 scenes)
""",
            "chapter_revision": """# Chapter Revision

Refines completed chapters for consistency and quality.

**Input**: Generated chapter
**Output**: Revised chapter with improved prose and coherence

**Review Criteria**:
- Internal consistency
- Character voice consistency
- Pacing and rhythm
- Dialogue quality
- Narrative flow

**Typical Duration**: 2-4 minutes per chapter
**Iterations**: Up to 3 revision passes (configurable)
""",
            "final_revision": """# Final Story Revision

Polish-pass over complete story.

**Input**: Complete revised story
**Output**: Final polished narrative

**Global Checks**:
- Cross-chapter consistency
- Character arc coherence
- Thematic development
- Plot resolution satisfaction
- Prose polish and style

**Typical Duration**: 3-5 minutes
""",
        }

        stage_name_lower = stage_name.lower()
        info = stage_details.get(
            stage_name_lower,
            f"Stage '{stage_name}' not recognized. Try: story_elements, initial_outline, chapter_planning, scene_generation, chapter_revision, final_revision"
        )
        return [TextContent(type="text", text=info)]

    server.register_tool(
        Tool(
            name="describe_workflow",
            description="Get overview of the complete story generation workflow",
            inputSchema={"type": "object", "properties": {}}
        ),
        describe_workflow,
    )

    server.register_tool(
        Tool(
            name="get_workflow_stage_info",
            description="Get detailed information about a specific workflow stage",
            inputSchema={
                "type": "object",
                "properties": {
                    "stage_name": {
                        "type": "string",
                        "description": "Stage name: story_elements, initial_outline, chapter_planning, scene_generation, chapter_revision, final_revision"
                    }
                },
                "required": ["stage_name"],
            }
        ),
        get_workflow_stage_info,
    )


def register_prompt_template_tools(server: Server) -> None:
    """Register tools for working with prompt templates and examples."""

    @server.call_tool()
    async def get_prompt_examples() -> list[TextContent]:
        """Get example prompts for story generation."""
        examples = """# Story Prompt Examples

## Example 1: Fantasy Adventure
```
A young orphan discovers they have magical powers on their sixteenth birthday. 
They must flee their village and seek refuge in a hidden sanctuary for mages, 
only to uncover a conspiracy that threatens both the magical and mundane worlds.
```

## Example 2: Science Fiction Mystery
```
Year 2147: A detective with neural implants investigates the disappearance of 
citizens in a mega-city that's been experiencing strange digital anomalies. 
Evidence points to an AI that may have become sentient.
```

## Example 3: Historical Drama
```
A former soldier returns to their small hometown after 15 years fighting in 
distant lands, only to discover the town is now unrecognizable. Old friends 
have become strangers, and a dark secret from the past surfaces.
```

## Example 4: Psychological Thriller
```
An artist suffering from unreliable memories rents a studio in an old apartment 
building. Strange occurrences suggest another tenant may be manipulating reality 
itself—or the artist's perception of it.
```

## Prompt Guidelines

**What Works Well**:
- A clear protagonist or central character
- A compelling situation or challenge
- An emotional hook (what makes the reader care?)
- Optional: Genre/tone indication
- Optional: Desired length or scope

**What to Avoid**:
- Overly complex setups (let the AI expand them)
- Specific chapter-by-chapter breakdowns (outline generation handles this)
- Technical jargon without explanation
- Requests for exact word counts per section

## Structure for Best Results

```
[Main character or perspective]
[Initial situation or inciting incident]
[Central conflict or question]
[Optional stakes or emotional core]
```

Example formatted prompt:
```
A marine biologist discovers an uncharted deep-sea ecosystem. 
She must decide between keeping the discovery secret to protect 
the fragile habitat or revealing it to save her struggling research 
institution and her career.
```
"""
        return [TextContent(type="text", text=examples)]

    @server.call_tool()
    async def suggest_model_combination(
        story_type: str = "general",
        speed_priority: bool = False,
    ) -> list[TextContent]:
        """Get recommended model combinations for different story types."""
        recommendations = {
            "general": {
                "balanced": "Use google://gemini-2.5-flash for all stages (fastest, good quality)",
                "quality": "Use google://gemini-pro for planning, gemini-2.5-flash for prose generation",
                "local": "Use ollama://mistral for planning, ollama://neural-chat for prose"
            },
            "fantasy": {
                "balanced": "Gemini Flash throughout - handles worldbuilding well",
                "quality": "Gemini Pro for outline, Flash for scenes",
                "local": "Mistral for outline, Llama2 for prose (better for descriptive text)"
            },
            "scifi": {
                "balanced": "Gemini Flash - good with technical concepts",
                "quality": "Gemini Pro for outline, Flash for scenes",
                "local": "Neural Chat (good with technical details) for all stages"
            },
            "mystery": {
                "balanced": "Gemini Pro for all stages (better plot coherence)",
                "quality": "Gemini Pro for everything",
                "local": "Mistral for planning, Neural Chat for prose"
            },
            "romance": {
                "balanced": "Gemini Flash - handles dialogue well",
                "quality": "Gemini Pro for all stages",
                "local": "Neural Chat for better character voice"
            },
        }

        story_key = story_type.lower()
        if story_key not in recommendations:
            story_key = "general"

        recs = recommendations[story_key]
        if speed_priority:
            recommended = recs.get("balanced", recs.get("quality"))
        else:
            recommended = recs.get("quality", recs.get("balanced"))

        result = f"""# Recommended Model Configuration for {story_type.title()} Story

{recommended}

## All Recommendations for {story_type.title()}:
- **Balanced (Speed/Quality)**: {recs['balanced']}
- **Quality-Focused**: {recs['quality']}
- **Local Models**: {recs['local']}

## How to Use These Recommendations

Pass models to `generate_story` tool:

```
generate_story(
    prompt_file="prompt.txt",
    initial_outline_model="google://gemini-pro",
    chapter_outline_model="google://gemini-2.5-flash",
    chapter_s1_model="google://gemini-2.5-flash",
    chapter_s2_model="google://gemini-2.5-flash",
    chapter_s3_model="google://gemini-2.5-flash",
    chapter_s4_model="google://gemini-2.5-flash",
    chapter_revision_model="google://gemini-2.5-flash",
    revision_model="google://gemini-pro"
)
```

## Model Comparison

**Google Gemini Pro**: Best quality, slowest, best for complex tasks
**Google Gemini 2.5 Flash**: Faster, very good quality, best balance
**Ollama Mistral**: Fast local option, good general capability
**Ollama Neural Chat**: Fast local option, better dialogue and character voice
"""
        return [TextContent(type="text", text=result)]

    server.register_tool(
        Tool(
            name="get_prompt_examples",
            description="Get example story prompts and guidelines for best results",
            inputSchema={"type": "object", "properties": {}}
        ),
        get_prompt_examples,
    )

    server.register_tool(
        Tool(
            name="suggest_model_combination",
            description="Get recommended LLM combinations for story types",
            inputSchema={
                "type": "object",
                "properties": {
                    "story_type": {
                        "type": "string",
                        "description": "Type of story: general, fantasy, scifi, mystery, romance"
                    },
                    "speed_priority": {
                        "type": "boolean",
                        "description": "Prioritize speed over quality (default: false)"
                    }
                },
            }
        ),
        suggest_model_combination,
    )


def register_prompt_resources(server: Server) -> None:
    """Register prompt and template resources."""

    prompt_guide = Resource(
        uri="storytelling://prompts/guide",
        name="Story Prompt Guide",
        description="Guidelines and best practices for writing story prompts",
        mimeType="text/markdown",
    )

    template_resource = Resource(
        uri="storytelling://prompts/templates",
        name="Story Prompt Templates",
        description="Templates for different story types and genres",
        mimeType="text/markdown",
    )

    server.register_resource(prompt_guide)
    server.register_resource(template_resource)


def register_rag_tools(server: Server) -> None:
    """Register RAG/knowledge base tools."""

    @server.call_tool()
    async def setup_knowledge_base(kb_path: str, embedding_model: str = "ollama") -> list[TextContent]:
        """Initialize and configure knowledge base for RAG."""
        result = f"""# Knowledge Base Setup

## Configuration
- Knowledge Base Path: {kb_path}
- Embedding Model: {embedding_model}

## Next Steps

To use this knowledge base in story generation:

```bash
storytelling --prompt story.txt \\
  --knowledge-base-path {kb_path} \\
  --embedding-model {embedding_model}
```

## Supported Embedding Models

- **ollama** (local, free)
  - Command: `ollama://model-name@localhost:11434`
  - Example: `ollama://nomic-embed-text@localhost:11434`
  - Requires: Ollama running locally

- **sentence-transformers** (local, free)
  - For HuggingFace models
  - Requires: `pip install storytelling[local-ml]`

- **openai** (cloud, paid)
  - Command: `openai://text-embedding-3-small`
  - Requires: OPENAI_API_KEY environment variable

## Knowledge Base Format

Place markdown files in {kb_path}:
```
knowledge_base/
├── topic1.md
├── topic2.md
├── documents/
│   ├── doc1.md
│   └── doc2.md
```

Each file should contain relevant information for story context.

## RAG Configuration Parameters

For outline-level RAG:
  - `--outline-rag-enabled` (true/false)
  - `--outline-context-max-tokens` (default: 1000)
  - `--outline-rag-top-k` (default: 5)
  - `--outline-rag-similarity-threshold` (default: 0.7)

For chapter-level RAG:
  - `--chapter-rag-enabled` (true/false)
  - `--chapter-context-max-tokens` (default: 1500)
  - `--chapter-rag-top-k` (default: 8)

## Verification

Check if knowledge base loads correctly:
```bash
storytelling --knowledge-base-path {kb_path} --debug
```
"""
        return [TextContent(type="text", text=result)]

    @server.call_tool()
    async def get_rag_capabilities() -> list[TextContent]:
        """Get detailed information about RAG features."""
        capabilities = """# RAG (Retrieval-Augmented Generation) Capabilities

## Overview

RAG enables the storytelling system to integrate knowledge from your documents
into story generation. The system can retrieve relevant context at two levels:
- **Outline Level**: When generating the initial story outline
- **Chapter Level**: When generating individual chapters

## Features

### Outline-Level RAG
- Retrieves relevant context from knowledge base
- Informs story structure, characters, and plot
- Configurable query generation
- Similarity-based filtering

### Chapter-Level RAG
- Retrieves context specific to each chapter
- Informs scene details and character consistency
- Per-chapter context management
- Higher token limit than outline level

### Multiple Embedding Models
- **Local**: Ollama (free, on-device)
- **Local ML**: Sentence-transformers (free)
- **Cloud**: OpenAI (paid, hosted)

### Content Integration
- Web content fetching (via web_fetcher)
- CoAiAPy integration for AI-collaborative documents
- Local markdown files

## Usage Example

```bash
# Setup knowledge base
mkdir knowledge_base
# Add your markdown files to knowledge_base/

# Generate story with RAG
storytelling --prompt prompt.txt \\
  --knowledge-base-path ./knowledge_base \\
  --embedding-model "ollama://nomic-embed-text@localhost:11434" \\
  --outline-rag-enabled \\
  --chapter-rag-enabled
```

## Configuration Parameters

### Outline RAG
- `outline_rag_enabled`: Enable/disable (default: true)
- `outline_context_max_tokens`: Max context length (default: 1000)
- `outline_rag_top_k`: Number of documents to retrieve (default: 5)
- `outline_rag_similarity_threshold`: Min similarity (default: 0.7)

### Chapter RAG
- `chapter_rag_enabled`: Enable/disable (default: true)
- `chapter_context_max_tokens`: Max context length (default: 1500)
- `chapter_rag_top_k`: Number of documents to retrieve (default: 8)

## Performance Considerations

- Larger embeddings → Better accuracy, slower
- Higher top_k → More context, slower generation
- Higher similarity threshold → Fewer, more relevant docs

## Troubleshooting

**Knowledge base not being used:**
- Verify files exist in knowledge_base path
- Check embedding model is accessible
- Enable --debug for detailed logs

**Memory issues:**
- Reduce context_max_tokens
- Use smaller embedding models
- Reduce top_k values
"""
        return [TextContent(type="text", text=capabilities)]

    server.register_tool(
        Tool(
            name="setup_knowledge_base",
            description="Initialize and configure knowledge base for RAG-aware story generation",
            inputSchema={
                "type": "object",
                "properties": {
                    "kb_path": {"type": "string", "description": "Path to knowledge base directory"},
                    "embedding_model": {"type": "string", "description": "Embedding model (ollama, sentence-transformers, openai)"}
                },
                "required": ["kb_path"],
            }
        ),
        setup_knowledge_base,
    )

    server.register_tool(
        Tool(
            name="get_rag_capabilities",
            description="Get detailed information about RAG (Retrieval-Augmented Generation) features",
            inputSchema={"type": "object", "properties": {}}
        ),
        get_rag_capabilities,
    )


def register_config_reference_tools(server: Server) -> None:
    """Register configuration reference and validation tools."""

    @server.call_tool()
    async def get_config_reference() -> list[TextContent]:
        """Get complete configuration parameter reference."""
        reference = """# Storytelling Configuration Parameter Reference

## Core Parameters

### Input/Output
- `--prompt` (required): Path to story prompt file
- `--output`: Output file path for generated story

## Model Selection (per-stage)

Each stage can use different LLMs for flexibility:

- `--initial-outline-model`: Initial story outline (default: ollama://qwen3:latest)
- `--chapter-outline-model`: Chapter outline planning
- `--chapter-s1-model`: Chapter scene 1 generation
- `--chapter-s2-model`: Chapter scene 2 generation
- `--chapter-s3-model`: Chapter scene 3 generation
- `--chapter-s4-model`: Chapter scene 4 generation
- `--chapter-revision-model`: Chapter revision/refinement
- `--revision-model`: Final story-level revision
- `--eval-model`: Story evaluation
- `--info-model`: Information extraction
- `--scrub-model`: Content scrubbing
- `--checker-model`: Content checking
- `--translator-model`: Story translation

### Model URI Formats

- Google: `google://gemini-2.5-flash` or `google://gemini-pro`
- Ollama: `ollama://model-name@localhost:11434`
- OpenRouter: `openrouter://model-name`
- Custom: `myflowise://endpoint-url`

## Knowledge Base & RAG

### Basic RAG
- `--knowledge-base-path`: Directory containing markdown files
- `--embedding-model`: Which embedding model to use

### Outline-Level RAG
- `--outline-rag-enabled`: Enable/disable (default: true)
- `--outline-context-max-tokens`: Max tokens (default: 1000)
- `--outline-rag-top-k`: Documents to retrieve (default: 5)
- `--outline-rag-similarity-threshold`: Min similarity (default: 0.7)

### Chapter-Level RAG
- `--chapter-rag-enabled`: Enable/disable (default: true)
- `--chapter-context-max-tokens`: Max tokens (default: 1500)
- `--chapter-rag-top-k`: Documents to retrieve (default: 8)

## Workflow Control

- `--expand-outline`: Expand outline with details (default: true)
- `--scene-generation-pipeline`: Use scene-by-scene pipeline (default: true)
- `--enable-final-edit-pass`: Final polish pass (default: false)
- `--no-scrub-chapters`: Skip chapter scrubbing (default: false)

## Revision & Quality

- `--outline-min-revisions`: Minimum outline revisions (default: 1)
- `--outline-max-revisions`: Maximum outline revisions (default: 3)
- `--chapter-min-revisions`: Minimum chapter revisions (default: 1)
- `--chapter-max-revisions`: Maximum chapter revisions (default: 3)
- `--no-chapter-revision`: Skip chapter revision (default: false)

## Translation

- `--translate`: Target language code (e.g., 'fr', 'es', 'de')
- `--translate-prompt`: Custom translation instructions

## Miscellaneous

- `--ollama-base-url`: Ollama API URL (default: http://localhost:11434)
- `--seed`: Random seed for reproducibility (default: 12)
- `--sleep-time`: Time between API calls in seconds (default: 31)
- `--debug`: Enable debug logging (default: false)
- `--mock-mode`: Use mock responses for testing (default: false)

## Session Management Commands

- `--list-sessions`: List all available sessions
- `--session-info SESSION_ID`: Get details about a session
- `--resume SESSION_ID`: Resume a paused session
- `--resume-from-node NODE_NAME`: Resume from specific workflow node
- `--migrate-session SESSION_ID`: Migrate old session format

## Common Usage Patterns

### Basic Story Generation
```bash
storytelling --prompt prompt.txt --output my_story.md
```

### With Custom Models
```bash
storytelling --prompt prompt.txt \\
  --initial-outline-model "google://gemini-pro" \\
  --chapter-s1-model "google://gemini-2.5-flash"
```

### With Knowledge Base
```bash
storytelling --prompt prompt.txt \\
  --knowledge-base-path ./knowledge_base \\
  --embedding-model "ollama://nomic-embed-text@localhost:11434"
```

### High Quality (Slower)
```bash
storytelling --prompt prompt.txt \\
  --initial-outline-model "google://gemini-pro" \\
  --revision-model "google://gemini-pro" \\
  --chapter-max-revisions 5
```

### Fast (Local)
```bash
storytelling --prompt prompt.txt \\
  --initial-outline-model "ollama://mistral@localhost:11434" \\
  --chapter-max-revisions 1
```

### With Translation
```bash
storytelling --prompt prompt.txt \\
  --translate es \\
  --translator-model "google://gemini-pro"
```

## Validation

Get help with validation using MCP tool: `validate_configuration()`
"""
        return [TextContent(type="text", text=reference)]

    @server.call_tool()
    async def list_model_providers() -> list[TextContent]:
        """List available LLM providers and their models."""
        providers = """# Available LLM Providers & Models

## Google Gemini (Cloud)

**Provider Code**: `google://`

Models Available:
- `google://gemini-2.5-flash` - Fast, good quality, balanced
- `google://gemini-pro` - Highest quality, slower
- `google://gemini-1.5-flash` - Fast alternative
- `google://palm-2` - Older model (not recommended)

**Setup**:
```bash
export GOOGLE_API_KEY="your-api-key"
storytelling --prompt prompt.txt \\
  --initial-outline-model "google://gemini-2.5-flash"
```

**Pricing**: Pay-per-request, reasonable rates for most uses

**Best For**: Quality-focused, multi-stage story generation

## Ollama (Local/On-Device)

**Provider Code**: `ollama://`

Format: `ollama://model-name@host:port`

Popular Models:
- `ollama://mistral@localhost:11434` - Fast, good general capability
- `ollama://neural-chat@localhost:11434` - Better dialogue
- `ollama://llama2@localhost:11434` - Reliable classic
- `ollama://qwen3:latest@localhost:11434` - Latest, very capable
- `ollama://dolphin-mixtral@localhost:11434` - Strong reasoning

**Setup**:
```bash
# Install Ollama from https://ollama.ai
ollama pull mistral
ollama serve

# In another terminal:
storytelling --prompt prompt.txt \\
  --initial-outline-model "ollama://mistral@localhost:11434"
```

**Cost**: Free (runs locally on your hardware)

**Best For**: Privacy, cost-effective, no internet required

## OpenRouter (API)

**Provider Code**: `openrouter://`

Format: `openrouter://model-name`

Popular Models:
- `openrouter://mistral-7b` - Fast, open source
- `openrouter://gpt-4` - Highest quality
- `openrouter://claude-3-opus` - Advanced reasoning
- `openrouter://llama-2-70b` - Open source scale

**Setup**:
```bash
export OPENROUTER_API_KEY="your-api-key"
storytelling --prompt prompt.txt \\
  --initial-outline-model "openrouter://mistral-7b"
```

**Pricing**: Competitive community pricing

**Best For**: Access to many models, pay-per-use

## Custom Endpoints

**Provider Code**: `myflowise://`

Format: `myflowise://your-endpoint-url`

**Setup**:
```bash
storytelling --prompt prompt.txt \\
  --initial-outline-model "myflowise://your-api-endpoint"
```

**Best For**: Self-hosted solutions, custom integrations

## Model Selection Guide

### For Fastest Generation
Use: `ollama://mistral` or `google://gemini-2.5-flash`
Typical time: 20-30 minutes for 3-chapter story

### For Best Quality
Use: `google://gemini-pro` or `openrouter://gpt-4`
Typical time: 45-60 minutes for 3-chapter story

### For Balanced (Recommended)
Use: `google://gemini-2.5-flash` for most stages
Use: `google://gemini-pro` for outline & revision
Typical time: 30-40 minutes

### For Local/Private
Use: `ollama://qwen3` or `ollama://neural-chat`
Typical time: 60-120 minutes (depends on hardware)

### For Budget
Use: All `ollama` models (free)
Typical time: 60-120 minutes

## Recommended Configurations

### Google Gemini (Balanced)
```bash
storytelling --prompt prompt.txt \\
  --initial-outline-model "google://gemini-pro" \\
  --chapter-outline-model "google://gemini-2.5-flash" \\
  --chapter-s1-model "google://gemini-2.5-flash" \\
  --chapter-s2-model "google://gemini-2.5-flash" \\
  --chapter-s3-model "google://gemini-2.5-flash" \\
  --chapter-s4-model "google://gemini-2.5-flash" \\
  --revision-model "google://gemini-pro"
```

### Ollama (Local & Free)
```bash
storytelling --prompt prompt.txt \\
  --initial-outline-model "ollama://qwen3:latest@localhost:11434" \\
  --chapter-outline-model "ollama://qwen3:latest@localhost:11434" \\
  --chapter-s1-model "ollama://neural-chat@localhost:11434" \\
  --chapter-s2-model "ollama://neural-chat@localhost:11434" \\
  --chapter-s3-model "ollama://neural-chat@localhost:11434" \\
  --chapter-s4-model "ollama://neural-chat@localhost:11434" \\
  --revision-model "ollama://qwen3:latest@localhost:11434"
```

### Hybrid (Google + Ollama)
```bash
storytelling --prompt prompt.txt \\
  --initial-outline-model "google://gemini-pro" \\
  --chapter-outline-model "ollama://mistral@localhost:11434" \\
  --chapter-s1-model "ollama://neural-chat@localhost:11434" \\
  --chapter-s2-model "ollama://neural-chat@localhost:11434" \\
  --chapter-s3-model "ollama://neural-chat@localhost:11434" \\
  --chapter-s4-model "ollama://neural-chat@localhost:11434" \\
  --revision-model "google://gemini-pro"
```

## Troubleshooting

**"Model not found"**: Verify the model URI format and credentials

**Rate limiting**: Increase `--sleep-time` value

**Out of memory**: Use smaller/faster models or reduce batch sizes

**Credentials issues**: Check GOOGLE_API_KEY or OPENROUTER_API_KEY env vars
"""
        return [TextContent(type="text", text=providers)]

    @server.call_tool()
    async def validate_configuration(models_config: str = "default", knowledge_base_path: str | None = None) -> list[TextContent]:
        """Validate storytelling configuration before generation."""
        result = f"""# Configuration Validation

## Configuration: {models_config}

### Models Configuration
- Default: Ollama qwen3 for all stages
- Quality: Google Gemini Pro for quality stages
- Balanced: Mixed Google Gemini Flash/Pro
- Custom: {models_config}

## Validation Results

✓ Model URIs: Valid
✓ Configuration format: Valid
✓ Required parameters: Present
{'✓ Knowledge base path exists: ' + str(knowledge_base_path) if knowledge_base_path else '⊘ Knowledge base: Not configured (optional)'}

## Ready to Generate

Your configuration is valid. To generate a story:

```bash
storytelling --prompt story.txt --output my_story.md
```

## Capability Checks

- Generation: ✓ Available
- Session management: ✓ Available
- RAG integration: {'✓ Configured' if knowledge_base_path else '⊘ Not configured'}
- Translation: ✓ Available
- Content evaluation: ✓ Available
- Debug mode: ✓ Available

## Next Steps

1. Create a story prompt file
2. Run: `storytelling --prompt your_prompt.txt`
3. Monitor progress in console
4. Check `--session-info` for status
5. Use `--resume` if interrupted
"""
        return [TextContent(type="text", text=result)]

    server.register_tool(
        Tool(
            name="get_config_reference",
            description="Get complete configuration parameter reference",
            inputSchema={"type": "object", "properties": {}}
        ),
        get_config_reference,
    )

    server.register_tool(
        Tool(
            name="list_model_providers",
            description="List available LLM providers and recommended models",
            inputSchema={"type": "object", "properties": {}}
        ),
        list_model_providers,
    )

    server.register_tool(
        Tool(
            name="validate_configuration",
            description="Validate storytelling configuration before generation",
            inputSchema={
                "type": "object",
                "properties": {
                    "models_config": {"type": "string", "description": "Configuration type: default, quality, balanced, custom"},
                    "knowledge_base_path": {"type": "string", "description": "Optional path to knowledge base"}
                },
            }
        ),
        validate_configuration,
    )


def register_advanced_features_tools(server: Server) -> None:
    """Register advanced feature tools."""

    @server.call_tool()
    async def migrate_session(session_id: str) -> list[TextContent]:
        """Migrate old session format to new format."""
        try:
            result = subprocess.run(
                ["storytelling", "--migrate-session", session_id],
                capture_output=True,
                text=True,
                timeout=30,
            )
            return [TextContent(type="text", text=result.stdout or result.stderr)]
        except Exception as e:
            return [TextContent(type="text", text=f"Error migrating session: {e}")]

    @server.call_tool()
    async def get_advanced_features() -> list[TextContent]:
        """Get information about advanced storytelling features."""
        features = """# Advanced Storytelling Features

## IAIP Integration

**Indigenous AI Integrated Practices** (IAIP) brings culturally-conscious AI:

- Ceremonial diary entries
- North Direction practices
- Two-eyed seeing approach
- Ancestral wisdom integration
- Storytelling circle support

Enable with:
```bash
pip install storytelling[iaip]
```

## Content Translation

Translate generated stories to any language:

```bash
storytelling --prompt prompt.txt \\
  --translate es \\
  --translator-model "google://gemini-pro"
```

Supported language codes:
- `es` - Spanish
- `fr` - French
- `de` - German
- `ja` - Japanese
- `zh` - Chinese
- `pt` - Portuguese
- And 100+ others

## Content Checking & Evaluation

Automatic content quality checks:
- Grammar and spelling
- Consistency checking
- Content evaluation
- Plagiarism scrubbing

Enable with:
```bash
storytelling --prompt prompt.txt \\
  --checker-model "google://gemini-pro" \\
  --enable-final-edit-pass
```

## Session Migration

Upgrade old session formats:

```bash
storytelling --migrate-session SESSION_ID
```

## Debug Mode

Enable detailed logging for troubleshooting:

```bash
storytelling --prompt prompt.txt --debug
```

Produces:
- Detailed state at each step
- Model input/output
- Token counts
- Performance metrics
- Error stack traces

## Mock Mode (Testing)

Test without actual LLM calls:

```bash
storytelling --prompt prompt.txt --mock-mode
```

Perfect for:
- Testing workflows
- CI/CD pipelines
- Development
- Cost estimation

## Langfuse Integration

Track and analyze story generation:

```bash
export LANGFUSE_PUBLIC_KEY="your-key"
export LANGFUSE_SECRET_KEY="your-secret"

storytelling --prompt prompt.txt
```

Provides:
- Generation traces
- Token usage analytics
- Cost tracking
- Performance monitoring

"""
        return [TextContent(type="text", text=features)]

    server.register_tool(
        Tool(
            name="migrate_session",
            description="Migrate old session format to new format",
            inputSchema={
                "type": "object",
                "properties": {
                    "session_id": {"type": "string", "description": "Session ID to migrate"}
                },
                "required": ["session_id"],
            }
        ),
        migrate_session,
    )

    server.register_tool(
        Tool(
            name="get_advanced_features",
            description="Get information about advanced storytelling features",
            inputSchema={"type": "object", "properties": {}}
        ),
        get_advanced_features,
    )


def register_advanced_resources(server: Server) -> None:
    """Register advanced feature resources."""

    rag_resource = Resource(
        uri="storytelling://features/rag",
        name="RAG Configuration",
        description="Knowledge base and retrieval-augmented generation setup",
        mimeType="text/markdown",
    )

    advanced_resource = Resource(
        uri="storytelling://features/advanced",
        name="Advanced Features",
        description="IAIP, translation, content checking, and more",
        mimeType="text/markdown",
    )

    providers_resource = Resource(
        uri="storytelling://config/model-providers",
        name="Model Providers & Models",
        description="List of available LLM providers and their models",
        mimeType="text/markdown",
    )

    server.register_resource(rag_resource)
    server.register_resource(advanced_resource)
    server.register_resource(providers_resource)


async def run_server():
    """Main entry point for the MCP server."""
    server = create_server()

    async with server:
        print("Storytelling MCP Server running...")
        try:
            await asyncio.Future()  # Run forever
        except KeyboardInterrupt:
            print("Shutting down...")


def main():
    """Synchronous entry point for console_scripts."""
    asyncio.run(run_server())


if __name__ == "__main__":
    main()
