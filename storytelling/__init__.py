"""Storytelling - AI-powered narrative generation system implementing Software 3.0 methodology."""

__version__ = "0.2.0"
__author__ = "JGWill"
__email__ = "jgwill@example.com"
__description__ = "AI-powered narrative generation system implementing Software 3.0 methodology - The Soul of Your Story's Blueprint"

# Core modules
from .core import Story
from .config import WillWriteConfig, load_config
from .session_manager import SessionManager, SessionInfo, SessionCheckpoint
from .logger import Logger
from .llm_providers import get_llm_from_uri
from .data_models import ChapterCount, CompletionCheck, SummaryCheck, StoryInfo, SceneList

# RAG and knowledge base
from .rag import initialize_knowledge_base, get_embedding_model

# Advanced features (optional imports with graceful degradation)
try:
    from .enhanced_rag import EnhancedRAGSystem, create_enhanced_knowledge_base
    from .web_fetcher import WebContentFetcher, fetch_urls_from_scratchpad
    from .coaia_fuse import CoAiaFuseIntegrator
    ENHANCED_FEATURES = True
except ImportError:
    ENHANCED_FEATURES = False

# IAIP integration (optional imports with graceful degradation)
try:
    from .iaip_bridge import (
        NorthDirectionStoryteller,
        TwoEyedSeeingStorytellingAdapter,
        CeremonialPhase,
        create_north_direction_session_metadata,
        export_storytelling_wisdom_to_iaip
    )
    from .ceremonial_diary import (
        DiaryEntry,
        CeremonialDiary,
        DiaryManager,
        CeremonialPhaseEnum,
        EntryTypeEnum
    )
    IAIP_INTEGRATION = True
except ImportError:
    IAIP_INTEGRATION = False

# Graph workflow (may not be available in all installations)
try:
    from .graph import create_graph, create_resume_graph, StoryState
    GRAPH_AVAILABLE = True
except ImportError:
    GRAPH_AVAILABLE = False

__all__ = [
    # Core
    "Story", "WillWriteConfig", "load_config",
    "SessionManager", "SessionInfo", "SessionCheckpoint",
    "Logger", "get_llm_from_uri",

    # Data models
    "ChapterCount", "CompletionCheck", "SummaryCheck", "StoryInfo", "SceneList",

    # RAG
    "initialize_knowledge_base", "get_embedding_model",

    # Metadata
    "__version__", "ENHANCED_FEATURES", "GRAPH_AVAILABLE", "IAIP_INTEGRATION"
]

# Add enhanced features to exports if available
if ENHANCED_FEATURES:
    __all__.extend([
        "EnhancedRAGSystem", "create_enhanced_knowledge_base",
        "WebContentFetcher", "fetch_urls_from_scratchpad", 
        "CoAiaFuseIntegrator"
    ])

# Add graph features to exports if available
if GRAPH_AVAILABLE:
    __all__.extend(["create_graph", "create_resume_graph", "StoryState"])

# Add IAIP features to exports if available
if IAIP_INTEGRATION:
    __all__.extend([
        "NorthDirectionStoryteller", "TwoEyedSeeingStorytellingAdapter",
        "CeremonialPhase", "create_north_direction_session_metadata",
        "export_storytelling_wisdom_to_iaip",
        "DiaryEntry", "CeremonialDiary", "DiaryManager",
        "CeremonialPhaseEnum", "EntryTypeEnum"
    ])
