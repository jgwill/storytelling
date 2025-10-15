# Tiered Package Architecture Specification

## Structural Tension
- **Desired Outcome**: Users create story generation workflows that match their technical environment and computational resources, from lightweight deployment to full-featured RAG-enhanced generation
- **Current Reality**: Heavy dependencies (sentence-transformers, torch ~3-5GB) force all users to install complete ML stack even for basic story generation
- **Natural Progression**: Tiered package architecture that enables users to create appropriate installation footprint for their specific creative and technical needs

## Creative Advancement Pattern

### What This Architecture Enables Users to Create

#### **Tier 1: Core Creative Flow** (Lightweight ~50MB)
**Users create**:
- **Essential Story Generation**: Complete narratives using external LLM providers
- **Session-Managed Workflows**: Full PHOENIX_WEAVE continuation capabilities  
- **Portable Creative Environments**: Deploy anywhere without heavy ML dependencies
- **Fast Development Cycles**: Rapid installation and testing

#### **Tier 2: Knowledge-Enhanced Creation** (+RAG ~3-5GB) 
**Users create**:
- **Context-Aware Narratives**: Stories grounded in specific knowledge bases
- **Consistent World-Building**: RAG-enhanced character and setting continuity
- **Domain-Specific Stories**: Technical, historical, or specialized narrative generation
- **Local Embedding Control**: Privacy-focused knowledge integration

#### **Tier 3: Specialized Creative Environments** (Provider-Specific)
**Users create**:
- **Provider-Optimized Workflows**: Tailored integration with specific LLM services
- **GPU-Accelerated Generation**: High-performance local processing
- **Cloud-Integrated Pipelines**: Hybrid local/cloud creative workflows
- **Custom Model Integrations**: Specialized provider combinations

## Tiered Architecture Design

### Tier 1: Core + Basic RAG (`storytelling`)
**Creative Intent**: Enable complete story generation with lightweight RAG capabilities

**Size**: ~60MB  
**Target Users**: Full-featured story generation with cloud/Ollama embeddings

```toml
[project]
dependencies = [
    # Core Creative Infrastructure
    "pydantic>=2.0",              # Configuration and data validation
    "langchain>=0.1.0",           # LLM orchestration foundation
    "langgraph>=0.0.40",          # Workflow state management
    "langchain-community>=0.0.20", # Community provider support
    "langchain-openai>=0.0.8",    # OpenAI integration
    "langchain-ollama>=0.0.1",    # Ollama integration (~5MB)
    
    # Lightweight RAG Infrastructure
    "faiss-cpu>=1.7.4",          # Vector search (~10MB)
    
    # Session Management (PHOENIX_WEAVE)
    "python-dotenv>=1.0.0",       # Environment configuration
    "termcolor>=2.0.0",           # CLI user experience
]
```

**Complete Creative Capabilities**:
- ✅ Complete story generation pipeline
- ✅ LangGraph workflow orchestration  
- ✅ PHOENIX_WEAVE session management architecture
- ✅ Configuration and provider abstraction
- ✅ CLI interface with session commands
- ✅ All checkpoint and resume functionality
- ✅ **Full RAG/Knowledge base integration**
- ✅ **Ollama embeddings (local)**
- ✅ **OpenAI embeddings (cloud)**
- ✅ **FAISS vector search**
- ✅ **Document loading and chunking**
- ✅ **Context-aware generation**
- ❌ HuggingFace sentence-transformers (heavy PyTorch models)

### Tier 2: Heavy Local ML (`storytelling[local-ml]`)
**Creative Intent**: Enable offline HuggingFace model integration for specialized use cases

**Additional Size**: ~3-5GB  
**Target Users**: Offline generation, specialized embeddings, PyTorch ecosystem access

```toml
[project.optional-dependencies]
local-ml = [
    # Heavy PyTorch-based Models
    "sentence-transformers>=2.2.2",  # HuggingFace sentence transformers
    "langchain-huggingface>=0.0.1",  # Hugging Face integration
    
    # Note: unstructured removed as identified unused dependency
]
```

**Advanced Creative Capabilities**:
- ✅ **All Tier 1 capabilities** (full RAG already included)
- ✅ HuggingFace sentence-transformers models
- ✅ Offline embedding generation without external services
- ✅ Full PyTorch ecosystem access
- ✅ Specialized embedding models for domain-specific generation

### Tier 3: Provider & Performance Extensions
**Creative Intent**: Enable specialized creative environments

```toml
[project.optional-dependencies]
# Provider-Specific Optimizations
ollama = ["langchain-ollama>=0.0.1"]
google = ["langchain-google-genai>=0.0.6"] 
openrouter = ["langchain-openrouter>=0.0.1"]

# Performance Enhancements
gpu = ["faiss-gpu>=1.7.4"]              # GPU-accelerated vector search
performance = ["torch-audio", "transformers[torch]"]  # Optimized ML backends

# Cloud & Monitoring Integration  
cloud = [
    "langfuse>=2.0.0",    # LLM observability
    "openai>=1.0.0",      # Direct OpenAI integration
]

# Complete Installation
all = ["storytelling[rag,ollama,google,openrouter,gpu,cloud]"]
```

## Implementation Architecture

### Graceful Degradation Pattern
**Creative Intent**: Enable users to create stories regardless of installed dependencies

```python
# src/storytelling/rag.py - Enhanced with tiered architecture
try:
    from sentence_transformers import SentenceTransformer
    import faiss
    RAG_AVAILABLE = True
except ImportError:
    RAG_AVAILABLE = False
    SentenceTransformer = None
    faiss = None

class RAGCapabilityManager:
    """Manage RAG capabilities based on installed dependencies"""
    
    @classmethod
    def check_rag_availability(cls) -> dict:
        """Return detailed capability assessment"""
        return {
            "rag_available": RAG_AVAILABLE,
            "local_embeddings": SentenceTransformer is not None,
            "vector_search": faiss is not None,
            "installation_command": "pip install storytelling[rag]" if not RAG_AVAILABLE else None
        }
    
    @classmethod
    def require_rag(cls, feature_name: str):
        """Raise informative error when RAG features needed"""
        if not RAG_AVAILABLE:
            raise ImportError(
                f"{feature_name} requires RAG functionality. "
                f"Install with: pip install storytelling[rag]"
            )

def initialize_knowledge_base(knowledge_base_path: str, embedding_model: str, ollama_base_url: str):
    """Initialize knowledge base with graceful degradation"""
    
    # Check capabilities
    capabilities = RAGCapabilityManager.check_rag_availability()
    
    if not capabilities["rag_available"]:
        raise ImportError(
            "Knowledge base functionality requires RAG dependencies. "
            "Install with: pip install storytelling[rag]"
        )
    
    # Proceed with existing implementation
    return initialize_knowledge_base_impl(knowledge_base_path, embedding_model, ollama_base_url)
```

### Configuration Integration
**Creative Intent**: Enable users to create appropriate configurations for their installation tier

```python
# src/storytelling/config.py - Enhanced with tier awareness
@dataclass
class WillWriteConfig:
    # ... existing configuration fields
    
    # Tier Management
    rag_enabled: bool = Field(default=True, description="Enable RAG functionality if available")
    auto_detect_capabilities: bool = Field(default=True, description="Automatically detect installed capabilities")
    
    def __post_init__(self):
        """Validate configuration against installed capabilities"""
        if self.auto_detect_capabilities:
            capabilities = self._detect_capabilities()
            self._adjust_configuration(capabilities)
    
    def _detect_capabilities(self) -> dict:
        """Detect what functionality is available"""
        from .rag import RAGCapabilityManager
        return RAGCapabilityManager.check_rag_availability()
    
    def _adjust_configuration(self, capabilities: dict):
        """Adjust configuration based on available capabilities"""
        if not capabilities["rag_available"]:
            self.rag_enabled = False
            self.knowledge_base_path = None
            
        # Log capability adjustments
        if hasattr(self, 'logger'):
            self.logger.info(f"Detected capabilities: {capabilities}")
```

### Session Management Integration
**Creative Intent**: Session management works across all tiers

The PHOENIX_WEAVE session architecture works seamlessly across all tiers:

```python
# Session management tier compatibility
class SessionManager:
    def save_checkpoint(self, session_id: str, node_name: str, state: Dict[str, Any], metadata: Dict[str, Any] = None):
        """Save checkpoint with tier-aware capability preservation"""
        
        # Standard checkpoint saving (works across all tiers)
        checkpoint = SessionCheckpoint(...)
        
        # Tier-aware capability preservation
        if metadata is None:
            metadata = {}
        
        # Record which capabilities were active during checkpoint
        capabilities = self._detect_active_capabilities(state)
        metadata.update({
            "active_capabilities": capabilities,
            "tier_compatibility": self._assess_tier_requirements(capabilities)
        })
        
        checkpoint.metadata = metadata
        self._save_checkpoint_file(checkpoint)
    
    def _assess_tier_requirements(self, capabilities: dict) -> dict:
        """Determine minimum tier needed to resume this checkpoint"""
        tier_requirements = {"core": True}
        
        if capabilities.get("rag_used", False):
            tier_requirements["rag"] = True
            
        if capabilities.get("gpu_used", False):
            tier_requirements["gpu"] = True
            
        return tier_requirements
```

## Installation & Usage Patterns

### Core Installation (Tier 1)
```bash
# Essential story generation (~50MB)
pip install storytelling

# Verify capabilities
python -c "from src.storytelling.rag import RAGCapabilityManager; print(RAGCapabilityManager.check_rag_availability())"
```

**Creative Workflows Enabled**:
```bash
# Full story generation with external LLM providers
python -m src.storytelling.main --prompt story.txt --output my_story

# Complete session management
python -m src.storytelling.main --list-sessions
python -m src.storytelling.main --resume session_2025_08_30

# All PHOENIX_WEAVE functionality
python -m src.storytelling.main --session-info session_id
```

### RAG-Enhanced Installation (Tier 2)
```bash
# With knowledge base support (~3-5GB additional)
pip install storytelling[rag]

# Verify RAG capabilities
python -c "from src.storytelling.rag import initialize_knowledge_base; print('RAG Available')"
```

**Enhanced Creative Workflows**:
```bash
# Knowledge-enhanced generation
python -m src.storytelling.main --prompt story.txt --knowledge-base ./lore/ --output enhanced_story

# RAG-enhanced session resume
python -m src.storytelling.main --resume session_id --knowledge-base ./updated_lore/
```

### Specialized Installation (Tier 3)
```bash
# Provider-specific optimization
pip install storytelling[rag,ollama,gpu]

# Complete installation
pip install storytelling[all]
```

## Integration with Agent Architecture

### Agent-Tier Compatibility
The planned agent system (from `agents/` directory) benefits from tiered architecture:

#### **Tier 1 Agent Support**
- **Vision Agent**: Works with any LLM provider, no heavy dependencies
- **Architect Agent**: Structure generation without RAG requirements
- **Core Session Management**: Full agent checkpoint/resume capabilities

#### **Tier 2 Agent Enhancement**
- **RAG Agent**: Only available with `[rag]` installation
- **Knowledge-Enhanced Vision**: Context-aware story foundation
- **Consistent World-Building**: Agent-driven knowledge integration

#### **Tier 3 Agent Specialization**
- **Provider-Optimized Agents**: Specialized model integration
- **GPU-Accelerated Processing**: Performance-enhanced generation
- **Cloud-Integrated Workflows**: Hybrid agent orchestration

### Agent Command Tier Awareness
```bash
# Core agent functionality (all tiers)
/generate-story --prompt "story idea"
/continue-chapter --session session_id

# RAG-enhanced agent commands (Tier 2+)
/inject-knowledge --knowledge-base ./lore/
/generate-story --prompt "story idea" --with-context

# Specialized agent commands (Tier 3)
/generate-story --provider ollama --gpu-accelerated
/export-formats --cloud-storage --high-performance
```

## Migration & Upgrade Paths

### Existing User Migration
**For users with current full installation**:
```bash
# Maintain current behavior
pip install storytelling[all]

# Or migrate to minimal installation if RAG not needed
pip uninstall storytelling  
pip install storytelling  # Core only
```

### Incremental Adoption
**Natural progression for new users**:
1. **Start Core**: `pip install storytelling` → Test basic generation
2. **Add RAG**: `pip install storytelling[rag]` → Enable knowledge base
3. **Specialize**: Add provider-specific optimizations as needed

### Session Compatibility
**PHOENIX_WEAVE sessions work across tiers**:
- Sessions created with RAG can be resumed without RAG (with warnings)
- Core sessions can be enhanced by upgrading to RAG tier
- Tier requirements preserved in session metadata

## Success Metrics

### Installation Flexibility
- **50MB Core Package**: Essential story generation without heavy ML dependencies
- **Modular Growth**: Users add only needed functionality
- **Clear Capability Communication**: Users understand what each tier provides

### Creative Workflow Enablement
- **Tier 1**: Essential creative workflows for all users
- **Tier 2**: Enhanced creative capabilities for knowledge-intensive projects
- **Tier 3**: Specialized creative environments for advanced users

### System Architecture Benefits
- **Container Optimization**: Dramatically smaller images for basic functionality
- **CI/CD Efficiency**: Faster builds and deployments
- **Resource Management**: Appropriate computational resource allocation

## Implementation Status

### ✅ **Specification Complete**
- Tiered architecture design aligned with PHOENIX_WEAVE
- Graceful degradation patterns defined
- Session management tier compatibility specified
- Agent system integration planned

### 🔄 **Implementation Required**
- Move dependencies to optional groups in `pyproject.toml`
- Add graceful degradation to `rag.py`
- Update configuration with tier awareness
- Enhance session management with capability preservation
- Update documentation and installation guides

### ⏳ **Testing Strategy**
- Validate each tier installs correctly
- Test feature degradation gracefully
- Ensure session compatibility across tiers
- Verify agent functionality at each tier level

This tiered architecture specification integrates seamlessly with PHOENIX_WEAVE session management while addressing the heavy dependency problem identified in the tier separation plan. Users can now create appropriate creative environments for their specific needs without forced dependency installation.