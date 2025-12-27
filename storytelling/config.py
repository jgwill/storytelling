import argparse
import os
import sys
from typing import Any, Dict, List, Optional

import yaml
from pydantic import BaseModel, Field


class StyleGlossary(BaseModel):
    """Style glossary configuration for buzz term detection and replacement."""
    avoid_terms: List[str] = Field(default_factory=list)
    preferred_alternatives: Dict[str, List[str]] = Field(default_factory=dict)
    custom_avoid_phrases: List[str] = Field(default_factory=list)
    tone_words: Dict[str, List[str]] = Field(default_factory=dict)
    enforcement_level: str = Field(default="moderate")


def load_style_glossary(path: str) -> StyleGlossary:
    """Load style glossary from YAML file."""
    with open(path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    return StyleGlossary(**data)


def get_default_glossary() -> StyleGlossary:
    """Return default style glossary with common buzz terms."""
    return StyleGlossary(
        avoid_terms=[
            "gap", "journey", "leverage", "synergy", "paradigm",
            "ecosystem", "landscape", "bandwidth", "pivot",
            "very", "really", "just", "basically", "actually",
            "amazing", "incredible", "literally"
        ],
        preferred_alternatives={
            "gap": ["distance", "divide", "separation", "difference"],
            "journey": ["path", "progression", "evolution", "experience"],
            "leverage": ["use", "employ", "apply", "harness"],
            "very": ["extremely", "remarkably", "exceptionally"],
            "amazing": ["remarkable", "extraordinary", "striking"],
        },
        custom_avoid_phrases=[
            "at the end of the day", "moving forward", "low-hanging fruit",
            "it was then that", "suddenly realized", "heart pounded"
        ],
        enforcement_level="moderate"
    )


class WillWriteConfig(BaseModel):
    """
    Configuration for the WillWrite application, validated with Pydantic.
    """

    # Core Parameters
    prompt_file: Optional[str] = Field(
        None,
        alias="prompt",
        description="The file path to the initial user prompt for the story. Optional when resuming.",
    )
    output_file: Optional[str] = Field(
        "",
        alias="output",
        description="An optional file path and name for the output files.",
    )
    # Model Selection
    initial_outline_model: str = Field(
        "ollama://qwen3:latest@localhost:11434",
        alias="initial-outline-model",
        description="Model URI for initial outline generation. Format: google://gemini-2.5-flash, ollama://model@host:port, or openrouter://model",
    )
    chapter_outline_model: str = Field(
        "ollama://qwen3:latest@localhost:11434",
        alias="chapter-outline-model",
        description="Model URI for chapter outline generation. Format: google://gemini-2.5-flash, ollama://model@host:port, or openrouter://model",
    )
    chapter_s1_model: str = Field(
        "ollama://qwen3:latest@localhost:11434",
        alias="chapter-s1-model",
        description="Model URI for chapter scene 1 generation. Format: google://gemini-2.5-flash, ollama://model@host:port, or openrouter://model",
    )
    chapter_s2_model: str = Field(
        "ollama://qwen3:latest@localhost:11434",
        alias="chapter-s2-model",
        description="Model URI for chapter scene 2 generation. Format: google://gemini-2.5-flash, ollama://model@host:port, or openrouter://model",
    )
    chapter_s3_model: str = Field(
        "ollama://qwen3:latest@localhost:11434",
        alias="chapter-s3-model",
        description="Model URI for chapter scene 3 generation. Format: google://gemini-2.5-flash, ollama://model@host:port, or openrouter://model",
    )
    chapter_s4_model: str = Field(
        "ollama://qwen3:latest@localhost:11434",
        alias="chapter-s4-model",
        description="Model URI for chapter scene 4 generation. Format: google://gemini-2.5-flash, ollama://model@host:port, or openrouter://model",
    )
    chapter_revision_model: str = Field(
        "ollama://qwen3:latest@localhost:11434",
        alias="chapter-revision-model",
        description="Model URI for chapter-level revision. Format: google://gemini-2.5-flash, ollama://model@host:port, or openrouter://model",
    )
    revision_model: str = Field(
        "ollama://qwen3:latest@localhost:11434",
        alias="revision-model",
        description="Model URI for final story-level revision. Format: google://gemini-2.5-flash, ollama://model@host:port, or openrouter://model",
    )
    eval_model: str = Field(
        "ollama://qwen3:latest@localhost:11434",
        alias="eval-model",
        description="Model URI for evaluation. Format: google://gemini-2.5-flash, ollama://model@host:port, or openrouter://model",
    )
    info_model: str = Field(
        "ollama://qwen3:latest@localhost:11434",
        alias="info-model",
        description="Model URI for information extraction. Format: google://gemini-2.5-flash, ollama://model@host:port, or openrouter://model",
    )
    scrub_model: str = Field(
        "ollama://qwen3:latest@localhost:11434",
        alias="scrub-model",
        description="Model URI for content scrubbing. Format: google://gemini-2.5-flash, ollama://model@host:port, or openrouter://model",
    )
    checker_model: str = Field(
        "ollama://qwen3:latest@localhost:11434",
        alias="checker-model",
        description="Model URI for content checking. Format: google://gemini-2.5-flash, ollama://model@host:port, or openrouter://model",
    )
    translator_model: str = Field(
        "ollama://qwen3:latest@localhost:11434",
        alias="translator-model",
        description="Model URI for translation. Format: google://gemini-2.5-flash, ollama://model@host:port, or openrouter://model",
    )
    # Knowledge Base / RAG
    knowledge_base_path: Optional[str] = Field(
        "",
        alias="knowledge-base-path",
        description="The file path to a directory containing Markdown files that make up the knowledge base. Requires: pip install 'storytelling[rag]'",
    )
    embedding_model: Optional[str] = Field(
        "",
        alias="embedding-model",
        description="The model to be used for creating text embeddings.",
    )
    ollama_base_url: str = Field(
        "http://localhost:11434",
        alias="ollama-base-url",
        description="Base URL for Ollama API server.",
    )
    # Outline-level RAG configuration
    outline_rag_enabled: bool = Field(
        True,
        alias="outline-rag-enabled",
        description="Enable RAG context injection during outline generation.",
    )
    outline_context_max_tokens: int = Field(
        1000,
        alias="outline-context-max-tokens",
        description="Maximum tokens for outline-stage RAG context.",
    )
    outline_rag_top_k: int = Field(
        5,
        alias="outline-rag-top-k",
        description="Number of documents to retrieve per query for outline stage.",
    )
    outline_rag_similarity_threshold: float = Field(
        0.7,
        alias="outline-rag-similarity-threshold",
        description="Minimum similarity threshold for outline-stage document retrieval.",
    )
    # Chapter-level RAG configuration
    chapter_rag_enabled: bool = Field(
        True,
        alias="chapter-rag-enabled",
        description="Enable RAG context injection during chapter generation.",
    )
    chapter_context_max_tokens: int = Field(
        1500,
        alias="chapter-context-max-tokens",
        description="Maximum tokens for chapter-stage RAG context.",
    )
    chapter_rag_top_k: int = Field(
        8,
        alias="chapter-rag-top-k",
        description="Number of documents to retrieve per query for chapter stage.",
    )
    # Workflow Control
    expand_outline: bool = Field(True, alias="expand-outline")
    enable_final_edit_pass: bool = Field(False, alias="enable-final-edit-pass")
    no_scrub_chapters: bool = Field(False, alias="no-scrub-chapters")
    scene_generation_pipeline: bool = Field(True, alias="scene-generation-pipeline")
    # Revision and Quality Control
    outline_min_revisions: int = Field(1, alias="outline-min-revisions")
    outline_max_revisions: int = Field(3, alias="outline-max-revisions")
    chapter_min_revisions: int = Field(1, alias="chapter-min-revisions")
    chapter_max_revisions: int = Field(3, alias="chapter-max-revisions")
    no_chapter_revision: bool = Field(False, alias="no-chapter-revision")
    # Translation
    translate: Optional[str] = Field("", alias="translate")
    translate_prompt: Optional[str] = Field("", alias="translate-prompt")
    # Style Glossary for buzz term revision
    style_glossary_path: Optional[str] = Field(
        "",
        alias="style-glossary",
        description="Path to YAML file defining terms to avoid, preferred alternatives, and tone guidance.",
    )
    style_glossary: Optional[StyleGlossary] = Field(
        default=None,
        description="Loaded style glossary configuration (internal use).",
    )
    enable_buzz_term_revision: bool = Field(
        True,
        alias="enable-buzz-term-revision",
        description="Enable automatic detection and replacement of overused/cliché terms.",
    )
    # Miscellaneous
    seed: int = Field(12, alias="seed")
    sleep_time: int = Field(31, alias="sleep-time")
    debug: bool = Field(False, alias="debug")
    mock_mode: bool = Field(
        False,
        alias="mock-mode",
        description="Use mock responses instead of actual LLM calls for testing",
    )


def load_config(argv=None) -> WillWriteConfig:
    """
    Parses command-line arguments and loads them into a WillWriteConfig object.

    Args:
        argv: Optional list of arguments to parse. If None, uses sys.argv.
    """
    parser = argparse.ArgumentParser(
        description="WillWrite: A RISE-Based Story Generation Application",
        epilog="""Session Management Commands:
  --list-sessions           List available sessions
  --session-info SESSION_ID Show information about a session
  --resume SESSION_ID       Resume from session ID
  --resume-from-node NODE   Resume from specific node
  --migrate-session ID      Migrate existing session to new format

Style Glossary Commands:
  --init-style-glossary [PATH]  Create a sample style glossary file
  --style-glossary PATH         Use custom style glossary for buzz term revision

Examples:
  storytelling --prompt story.txt --output my_story
  storytelling --init-style-glossary my_glossary.yaml
  storytelling --prompt story.txt --style-glossary my_glossary.yaml
  storytelling --list-sessions
  storytelling --resume 2025-08-30_07-01-28-679308""",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    
    # Add special command for initializing style glossary
    parser.add_argument(
        "--init-style-glossary",
        nargs="?",
        const="style_glossary.yaml",
        metavar="PATH",
        help="Create a sample style glossary file at the specified path (default: style_glossary.yaml)",
    )
    
    # Add arguments from the Pydantic model
    for field_name, model_field in WillWriteConfig.model_fields.items():
        # Skip internal fields that shouldn't be CLI args
        if field_name == "style_glossary":
            continue
        alias = model_field.alias
        field_type = model_field.annotation
        default = model_field.default
        if field_type is bool:
            parser.add_argument(
                f"--{alias}",
                dest=field_name,
                action=argparse.BooleanOptionalAction,
                default=default,
                help=model_field.description,
            )
        else:
            parser.add_argument(
                f"--{alias}",
                dest=field_name,
                type=str,  # All CLI args are strings initially
                default=default,
                help=model_field.description,
                required=model_field.is_required(),
            )
    args = parser.parse_args(argv)
    
    # Handle --init-style-glossary command
    if args.init_style_glossary:
        _create_sample_glossary(args.init_style_glossary)
        sys.exit(0)
    
    args_dict = vars(args)
    # Pydantic V2 requires aliases to be used when instantiating a model from a dictionary
    config_dict = {}
    for field_name, model_field in WillWriteConfig.model_fields.items():
        if field_name == "style_glossary":
            continue
        if field_name in args_dict:
            config_dict[model_field.alias] = args_dict[field_name]
    # Create the config object, which will handle type conversion and validation
    config = WillWriteConfig(**config_dict)
    
    # Load style glossary if path provided
    if config.style_glossary_path:
        try:
            config.style_glossary = load_style_glossary(config.style_glossary_path)
            print(f"Loaded style glossary from: {config.style_glossary_path}")
            print(f"  - {len(config.style_glossary.avoid_terms)} terms to avoid")
            print(f"  - {len(config.style_glossary.custom_avoid_phrases)} custom phrases to avoid")
        except Exception as e:
            print(f"Warning: Could not load style glossary: {e}")
            config.style_glossary = get_default_glossary()
    elif config.enable_buzz_term_revision:
        # Use default glossary if buzz term revision is enabled but no custom glossary
        config.style_glossary = get_default_glossary()
    
    return config


def _create_sample_glossary(output_path: str) -> None:
    """Create a sample style glossary file."""
    # Get the template path
    template_path = os.path.join(
        os.path.dirname(__file__), "templates", "style_glossary_sample.yaml"
    )
    
    if os.path.exists(template_path):
        # Copy from template
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
    else:
        # Generate default content
        content = """# Style Glossary for Storytelling
# Use with: storytelling --style-glossary path/to/this/file.yaml

avoid_terms:
  - gap
  - journey
  - leverage
  - synergy
  - very
  - really
  - just
  - basically
  - amazing
  - incredible

preferred_alternatives:
  gap:
    - distance
    - divide
    - separation
  journey:
    - path
    - progression
    - evolution
  very:
    - extremely
    - remarkably

custom_avoid_phrases:
  - "at the end of the day"
  - "moving forward"
  - "it was then that"
  - "suddenly realized"

enforcement_level: moderate
"""
    
    # Write to output path
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✓ Created sample style glossary: {output_path}")
    print("  Edit this file to customize terms to avoid and preferred alternatives.")
    print(f"  Usage: storytelling --prompt your_story.txt --style-glossary {output_path}")


if __name__ == "__main__":
    # Example of how to load and print the configuration
    try:
        config = load_config()
        print("Configuration loaded successfully:")
        print(config.model_dump_json(indent=2))
    except Exception as e:
        print(f"Error loading configuration: {e}")
