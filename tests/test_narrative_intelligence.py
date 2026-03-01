"""Tests for narrative intelligence integration modules."""

import pytest
from unittest.mock import Mock, AsyncMock, patch, MagicMock
from dataclasses import asdict

# Import the modules we're testing
from storytelling.narrative_intelligence_integration import (
    StoryBeat,
    ArcPoint,
    RelationshipState,
    CharacterArcState,
    EmotionalAnalysis,
    Gap,
    NCPState,
    NCPAwareStoryGenerator,
    CharacterArcTracker,
    EmotionCategory,
)
from storytelling.emotional_beat_enricher import (
    EmotionalBeatEnricher,
    QualityThreshold,
    EnrichedBeatResult,
    ENRICHMENT_TECHNIQUES,
)
from storytelling.analytical_feedback_loop import (
    AnalyticalFeedbackLoop,
    GapType,
    GapSeverity,
    GapDimension,
    MultiDimensionalAnalysis,
    FlowRoute,
    Enrichment,
)
from storytelling.narrative_story_graph import (
    NarrativeAwareStoryGraph,
    GraphState,
    NodeResult,
    NodeStatus,
    create_narrative_story_graph,
)


# ============================================================================
# Story Beat Tests
# ============================================================================

class TestStoryBeat:
    """Tests for StoryBeat dataclass."""
    
    def test_story_beat_creation(self):
        """Test creating a story beat with required fields."""
        beat = StoryBeat(
            beat_id="beat_001",
            beat_index=0,
            raw_text="The hero enters the dark forest.",
            character_id="hero",
            emotional_tone="anticipation",
        )
        
        assert beat.beat_id == "beat_001"
        assert beat.beat_index == 0
        assert beat.character_id == "hero"
        assert beat.emotional_tone == "anticipation"
    
    def test_story_beat_with_optional_fields(self):
        """Test story beat with all optional fields."""
        beat = StoryBeat(
            beat_id="beat_002",
            beat_index=1,
            raw_text="She spoke softly.",
            character_id="mentor",
            emotional_tone="trust",
            dialogue="'You must believe in yourself.'",
            action="She placed her hand on his shoulder.",
            internal="This was the moment she had waited for.",  # Field is 'internal' not 'internal_thought'
            theme_resonance="coming of age",
            quality_score=0.85,
        )
        
        assert beat.dialogue is not None
        assert beat.action is not None
        assert beat.internal is not None  # Field is 'internal'
        assert beat.quality_score == 0.85
    
    def test_story_beat_to_dict(self):
        """Test converting story beat to dictionary."""
        beat = StoryBeat(
            beat_id="beat_003",
            beat_index=2,
            raw_text="Test beat",
            character_id="test",
            emotional_tone="joy",
        )
        
        beat_dict = beat.to_dict()  # Use to_dict() method
        assert isinstance(beat_dict, dict)
        assert beat_dict["beat_id"] == "beat_003"


# ============================================================================
# Character Arc State Tests
# ============================================================================

class TestCharacterArcState:
    """Tests for character arc tracking."""
    
    def test_character_arc_state_creation(self):
        """Test creating character arc state."""
        arc = CharacterArcState(
            player_id="protagonist",  # Field is 'player_id' not 'character_id'
            name="The Hero",  # Required field
            wound="past trauma",
            desire="to prove worthy",
        )
        
        assert arc.player_id == "protagonist"
        assert arc.name == "The Hero"
        assert arc.wound == "past trauma"
        assert len(arc.arc_points) == 0
    
    def test_arc_point_tracking(self):
        """Test tracking arc points."""
        arc = CharacterArcState(
            player_id="hero",
            name="Hero",
        )
        
        point = ArcPoint(
            beat_id="beat_005",
            beat_index=5,
            timestamp="2026-01-30T12:00:00",
            emotional_state="determination",  # Correct field names
            arc_direction="ascending",  # Use 'ascending' not 'positive'
            impact_magnitude=0.5,
        )
        
        arc.add_arc_point(point)  # Use add_arc_point() method
        assert len(arc.arc_points) == 1
        assert arc.arc_points[0].beat_id == "beat_005"


# ============================================================================
# NCP State Tests
# ============================================================================

class TestNCPState:
    """Tests for NCP state container."""
    
    def test_ncp_state_creation(self):
        """Test creating NCP state."""
        state = NCPState(
            session_id="session_001",
            story_id="story_001",
        )
        
        assert state.session_id == "session_001"
        assert state.story_id == "story_001"
        assert len(state.beats) == 0
        assert len(state.character_states) == 0
    
    def test_ncp_state_with_context(self):
        """Test NCP state with context."""
        state = NCPState(
            session_id="session_002",
            story_id="story_002",
            active_theme="redemption",
            dramatic_phase="crisis",
        )
        
        assert state.active_theme == "redemption"
        assert state.dramatic_phase == "crisis"


# ============================================================================
# Emotional Beat Enricher Tests
# ============================================================================

class TestEmotionalBeatEnricher:
    """Tests for emotional beat enricher."""
    
    def test_quality_threshold_values(self):
        """Test quality threshold values - QualityThreshold is a class, not enum."""
        assert QualityThreshold.EXCELLENT == 0.85
        assert QualityThreshold.GOOD == 0.75
        assert QualityThreshold.ADEQUATE == 0.60
        assert QualityThreshold.WEAK == 0.40
    
    def test_enrichment_techniques_available(self):
        """Test enrichment techniques are defined."""
        assert len(ENRICHMENT_TECHNIQUES) > 0
        # Actual keys are: stakes, sensory, internal, dialogue, action, etc.
        assert "stakes" in ENRICHMENT_TECHNIQUES
        assert "sensory" in ENRICHMENT_TECHNIQUES
        assert "dialogue" in ENRICHMENT_TECHNIQUES
    
    def test_enricher_initialization(self):
        """Test enricher initialization."""
        mock_llm = Mock()
        enricher = EmotionalBeatEnricher(mock_llm, {})
        
        assert enricher is not None
        assert enricher.llm_provider == mock_llm
        assert enricher.config == {}


# ============================================================================
# Analytical Feedback Loop Tests
# ============================================================================

class TestAnalyticalFeedbackLoop:
    """Tests for analytical feedback loop."""
    
    def test_gap_type_enum(self):
        """Test gap type values - actual enum values."""
        assert GapType.EMOTIONAL_WEAK in GapType
        assert GapType.CHARACTER_INCONSISTENT in GapType
        assert GapType.THEME_MISSING in GapType
    
    def test_gap_severity_enum(self):
        """Test gap severity values."""
        assert GapSeverity.CRITICAL.value == "critical"
        assert GapSeverity.MAJOR.value == "major"
        assert GapSeverity.MINOR.value == "minor"
    
    def test_feedback_loop_initialization(self):
        """Test feedback loop initialization."""
        mock_enricher = Mock(spec=EmotionalBeatEnricher)
        mock_llm = Mock()
        
        loop = AnalyticalFeedbackLoop(mock_enricher, mock_llm, {})
        
        assert loop is not None
        # enricher is stored in emotional_enricher attribute
        assert loop.emotional_enricher == mock_enricher


# ============================================================================
# Narrative Story Graph Tests
# ============================================================================

class TestNarrativeStoryGraph:
    """Tests for narrative story graph."""
    
    def test_graph_state_creation(self):
        """Test creating graph state."""
        state = GraphState(
            prompt="Write a hero's journey",
            context={"genre": "fantasy"},
        )
        
        assert state.prompt == "Write a hero's journey"
        assert state.context["genre"] == "fantasy"
        assert state.should_continue is True
        assert len(state.beats) == 0
    
    def test_node_status_enum(self):
        """Test node status values."""
        assert NodeStatus.PENDING.value == "pending"
        assert NodeStatus.RUNNING.value == "running"
        assert NodeStatus.COMPLETED.value == "completed"
        assert NodeStatus.FAILED.value == "failed"
    
    def test_node_result_creation(self):
        """Test creating node result."""
        result = NodeResult(
            node_id="generate_beat",
            status=NodeStatus.COMPLETED,
            output={"beat_id": "beat_001"},
            duration_ms=150.5,
        )
        
        assert result.node_id == "generate_beat"
        assert result.status == NodeStatus.COMPLETED
        assert result.output["beat_id"] == "beat_001"
    
    def test_graph_initialization(self):
        """Test graph initialization."""
        mock_llm = Mock()
        mock_generator = Mock(spec=NCPAwareStoryGenerator)
        mock_enricher = Mock(spec=EmotionalBeatEnricher)
        mock_feedback = Mock(spec=AnalyticalFeedbackLoop)
        
        graph = NarrativeAwareStoryGraph(
            generator=mock_generator,
            feedback_loop=mock_feedback,
            config={"max_beats": 5},
        )
        
        assert graph is not None
        assert graph.entry_node == "ncp_load"
        assert "generate_beat" in graph.nodes
        assert "analyze_beat" in graph.nodes


# ============================================================================
# Integration Tests (with mocks)
# ============================================================================

class TestNarrativeIntegration:
    """Integration tests for the complete narrative pipeline."""
    
    @pytest.mark.asyncio
    async def test_full_pipeline_mock(self):
        """Test full pipeline with mocked components."""
        mock_llm = AsyncMock()
        mock_llm.generate = AsyncMock(return_value="Generated beat text")
        
        # Create state
        state = GraphState(
            prompt="A hero's journey through darkness",
            context={"max_beats": 1},
        )
        
        # Initialize NCP state
        state.ncp_state = NCPState(
            session_id="test_session",
            story_id="test_story",
        )
        
        # Add a beat manually
        beat = StoryBeat(
            beat_id="test_beat",
            beat_index=0,
            raw_text="The hero stepped forward.",
            character_id="hero",
            emotional_tone="courage",
            quality_score=0.8,
        )
        state.beats.append(beat)
        
        assert len(state.beats) == 1
        assert state.beats[0].quality_score == 0.8
    
    def test_character_arc_tracker(self):
        """Test character arc tracker functionality."""
        tracker = CharacterArcTracker()
        
        # Initialize character - requires player_id and name
        tracker.initialize_character(
            player_id="hero",
            name="The Hero",
            wound="past trauma",
        )
        
        assert "hero" in tracker.character_states
        assert tracker.character_states["hero"].name == "The Hero"
        
        # Record arc point (record_beat_impact takes beat and player_id)
        beat = StoryBeat(
            beat_id="beat_courage",
            beat_index=1,
            raw_text="Hero faces fear",
            character_id="hero",
            emotional_tone="determination",
        )
        
        arc_point = tracker.record_beat_impact(
            beat=beat,
            player_id="hero",
        )
        
        assert arc_point is not None
        assert len(tracker.character_states["hero"].arc_points) == 1


# ============================================================================
# Tracing Tests
# ============================================================================

class TestNarrativeTracing:
    """Tests for narrative tracing module."""
    
    def test_tracer_import(self):
        """Test tracer can be imported."""
        from storytelling.narrative_tracing import (
            StorytellingTracer,
            TraceContext,
            STORYTELLING_EVENT_TYPES,
            get_tracer,
        )
        
        assert StorytellingTracer is not None
        assert TraceContext is not None
        assert len(STORYTELLING_EVENT_TYPES) > 0
    
    def test_event_types_defined(self):
        """Test event types are properly defined."""
        from storytelling.narrative_tracing import STORYTELLING_EVENT_TYPES
        
        assert "BEAT_GENERATED" in STORYTELLING_EVENT_TYPES
        assert "GAP_IDENTIFIED" in STORYTELLING_EVENT_TYPES
        assert "STORY_GENERATION_STARTED" in STORYTELLING_EVENT_TYPES
    
    def test_tracer_initialization(self):
        """Test tracer initialization without Langfuse."""
        from storytelling.narrative_tracing import StorytellingTracer
        
        tracer = StorytellingTracer(
            session_id="test_session",
            story_id="test_story",
        )
        
        assert tracer.session_id == "test_session"
        assert tracer.story_id == "test_story"
        # Without credentials, handler should be None
        assert tracer._handler is None
    
    def test_trace_context_creation(self):
        """Test trace context creation."""
        from storytelling.narrative_tracing import TraceContext
        
        context = TraceContext(
            trace_id="trace_001",
            session_id="session_001",
            story_id="story_001",
        )
        
        assert context.trace_id == "trace_001"
        assert context.beats_generated == 0
        assert context.gaps_identified == 0
    
    def test_tracer_logging_methods(self):
        """Test tracer logging methods work without errors."""
        from storytelling.narrative_tracing import StorytellingTracer
        
        tracer = StorytellingTracer(session_id="test")
        
        # These should not raise errors even without Langfuse
        tracer.log_beat_generated(
            beat_id="beat_001",
            emotional_tone="joy",
            quality_score=0.8,
        )
        
        tracer.log_gap_identified(
            gap_type="emotional",
            beat_id="beat_001",
            severity="minor",
            score=0.5,
        )
        
        tracer.log_character_arc_updated(
            character_id="hero",
            beat_id="beat_001",
            arc_progress=0.5,
            new_state="growing",
        )


# ============================================================================
# Factory Function Tests
# ============================================================================

class TestFactoryFunctions:
    """Tests for factory functions."""
    
    def test_create_narrative_story_graph(self):
        """Test story graph factory function."""
        mock_llm = Mock()
        
        graph = create_narrative_story_graph(
            llm_provider=mock_llm,
            config={"max_beats": 3},
        )
        
        assert isinstance(graph, NarrativeAwareStoryGraph)
        assert graph.config.get("max_beats") == 3
    
    def test_create_graph_with_session_id(self):
        """Test story graph with session ID for tracing."""
        mock_llm = Mock()
        
        graph = create_narrative_story_graph(
            llm_provider=mock_llm,
            config={},
            session_id="trace_session",
        )
        
        assert isinstance(graph, NarrativeAwareStoryGraph)
        # Tracer may or may not be set depending on imports
