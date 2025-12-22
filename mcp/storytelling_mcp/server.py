"""
MCP Server for Storytelling Package
Uses MCP SDK 1.25.0 with proper stdio transport
"""

import subprocess
import anyio
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool


app = Server("storytelling-mcp")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available storytelling tools."""
    return [
        Tool(
            name="generate_story",
            description="Generate a complete multi-chapter story from a prompt file",
            inputSchema={
                "type": "object",
                "properties": {
                    "prompt_file": {
                        "type": "string",
                        "description": "Path to the prompt file"
                    },
                    "output_file": {
                        "type": "string",
                        "description": "Optional output file path"
                    },
                    "model": {
                        "type": "string",
                        "description": "Model URI (e.g., google://gemini-2.5-flash)"
                    }
                },
                "required": ["prompt_file"]
            }
        ),
        Tool(
            name="list_sessions",
            description="List all story generation sessions",
            inputSchema={"type": "object", "properties": {}}
        ),
        Tool(
            name="get_session_info",
            description="Get detailed information about a session",
            inputSchema={
                "type": "object",
                "properties": {
                    "session_id": {"type": "string", "description": "Session ID"}
                },
                "required": ["session_id"]
            }
        ),
        Tool(
            name="resume_session",
            description="Resume an interrupted story generation session",
            inputSchema={
                "type": "object",
                "properties": {
                    "session_id": {"type": "string"},
                    "resume_from_node": {"type": "string"}
                },
                "required": ["session_id"]
            }
        ),
        Tool(
            name="describe_workflow",
            description="Get an overview of the 6-stage story generation workflow",
            inputSchema={"type": "object", "properties": {}}
        ),
        Tool(
            name="get_prompt_examples",
            description="Get example story prompts for different genres",
            inputSchema={"type": "object", "properties": {}}
        ),
        Tool(
            name="list_model_providers",
            description="List available LLM providers (Google, Ollama, OpenRouter)",
            inputSchema={"type": "object", "properties": {}}
        ),
        Tool(
            name="validate_model_uri",
            description="Validate a model URI format",
            inputSchema={
                "type": "object",
                "properties": {
                    "model_uri": {"type": "string"}
                },
                "required": ["model_uri"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls."""
    
    if name == "generate_story":
        prompt_file = arguments["prompt_file"]
        model = arguments.get("model", "google://gemini-2.5-flash")
        
        cmd = ["storytelling", "--prompt", prompt_file, "--initial-outline-model", model]
        if "output_file" in arguments:
            cmd.extend(["--output", arguments["output_file"]])
        
        try:
            result = await anyio.run_process(cmd, check=False)
            output = result.stdout.decode() if result.stdout else result.stderr.decode()
            return [TextContent(type="text", text=output or "Story generation started")]
        except Exception as e:
            return [TextContent(type="text", text=f"Error: {str(e)}")]
    
    elif name == "list_sessions":
        try:
            result = await anyio.run_process(["storytelling", "--list-sessions"], check=False)
            output = result.stdout.decode() if result.stdout else "No sessions found"
            return [TextContent(type="text", text=output)]
        except Exception as e:
            return [TextContent(type="text", text=f"Error: {str(e)}")]
    
    elif name == "get_session_info":
        session_id = arguments["session_id"]
        try:
            result = await anyio.run_process(
                ["storytelling", "--session-info", session_id],
                check=False
            )
            output = result.stdout.decode() if result.stdout else "Session not found"
            return [TextContent(type="text", text=output)]
        except Exception as e:
            return [TextContent(type="text", text=f"Error: {str(e)}")]
    
    elif name == "resume_session":
        session_id = arguments["session_id"]
        cmd = ["storytelling", "--resume", session_id]
        if "resume_from_node" in arguments:
            cmd.extend(["--resume-from-node", arguments["resume_from_node"]])
        
        try:
            result = await anyio.run_process(cmd, check=False)
            output = result.stdout.decode() if result.stdout else result.stderr.decode()
            return [TextContent(type="text", text=output or "Session resumed")]
        except Exception as e:
            return [TextContent(type="text", text=f"Error: {str(e)}")]
    
    elif name == "describe_workflow":
        text = """# Storytelling Workflow

The system generates stories through 6 major stages:

## 1. Story Elements
Analyzes your prompt to extract genre, theme, pacing, and style preferences.

## 2. Initial Outline
Creates a comprehensive story structure with characters, plot points, and chapter breakdown.

## 3. Chapter Planning
Breaks down the outline into individual chapters, each with a detailed plan for 4 scenes.

## 4. Scene Generation
Generates 4 polished scenes per chapter (500-1000 words each):
- Scene 1: Establish/Introduce
- Scene 2: Develop/Complicate
- Scene 3: Intensify/Escalate
- Scene 4: Resolve/Transition

## 5. Chapter Revision
Refines each chapter through multiple passes for consistency and quality.

## 6. Final Revision
Performs a story-level polish ensuring global coherence.

Each stage can use different LLM models for optimal results."""
        return [TextContent(type="text", text=text)]
    
    elif name == "get_prompt_examples":
        text = """# Story Prompt Examples

## Fantasy
A young orphan discovers magical powers on their sixteenth birthday and must flee to a hidden sanctuary for mages.

## Science Fiction
Year 2147: A detective with neural implants investigates disappearances in a mega-city experiencing digital anomalies.

## Mystery
A marine biologist discovers an uncharted ecosystem and must choose between protecting it or saving her career.

## Thriller
An artist with unreliable memories rents a studio where strange occurrences suggest reality manipulation.

## Historical Drama
A soldier returns home after 15 years to find the town unrecognizable and a dark secret surfacing.

**Writing Tips:**
- Include a clear protagonist
- Present a compelling situation
- Add an emotional hook
- Optional: specify genre, tone, desired length"""
        return [TextContent(type="text", text=text)]
    
    elif name == "list_model_providers":
        text = """# Available LLM Providers

## Google Gemini (Cloud, API)
**Models:**
- `google://gemini-2.5-flash` - Fast, balanced quality
- `google://gemini-pro` - Best quality, slower

**Setup:** Set `GOOGLE_API_KEY` environment variable

**Best for:** Quality-focused generation, multi-model workflows

## Ollama (Local, Free)
**Models:**
- `ollama://mistral@localhost:11434` - Fast, general purpose
- `ollama://qwen3:latest@localhost:11434` - Latest, very capable
- `ollama://neural-chat@localhost:11434` - Better dialogue

**Setup:** Install Ollama, run `ollama pull mistral && ollama serve`

**Best for:** Privacy, cost-free, offline work

## OpenRouter (Community, Pay-per-use)
**Models:**
- `openrouter://mistral-7b` - Fast open source
- `openrouter://gpt-4` - Highest quality

**Setup:** Set `OPENROUTER_API_KEY` environment variable

**Best for:** Access to many models, flexible pricing

## Recommendations
- **Fastest:** `ollama://mistral` or `google://gemini-2.5-flash`
- **Quality:** `google://gemini-pro`
- **Budget:** Ollama models (free)
- **Balanced:** `google://gemini-2.5-flash` for all stages"""
        return [TextContent(type="text", text=text)]
    
    elif name == "validate_model_uri":
        model_uri = arguments["model_uri"]
        valid_schemes = ["google", "ollama", "openrouter", "myflowise"]
        
        try:
            scheme = model_uri.split("://")[0]
            if scheme in valid_schemes:
                return [TextContent(type="text", text=f"✓ Valid model URI: {model_uri}")]
            else:
                return [TextContent(
                    type="text",
                    text=f"✗ Invalid scheme '{scheme}'. Valid: {', '.join(valid_schemes)}"
                )]
        except:
            return [TextContent(type="text", text="✗ Invalid URI format. Use: scheme://model")]
    
    return [TextContent(type="text", text=f"Unknown tool: {name}")]


async def main():
    """Main entry point - runs MCP server via stdio."""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


def run():
    """Synchronous entry point for console_scripts."""
    anyio.run(main)


if __name__ == "__main__":
    run()
