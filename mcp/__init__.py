"""
MCP Server for Storytelling: AI-powered narrative generation system.

This MCP exposes the storytelling package as a set of tools, resources, and prompts
for LLMs to orchestrate story generation workflows using the RISE framework.

Supported model URIs:
- google://gemini-2.5-flash
- ollama://model-name@localhost:11434
- openrouter://model-name
"""

__version__ = "0.1.1"
__all__ = ["server"]
