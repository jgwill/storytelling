"""Storytelling - AI-powered narrative generation system implementing Software 3.0 methodology."""

__version__ = "0.2.0"
__author__ = "JGWill"
__email__ = "jgwill@example.com"
__description__ = "AI-powered narrative generation system implementing Software 3.0 methodology - The Soul of Your Story's Blueprint"

# Core modules
from .config import WillWriteConfig, load_config
from .core import Story
from .data_models import (
    ChapterCount,
    CompletionCheck,
    SceneList,
    StoryInfo,
    SummaryCheck,
)
from .llm_providers import get_llm_from_uri
from .logger import Logger

# RAG and knowledge base
from .rag import get_embedding_model, initialize_knowledge_base
from .session_manager import SessionCheckpoint, SessionInfo, SessionManager

# Advanced features (optional imports with graceful degradation)
try:
    from .coaia_fuse import CoAiaFuseIntegrator
    from .enhanced_rag import EnhancedRAGSystem, create_enhanced_knowledge_base
    from .web_fetcher import WebContentFetcher, fetch_urls_from_scratchpad

    ENHANCED_FEATURES = True
except ImportError:
    ENHANCED_FEATURES = False

# IAIP integration (optional imports with graceful degradation)
try:
    from .ceremonial_diary import (
        CeremonialDiary,
        CeremonialPhaseEnum,
        DiaryEntry,
        DiaryManager,
        EntryTypeEnum,
    )
    from .iaip_bridge import (
        CeremonialPhase,
        NorthDirectionStoryteller,
        TwoEyedSeeingStorytellingAdapter,
        create_north_direction_session_metadata,
        export_storytelling_wisdom_to_iaip,
    )

    IAIP_INTEGRATION = True
except ImportError:
    IAIP_INTEGRATION = False

# Graph workflow (may not be available in all installations)
try:
    from .graph import StoryState, create_graph, create_resume_graph

    GRAPH_AVAILABLE = True
except ImportError:
    GRAPH_AVAILABLE = False

__all__ = [
    # Core
    "Story",
    "WillWriteConfig",
    "load_config",
    "SessionManager",
    "SessionInfo",
    "SessionCheckpoint",
    "Logger",
    "get_llm_from_uri",
    # Data models
    "ChapterCount",
    "CompletionCheck",
    "SummaryCheck",
    "StoryInfo",
    "SceneList",
    # RAG
    "initialize_knowledge_base",
    "get_embedding_model",
    # Metadata
    "__version__",
    "ENHANCED_FEATURES",
    "GRAPH_AVAILABLE",
    "IAIP_INTEGRATION",
]

# Add enhanced features to exports if available
if ENHANCED_FEATURES:
    __all__.extend(
        [
            "EnhancedRAGSystem",
            "create_enhanced_knowledge_base",
            "WebContentFetcher",
            "fetch_urls_from_scratchpad",
            "CoAiaFuseIntegrator",
        ]
    )

# Add graph features to exports if available
if GRAPH_AVAILABLE:
    __all__.extend(["create_graph", "create_resume_graph", "StoryState"])

# Add IAIP features to exports if available
if IAIP_INTEGRATION:
    __all__.extend(
        [
            "NorthDirectionStoryteller",
            "TwoEyedSeeingStorytellingAdapter",
            "CeremonialPhase",
            "create_north_direction_session_metadata",
            "export_storytelling_wisdom_to_iaip",
            "DiaryEntry",
            "CeremonialDiary",
            "DiaryManager",
            "CeremonialPhaseEnum",
            "EntryTypeEnum",
        ]
    )
