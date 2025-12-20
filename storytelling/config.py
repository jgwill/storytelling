import argparse
from typing import Optional

from pydantic import BaseModel, Field


class WillWriteConfig(BaseModel):
    """
    Configuration for the WillWrite application, validated with Pydantic.
    """

    # Core Parameters
    prompt_file: str = Field(
        ...,
        alias="prompt",
        description="The file path to the initial user prompt for the story.",
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
    # Miscellaneous
    seed: int = Field(12, alias="seed")
    sleep_time: int = Field(31, alias="sleep-time")
    debug: bool = Field(False, alias="debug")
    mock_mode: bool = Field(
        False,
        alias="mock-mode",
        description="Use mock responses instead of actual LLM calls for testing",
    )


def load_config() -> WillWriteConfig:
    """
    Parses command-line arguments and loads them into a WillWriteConfig object.
    """
    parser = argparse.ArgumentParser(
        description="WillWrite: A RISE-Based Story Generation Application",
        epilog="""Session Management Commands:
  --list-sessions           List available sessions
  --session-info SESSION_ID Show information about a session
  --resume SESSION_ID       Resume from session ID
  --resume-from-node NODE   Resume from specific node
  --migrate-session ID      Migrate existing session to new format
Examples:
  storytelling --prompt story.txt --output my_story
  storytelling --list-sessions
  storytelling --resume 2025-08-30_07-01-28-679308""",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    # Add arguments from the Pydantic model
    for field_name, model_field in WillWriteConfig.model_fields.items():
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
    args = parser.parse_args()
    args_dict = vars(args)
    # Pydantic V2 requires aliases to be used when instantiating a model from a dictionary
    config_dict = {}
    for field_name, model_field in WillWriteConfig.model_fields.items():
        if field_name in args_dict:
            config_dict[model_field.alias] = args_dict[field_name]
    # Create the config object, which will handle type conversion and validation
    config = WillWriteConfig(**config_dict)
    return config


if __name__ == "__main__":
    # Example of how to load and print the configuration
    try:
        config = load_config()
        print("Configuration loaded successfully:")
        print(config.model_dump_json(indent=2))
    except Exception as e:
        print(f"Error loading configuration: {e}")
