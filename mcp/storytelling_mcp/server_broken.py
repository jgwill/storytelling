"""
MCP Server for Storytelling - AI-powered narrative generation.
Uses current MCP SDK with proper stdio integration for gemini-cli and other tools.
"""

import asyncio
import subprocess
from mcp.server import Server
from mcp.types import TextContent


async def run_server():
    """Main async server function."""
    server = Server("storytelling-mcp")

    @server.list_tools()
    async def list_tools():
        """List available tools."""
        return [
            {
                "name": "generate_story",
                "description": "Generate a complete story from a prompt",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "prompt_file": {"type": "string", "description": "Path to prompt file"},
                        "output_file": {"type": "string", "description": "Output file path (optional)"},
                        "model": {"type": "string", "description": "Model (google://gemini-2.5-flash, ollama://model@host:port)"}
                    },
                    "required": ["prompt_file"]
                }
            },
            {
                "name": "list_sessions",
                "description": "List all story generation sessions",
                "inputSchema": {"type": "object", "properties": {}}
            },
            {
                "name": "get_session_info",
                "description": "Get information about a session",
                "inputSchema": {
                    "type": "object",
                    "properties": {"session_id": {"type": "string"}},
                    "required": ["session_id"]
                }
            },
            {
                "name": "resume_session",
                "description": "Resume an interrupted session",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "session_id": {"type": "string"},
                        "resume_from_node": {"type": "string"}
                    },
                    "required": ["session_id"]
                }
            },
            {
                "name": "validate_model_uri",
                "description": "Validate a model URI",
                "inputSchema": {
                    "type": "object",
                    "properties": {"model_uri": {"type": "string"}},
                    "required": ["model_uri"]
                }
            },
            {
                "name": "describe_workflow",
                "description": "Describe the story generation workflow",
                "inputSchema": {"type": "object", "properties": {}}
            },
            {
                "name": "get_prompt_examples",
                "description": "Get example story prompts",
                "inputSchema": {"type": "object", "properties": {}}
            },
            {
                "name": "list_model_providers",
                "description": "List available LLM providers",
                "inputSchema": {"type": "object", "properties": {}}
            }
        ]

    @server.call_tool()
    async def handle_tool_call(name: str, arguments: dict):
        """Handle tool calls."""
        if name == "generate_story":
            prompt_file = arguments["prompt_file"]
            output_file = arguments.get("output_file", "")
            model = arguments.get("model", "google://gemini-2.5-flash")
            
            args = ["storytelling", "--prompt", prompt_file, "--initial-outline-model", model]
            if output_file:
                args.extend(["--output", output_file])
            
            try:
                result = subprocess.run(args, capture_output=True, text=True, timeout=3600)
                return [TextContent(type="text", text=result.stdout or result.stderr or "Story generated")]
            except Exception as e:
                return [TextContent(type="text", text=f"Error: {e}")]
        
        elif name == "list_sessions":
            try:
                result = subprocess.run(["storytelling", "--list-sessions"], capture_output=True, text=True, timeout=30)
                return [TextContent(type="text", text=result.stdout or "No sessions")]
            except Exception as e:
                return [TextContent(type="text", text=f"Error: {e}")]
        
        elif name == "get_session_info":
            session_id = arguments["session_id"]
            try:
                result = subprocess.run(["storytelling", "--session-info", session_id], capture_output=True, text=True, timeout=30)
                return [TextContent(type="text", text=result.stdout or "Session not found")]
            except Exception as e:
                return [TextContent(type="text", text=f"Error: {e}")]
        
        elif name == "resume_session":
            session_id = arguments["session_id"]
            args = ["storytelling", "--resume", session_id]
            if "resume_from_node" in arguments:
                args.extend(["--resume-from-node", arguments["resume_from_node"]])
            try:
                result = subprocess.run(args, capture_output=True, text=True, timeout=3600)
                return [TextContent(type="text", text=result.stdout or result.stderr or "Session resumed")]
            except Exception as e:
                return [TextContent(type="text", text=f"Error: {e}")]
        
        elif name == "validate_model_uri":
            model_uri = arguments["model_uri"]
            valid_schemes = ["google", "ollama", "openrouter", "myflowise"]
            try:
                scheme = model_uri.split("://")[0]
                if scheme in valid_schemes:
                    return [TextContent(type="text", text=f"✓ Valid URI: {model_uri}")]
                else:
                    return [TextContent(type="text", text=f"✗ Invalid scheme. Valid: {', '.join(valid_schemes)}")]
            except:
                return [TextContent(type="text", text="Invalid URI format")]
        
        elif name == "describe_workflow":
            return [TextContent(type="text", text="""# Storytelling Workflow

6 Stages:
1. **Story Elements** - Extract genre, theme, pacing
2. **Initial Outline** - Create story structure
3. **Chapter Planning** - Plan chapters and scenes
4. **Scene Generation** - Generate 4 scenes per chapter
5. **Chapter Revision** - Polish chapters
6. **Final Revision** - Complete story polish

Each stage uses LLMs for creative generation.""")]
        
        elif name == "get_prompt_examples":
            return [TextContent(type="text", text="""# Story Prompt Examples

**Fantasy**: A young orphan discovers magical powers on their sixteenth birthday and must flee their village to a sanctuary for mages.

**Science Fiction**: A detective with neural implants investigates disappearances in a mega-city experiencing digital anomalies.

**Mystery**: A marine biologist discovers an uncharted ecosystem and must choose between protecting it or saving her career.

**Thriller**: An artist with unreliable memories experiences strange occurrences in an old apartment building.

**Tips**: Include protagonist, situation, conflict, and emotional hook.""")]
        
        elif name == "list_model_providers":
            return [TextContent(type="text", text="""# LLM Providers

**Google Gemini** (Cloud)
- google://gemini-2.5-flash (fast)
- google://gemini-pro (quality)
Requires: GOOGLE_API_KEY env var

**Ollama** (Local, Free)
- ollama://mistral@localhost:11434
- ollama://qwen3:latest@localhost:11434
Setup: ollama pull mistral && ollama serve

**OpenRouter** (Community)
- openrouter://mistral-7b
- openrouter://gpt-4
Requires: OPENROUTER_API_KEY env var

**Recommendations**: Fast = Ollama/Gemini-Flash, Quality = Gemini-Pro, Local = Ollama models""")]
        return [TextContent(type="text", text=f"Unknown tool: {name}")]

    async with server:
        await server.wait_for_shutdown()


def main():
    """Entry point for console_scripts."""
    asyncio.run(run_server())


if __name__ == "__main__":
    main()
