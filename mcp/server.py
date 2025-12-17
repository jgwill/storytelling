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

    # Register resources
    register_workflow_resources(server)
    register_configuration_resources(server)

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
