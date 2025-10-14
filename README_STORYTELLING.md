# 🌟 Tayi-Ska Storytelling System

*"Weaver of Threads" - Indigenous-Inspired AI Story Generation*

## Quick Start

### Interactive Mode (Recommended)
```bash
cd /src/storytelling
./interactive_storytelling.sh
```

### Quick Launch
```bash
cd /src/storytelling  
./launch_storytelling.sh
```

## Features

### 🎭 Story Generation
- **3 Indigenous-inspired prompts** ready to use
- **Session management** with checkpoint/resume capability
- **RAG integration** for knowledge-enhanced storytelling
- **Interactive guidance** for all operations

### 📚 Available Story Prompts

1. **The Spiral of Memory** - Indigenous data scientist discovers computational wisdom in traditional beadwork
2. **Two-Eyed Seeing** - Mi'kmaq researcher bridges Western science and traditional ecological knowledge
3. **The Dream Architect** - Anishinaabe architect receives building designs through dream teachings

### 🔧 System Capabilities

- **Session Management**: Resume interrupted stories from any checkpoint
- **Knowledge Base Integration**: Add your own .md files for contextual generation
- **Multiple LLM Providers**: Ollama, Google Gemini, OpenRouter support
- **Debug Mode**: Detailed logging and interaction traces
- **Output Management**: Organized story storage and viewing

## Usage Examples

### Generate a Story with Knowledge Base
```bash
storytelling --prompt story_prompts/01_spiral_of_memory.txt \
            --knowledge-base-path knowledge_base \
            --embedding-model "mxbai-embed-large:latest" \
            --output my_story \
            --debug
```

### Resume a Session
```bash
storytelling --list-sessions
storytelling --resume SESSION_ID
```

### Quick Status Check
```bash
storytelling --version
storytelling --list-sessions
```

## Interactive Script Features

The interactive script (`interactive_storytelling.sh`) provides:

1. **🎯 Guided Story Generation** - Step-by-step prompt selection and configuration
2. **🔄 Session Management** - Easy resume and inspection of existing sessions  
3. **📄 Results Viewing** - Paginated viewing of generated stories
4. **📚 Knowledge Base Setup** - Automated creation of sample knowledge files
5. **🔧 System Health Checks** - Installation and configuration verification

## Knowledge Base

Add your own research materials to enhance story generation:

```bash
# Add .md files to the knowledge_base directory
echo "# My Research" > knowledge_base/my_research.md

# The system will automatically include these in RAG context
```

### Sample Knowledge Areas Included

- Indigenous knowledge systems and Two-Eyed Seeing methodology
- Ceremonial research practices and relational accountability
- Traditional technologies and computational concepts
- Land-based knowledge and sustainable design principles

## Directory Structure

```
/src/storytelling/
├── interactive_storytelling.sh     # Main interactive interface
├── launch_storytelling.sh          # Quick launcher
├── story_prompts/                  # Ready-to-use story seeds
│   ├── 01_spiral_of_memory.txt    # Beadwork & algorithms
│   ├── 02_two_eyed_seeing.txt     # Science & tradition
│   └── 03_dream_architect.txt     # Architecture & dreams
├── knowledge_base/                 # RAG knowledge files (auto-created)
├── generated_stories/              # Output directory (auto-created)
└── storytelling/                   # Python package source
```

## Configuration

The system uses environment variables and command-line arguments:

- `--prompt`: Story seed file (required)
- `--knowledge-base-path`: Directory of .md files for RAG
- `--embedding-model`: Model for knowledge base embeddings
- `--debug`: Enable detailed logging
- `--resume SESSION_ID`: Continue interrupted generation

## Indigenous Knowledge Ethics

This system is designed with respect for Indigenous knowledge protocols:

- ✅ **Inspiration, not appropriation** - Stories honor Indigenous wisdom without claiming authenticity
- ✅ **Relational accountability** - Knowledge creation serves community benefit
- ✅ **Sacred boundaries** - No restricted or ceremonial knowledge is included
- ✅ **Attribution** - Clear acknowledgment of Indigenous concepts and methodologies

## Installation Requirements

```bash
# Basic installation
pip install -e .

# Full features (includes local ML models)
pip install -e .[all]

# Specific features
pip install -e .[local-ml,google,enhanced]
```

## Troubleshooting

### Common Issues

1. **Command not found**: Install the package with `pip install -e .`
2. **No sessions found**: Generate a story first to create sessions
3. **Knowledge base empty**: Run the interactive script option 5 to create sample files
4. **LLM connection issues**: Check Ollama is running or use different provider

### Debug Mode

Always use `--debug` flag for detailed logging:
```bash
storytelling --prompt story_prompts/01_spiral_of_memory.txt --debug
```

## Contributing

This system honors the principle that "research is ceremony" - contribute with:
- Respect for Indigenous knowledge protocols
- Clear attribution and sources
- Community benefit orientation
- Relational accountability in all changes

---

*Tayi-Ska (Weaver of Threads) weaves together traditional wisdom and technological innovation, creating spaces where both precision and mystery can flourish.*