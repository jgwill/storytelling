"""
Narrative-Aware Story Graph for Storytelling Package

LangGraph-style orchestration of NCP-aware story generation with
Three-Universe analysis, emotional enrichment, and analytical feedback.

Implements specification from:
- rispecs/Narrative_Aware_Story_Graph_Specification.md
- rispecs/ncp-schema.rispec.md
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Callable, TYPE_CHECKING
import uuid

from .narrative_intelligence_integration import (
    StoryBeat,
    CharacterArcState,
    NCPState,
    NCPAwareStoryGenerator,
    CharacterArcTracker,
)
from .emotional_beat_enricher import EmotionalBeatEnricher, EnrichedBeatResult
from .analytical_feedback_loop import (
    AnalyticalFeedbackLoop,
    MultiDimensionalAnalysis,
    Gap,
)

logger = logging.getLogger(__name__)


# ============================================================================
# Graph State
# ============================================================================

class NodeStatus(str, Enum):
    """Status of a graph node execution."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class NodeResult:
    """Result from a graph node execution."""
    node_id: str
    status: NodeStatus
    output: Any = None
    error: Optional[str] = None
    duration_ms: float = 0.0
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())


@dataclass
class GraphState:
    """
    Complete state for the narrative-aware story graph.
    
    This mirrors the UnifiedNarrativeState from the langgraph
    narrative-intelligence package.
    """
    # Identity
    graph_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    session_id: Optional[str] = None
    
    # Input
    prompt: str = ""
    context: Dict[str, Any] = field(default_factory=dict)
    
    # NCP State
    ncp_state: Optional[NCPState] = None
    
    # Generated content
    beats: List[StoryBeat] = field(default_factory=list)
    current_beat_index: int = 0
    
    # Analysis results
    analyses: List[MultiDimensionalAnalysis] = field(default_factory=list)
    gaps_identified: List[Gap] = field(default_factory=list)
    
    # Enrichment tracking
    enrichments_applied: int = 0
    
    # Node execution history
    node_results: List[NodeResult] = field(default_factory=list)
    
    # Routing
    next_node: Optional[str] = None
    should_continue: bool = True
    
    # Metadata
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    
    def update(self) -> None:
        """Update the timestamp."""
        self.updated_at = datetime.utcnow().isoformat()


# ============================================================================
# Graph Nodes
# ============================================================================

class GraphNode:
    """Base class for graph nodes."""
    
    def __init__(self, node_id: str):
        self.node_id = node_id
    
    async def execute(self, state: GraphState) -> GraphState:
        """Execute node logic. Override in subclasses."""
        raise NotImplementedError


class NCPLoadNode(GraphNode):
    """Load NCP context and initialize state."""
    
    def __init__(self, generator: NCPAwareStoryGenerator):
        super().__init__("ncp_load")
        self.generator = generator
    
    async def execute(self, state: GraphState) -> GraphState:
        """Load NCP context from provided data."""
        start_time = datetime.utcnow()
        
        try:
            # Initialize NCP state if not present
            if state.ncp_state is None:
                state.ncp_state = NCPState(
                    session_id=state.session_id or str(uuid.uuid4()),
                    story_id=state.context.get('story_id', str(uuid.uuid4())),
                    active_universe=state.context.get('universe'),
                    active_perspective=state.context.get('perspective'),
                    active_theme=state.context.get('theme'),
                )
            
            # Load any external NCP data
            if 'ncp_data' in state.context:
                ncp_data = state.context['ncp_data']
                if isinstance(ncp_data, dict):
                    state.ncp_state.ncp_metadata.update(ncp_data)
            
            duration = (datetime.utcnow() - start_time).total_seconds() * 1000
            state.node_results.append(NodeResult(
                node_id=self.node_id,
                status=NodeStatus.COMPLETED,
                output={'ncp_loaded': True},
                duration_ms=duration,
            ))
            state.next_node = "generate_beat"
            
        except Exception as e:
            logger.error(f"NCP load failed: {e}")
            state.node_results.append(NodeResult(
                node_id=self.node_id,
                status=NodeStatus.FAILED,
                error=str(e),
            ))
            state.should_continue = False
        
        state.update()
        return state


class BeatGenerationNode(GraphNode):
    """Generate a story beat using NCP-aware generator."""
    
    def __init__(self, generator: NCPAwareStoryGenerator):
        super().__init__("generate_beat")
        self.generator = generator
    
    async def execute(self, state: GraphState) -> GraphState:
        """Generate the next story beat."""
        start_time = datetime.utcnow()
        
        try:
            # Build generation context
            context = {
                'prompt': state.prompt,
                'beat_index': state.current_beat_index,
                'previous_beats': state.beats[-3:] if state.beats else [],
                **state.context,
            }
            
            # Generate beat
            beat = await self.generator.generate_beat(
                prompt=state.prompt,
                ncp_state=state.ncp_state,
                context=context,
            )
            
            state.beats.append(beat)
            state.current_beat_index += 1
            
            duration = (datetime.utcnow() - start_time).total_seconds() * 1000
            state.node_results.append(NodeResult(
                node_id=self.node_id,
                status=NodeStatus.COMPLETED,
                output={'beat_id': beat.beat_id, 'beat_index': beat.beat_index},
                duration_ms=duration,
            ))
            state.next_node = "analyze_beat"
            
        except Exception as e:
            logger.error(f"Beat generation failed: {e}")
            state.node_results.append(NodeResult(
                node_id=self.node_id,
                status=NodeStatus.FAILED,
                error=str(e),
            ))
            state.should_continue = False
        
        state.update()
        return state


class AnalysisNode(GraphNode):
    """Analyze generated beat for quality gaps."""
    
    def __init__(self, feedback_loop: AnalyticalFeedbackLoop):
        super().__init__("analyze_beat")
        self.feedback_loop = feedback_loop
    
    async def execute(self, state: GraphState) -> GraphState:
        """Analyze the latest beat."""
        start_time = datetime.utcnow()
        
        try:
            if not state.beats:
                state.next_node = "output"
                return state
            
            current_beat = state.beats[-1]
            
            # Process with analysis (includes auto-remediation)
            enriched_beat = await self.feedback_loop.process_beat_with_analysis(
                current_beat,
                state.ncp_state,
            )
            
            # Update beat in state
            state.beats[-1] = enriched_beat
            
            # Track enrichments
            if enriched_beat.enrichments_applied:
                state.enrichments_applied += len(enriched_beat.enrichments_applied)
            
            duration = (datetime.utcnow() - start_time).total_seconds() * 1000
            state.node_results.append(NodeResult(
                node_id=self.node_id,
                status=NodeStatus.COMPLETED,
                output={
                    'quality_score': enriched_beat.quality_score,
                    'enrichments': len(enriched_beat.enrichments_applied),
                },
                duration_ms=duration,
            ))
            
            # Route to next node
            state.next_node = self._route_next(state, enriched_beat)
            
        except Exception as e:
            logger.error(f"Analysis failed: {e}")
            state.node_results.append(NodeResult(
                node_id=self.node_id,
                status=NodeStatus.FAILED,
                error=str(e),
            ))
            # Continue even if analysis fails
            state.next_node = "output"
        
        state.update()
        return state
    
    def _route_next(self, state: GraphState, beat: StoryBeat) -> str:
        """Determine next node based on analysis."""
        max_beats = state.context.get('max_beats', 10)
        
        if state.current_beat_index >= max_beats:
            return "output"
        elif beat.quality_score < 0.5 and state.enrichments_applied < 3:
            # Low quality, try regeneration
            return "generate_beat"
        else:
            return "should_continue"


class ContinuationCheckNode(GraphNode):
    """Check if story generation should continue."""
    
    def __init__(self):
        super().__init__("should_continue")
    
    async def execute(self, state: GraphState) -> GraphState:
        """Determine if we should generate more beats."""
        
        max_beats = state.context.get('max_beats', 10)
        min_quality = state.context.get('min_quality', 0.6)
        
        # Check stopping conditions
        if state.current_beat_index >= max_beats:
            state.should_continue = False
            state.next_node = "output"
        elif state.beats and state.beats[-1].quality_score >= min_quality:
            # Good quality, check if story complete
            last_beat = state.beats[-1]
            if last_beat.emotional_tone in ['resolution', 'conclusion', 'ending']:
                state.should_continue = False
                state.next_node = "output"
            else:
                state.next_node = "generate_beat"
        else:
            state.next_node = "generate_beat"
        
        state.node_results.append(NodeResult(
            node_id=self.node_id,
            status=NodeStatus.COMPLETED,
            output={'continue': state.should_continue, 'next': state.next_node},
        ))
        
        state.update()
        return state


class OutputNode(GraphNode):
    """Finalize and output the generated story."""
    
    def __init__(self):
        super().__init__("output")
    
    async def execute(self, state: GraphState) -> GraphState:
        """Compile final output."""
        
        state.should_continue = False
        
        state.node_results.append(NodeResult(
            node_id=self.node_id,
            status=NodeStatus.COMPLETED,
            output={
                'total_beats': len(state.beats),
                'enrichments_applied': state.enrichments_applied,
            },
        ))
        
        state.update()
        return state


# ============================================================================
# Story Graph
# ============================================================================

class NarrativeAwareStoryGraph:
    """
    LangGraph-style orchestration for NCP-aware story generation.
    
    Implements the complete flow:
    1. Load NCP context
    2. Generate story beats
    3. Analyze for quality gaps
    4. Apply enrichments
    5. Continue or output
    """
    
    def __init__(
        self,
        generator: NCPAwareStoryGenerator,
        feedback_loop: AnalyticalFeedbackLoop,
        config: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize the story graph.
        
        Args:
            generator: NCP-aware story generator
            feedback_loop: Analytical feedback loop
            config: Graph configuration
        """
        self.generator = generator
        self.feedback_loop = feedback_loop
        self.config = config or {}
        
        # Initialize nodes
        self.nodes: Dict[str, GraphNode] = {
            'ncp_load': NCPLoadNode(generator),
            'generate_beat': BeatGenerationNode(generator),
            'analyze_beat': AnalysisNode(feedback_loop),
            'should_continue': ContinuationCheckNode(),
            'output': OutputNode(),
        }
        
        # Entry point
        self.entry_node = 'ncp_load'
        
        logger.info("NarrativeAwareStoryGraph initialized")
    
    async def run(
        self,
        prompt: str,
        context: Optional[Dict[str, Any]] = None,
        session_id: Optional[str] = None,
    ) -> GraphState:
        """
        Execute the story generation graph.
        
        Args:
            prompt: Story generation prompt
            context: Additional context
            session_id: Optional session ID for tracing
        
        Returns:
            Final graph state with generated story
        """
        # Initialize state
        state = GraphState(
            prompt=prompt,
            context=context or {},
            session_id=session_id,
        )
        
        # Apply config defaults
        if 'max_beats' not in state.context:
            state.context['max_beats'] = self.config.get('max_beats', 10)
        if 'min_quality' not in state.context:
            state.context['min_quality'] = self.config.get('min_quality', 0.6)
        
        # Start at entry node
        current_node = self.entry_node
        
        # Execute graph
        while state.should_continue and current_node:
            node = self.nodes.get(current_node)
            if not node:
                logger.error(f"Unknown node: {current_node}")
                break
            
            logger.debug(f"Executing node: {current_node}")
            state = await node.execute(state)
            current_node = state.next_node
        
        return state
    
    async def stream(
        self,
        prompt: str,
        context: Optional[Dict[str, Any]] = None,
        session_id: Optional[str] = None,
    ):
        """
        Stream story generation, yielding beats as they're created.
        
        Args:
            prompt: Story generation prompt
            context: Additional context
            session_id: Optional session ID
        
        Yields:
            Generated story beats
        """
        state = GraphState(
            prompt=prompt,
            context=context or {},
            session_id=session_id,
        )
        
        state.context.setdefault('max_beats', self.config.get('max_beats', 10))
        state.context.setdefault('min_quality', self.config.get('min_quality', 0.6))
        
        current_node = self.entry_node
        last_beat_count = 0
        
        while state.should_continue and current_node:
            node = self.nodes.get(current_node)
            if not node:
                break
            
            state = await node.execute(state)
            
            # Yield new beats
            while last_beat_count < len(state.beats):
                yield state.beats[last_beat_count]
                last_beat_count += 1
            
            current_node = state.next_node
    
    def add_node(self, node: GraphNode) -> None:
        """Add a custom node to the graph."""
        self.nodes[node.node_id] = node
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics from components."""
        return {
            'generator_stats': self.generator.get_statistics() if hasattr(self.generator, 'get_statistics') else {},
            'feedback_loop_stats': self.feedback_loop.get_statistics(),
        }


# ============================================================================
# Factory Functions
# ============================================================================

def create_narrative_story_graph(
    llm_provider: Any,
    config: Optional[Dict[str, Any]] = None,
) -> NarrativeAwareStoryGraph:
    """
    Factory function to create a configured NarrativeAwareStoryGraph.
    
    Args:
        llm_provider: LLM provider for generation
        config: Configuration options
    
    Returns:
        Configured story graph
    """
    config = config or {}
    
    # Create components
    generator = NCPAwareStoryGenerator(llm_provider, config)
    enricher = EmotionalBeatEnricher(llm_provider, config)
    feedback_loop = AnalyticalFeedbackLoop(enricher, llm_provider, config)
    
    # Create graph
    return NarrativeAwareStoryGraph(generator, feedback_loop, config)


# ============================================================================
# Module Exports
# ============================================================================

__all__ = [
    # Enums
    "NodeStatus",
    
    # Data classes
    "NodeResult",
    "GraphState",
    
    # Node classes
    "GraphNode",
    "NCPLoadNode",
    "BeatGenerationNode",
    "AnalysisNode",
    "ContinuationCheckNode",
    "OutputNode",
    
    # Main class
    "NarrativeAwareStoryGraph",
    
    # Factory
    "create_narrative_story_graph",
]
