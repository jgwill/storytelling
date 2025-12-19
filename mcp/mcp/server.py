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
    ToolResult,
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

    # Register resources
    register_workflow_resources(server)
    register_configuration_resources(server)
    register_prompt_resources(server)

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


async def main():
    """Main entry point for the MCP server."""
    server = create_server()

    async with server:
        print("Storytelling MCP Server running...")
        try:
            await asyncio.Future()  # Run forever
        except KeyboardInterrupt:
            print("Shutting down...")


if __name__ == "__main__":
    asyncio.run(main())
