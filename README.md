# Storytelling: Turn Your Ideas Into Complete Narratives

Transform a simple story idea into a fully-written, multi-chapter narrative. **WillWrite** is an AI-powered storytelling partner that handles the heavy lifting—outline generation, chapter planning, scene development, and revision—so you can focus on your creative vision.

## What It Does

**Create complete stories in minutes.** You provide a story prompt. The system generates:

- A structured outline with plot, characters, and themes
- Individual chapters with detailed chapter outlines
- Four polished scenes per chapter
- Multiple revision passes for consistency and quality
- Session persistence—pause and resume anytime

**Powered by advanced AI orchestration.** Built on LangGraph and LangChain with multi-LLM provider support, knowledge-base integration, and intelligent retrieval-augmented generation (RAG).

## Getting Started

### Installation

```bash
# Basic installation
pip install storytelling

# With full features (web fetching, local embeddings, cloud logging)
pip install storytelling[all]
```

### Your First Story

```bash
# Create a prompt file
echo "A detective discovers a mysterious library" > my_prompt.txt

# Generate your story
storytelling --prompt my_prompt.txt --output my_story.md
```

Your completed story appears in `my_story.md`.

### Using Your Own LLMs

```bash
# With local Ollama
storytelling --prompt prompt.txt \
  --initial-outline-model "ollama://mistral@localhost:11434"

# With Google Gemini
storytelling --prompt prompt.txt \
  --initial-outline-model "google://gemini-2.5-flash"
```

## Key Features

**Flexible AI Providers**
- Google (Gemini, PaLM)
- Ollama (local models)
- OpenRouter (community models)
- Custom endpoints

**Knowledge-Aware Generation**
- Integrate your own knowledge bases
- Web content retrieval
- Semantic context enhancement
- Consistent worldbuilding

**Session Management**
- Pause and resume at any stage
- Checkpoint-based recovery
- Narrative branching
- Full generation history

**Production Ready**
- Comprehensive logging with Langfuse
- Type-safe with Pydantic
- Configurable for various use cases
- Extensible architecture

## Command Line

```bash
storytelling --help                    # See all options
storytelling --prompt file.txt         # Generate story
storytelling --list-sessions           # See your past sessions
storytelling --resume <session-id>     # Continue a session
```

## Documentation

- **Full Setup Guide**: See `scripts/init.sh` for environment setup
- **Architecture**: Check `rispecs/` directory for detailed specifications
- **Specifications**: `RISPECS.md` contains implementation architecture
- **Prompts & Models**: `rispecs/Prompts.md` and `rispecs/LLM_Provider_Specification.md`

## Development

```bash
# Setup development environment
./scripts/init.sh

# Run tests
make test

# Check code quality
make lint

# Build and release
make release-check
```

## License

CC0-1.0 License - See [LICENSE](LICENSE)