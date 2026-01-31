"""Storytelling - AI-powered narrative generation system implementing Software 3.0 methodology."""

__version__ = "1.0.0"
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

# Narrative Intelligence Integration (NCP-aware story generation)
try:
    from .narrative_intelligence_integration import (
        StoryBeat,
        ArcPoint,
        RelationshipState,
        CharacterArcState,
        EmotionalAnalysis,
        Gap,
        NCPState,
        NCPAwareStoryGenerator,
        CharacterArcTracker,
    )
    from .emotional_beat_enricher import (
        EmotionalBeatEnricher,
        QualityThreshold,
        EnrichedBeatResult,
        ENRICHMENT_TECHNIQUES,
    )
    from .analytical_feedback_loop import (
        AnalyticalFeedbackLoop,
        GapType,
        GapSeverity,
        GapDimension,
        MultiDimensionalAnalysis,
        FlowRoute,
        Enrichment,
    )

    NCP_INTEGRATION = True
except ImportError:
    NCP_INTEGRATION = False

# Add NCP integration features to exports if available
if NCP_INTEGRATION:
    __all__.extend(
        [
            # Narrative Intelligence
            "StoryBeat",
            "ArcPoint",
            "RelationshipState",
            "CharacterArcState",
            "EmotionalAnalysis",
            "Gap",
            "NCPState",
            "NCPAwareStoryGenerator",
            "CharacterArcTracker",
            # Emotional Beat Enricher
            "EmotionalBeatEnricher",
            "QualityThreshold",
            "EnrichedBeatResult",
            "ENRICHMENT_TECHNIQUES",
            # Analytical Feedback Loop
            "AnalyticalFeedbackLoop",
            "GapType",
            "GapSeverity",
            "GapDimension",
            "MultiDimensionalAnalysis",
            "FlowRoute",
            "Enrichment",
            # Metadata
            "NCP_INTEGRATION",
        ]
    )

# Narrative Story Graph (LangGraph-style orchestration)
try:
    from .narrative_story_graph import (
        NarrativeAwareStoryGraph,
        GraphState,
        NodeResult,
        NodeStatus,
        create_narrative_story_graph,
    )

    NARRATIVE_GRAPH_AVAILABLE = True
except ImportError:
    NARRATIVE_GRAPH_AVAILABLE = False

if NARRATIVE_GRAPH_AVAILABLE:
    __all__.extend(
        [
            "NarrativeAwareStoryGraph",
            "GraphState",
            "NodeResult",
            "NodeStatus",
            "create_narrative_story_graph",
            "NARRATIVE_GRAPH_AVAILABLE",
        ]
    )

# Role-Based Tooling (per storytelling-roles-tooling.rispec.md)
try:
    from .role_tooling import (
        # Enums
        Role,
        # Universe is already defined elsewhere, using RoleUniverse alias
        # Data classes
        Tool,
        RoleSession,
        # Registry
        ToolRegistry,
        register_tool,
        get_tools_for_role,
        # Role interfaces
        RoleInterface,
        ArchitectInterface,
        StructuristInterface,
        StorytellerInterface,
        EditorInterface,
        ReaderInterface,
        CollaboratorInterface,
        WitnessInterface,
        # Factory
        create_role_interface,
        # Constants
        ROLE_UNIVERSE_MAP,
    )

    ROLE_TOOLING_AVAILABLE = True
except ImportError:
    ROLE_TOOLING_AVAILABLE = False

if ROLE_TOOLING_AVAILABLE:
    __all__.extend(
        [
            # Enums
            "Role",
            # Data classes
            "Tool",
            "RoleSession",
            # Registry
            "ToolRegistry",
            "register_tool",
            "get_tools_for_role",
            # Role interfaces
            "RoleInterface",
            "ArchitectInterface",
            "StructuristInterface",
            "StorytellerInterface",
            "EditorInterface",
            "ReaderInterface",
            "CollaboratorInterface",
            "WitnessInterface",
            # Factory
            "create_role_interface",
            # Constants
            "ROLE_UNIVERSE_MAP",
            # Metadata
            "ROLE_TOOLING_AVAILABLE",
        ]
    )

# Narrative Tracing (Langfuse integration)
try:
    from .narrative_tracing import (
        StorytellingTracer,
        TraceContext,
        STORYTELLING_EVENT_TYPES,
        get_tracer,
        reset_tracer,
        HAS_NARRATIVE_TRACING,
    )

    TRACING_AVAILABLE = True
except ImportError:
    TRACING_AVAILABLE = False
    HAS_NARRATIVE_TRACING = False

if TRACING_AVAILABLE:
    __all__.extend(
        [
            "StorytellingTracer",
            "TraceContext",
            "STORYTELLING_EVENT_TYPES",
            "get_tracer",
            "reset_tracer",
            "TRACING_AVAILABLE",
            "HAS_NARRATIVE_TRACING",
        ]
    )
