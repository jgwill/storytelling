"""
Analytical Feedback Loop for Storytelling Package

This module provides closed-loop analysis that identifies quality gaps
and routes to appropriate enrichment flows.

Implements specification from:
- rispecs/Analytical_Feedback_Loop_Specification.md
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING
import uuid

from .narrative_intelligence_integration import (
    StoryBeat,
    CharacterArcState,
    EmotionalAnalysis,
    Gap,
    NCPState,
)
from .emotional_beat_enricher import (
    EmotionalBeatEnricher,
    EnrichedBeatResult,
    QualityThreshold,
)

logger = logging.getLogger(__name__)


# ============================================================================
# Gap Types and Routing
# ============================================================================

class GapType(str, Enum):
    """Categories of quality gaps."""
    EMOTIONAL_WEAK = "emotional_weak"
    EMOTIONAL_MISMATCH = "emotional_mismatch"
    CHARACTER_INCONSISTENT = "character_inconsistent"
    CHARACTER_STATIC = "character_static"
    THEME_MISSING = "theme_missing"
    THEME_CONTRADICTION = "theme_contradiction"
    PACING_ISSUE = "pacing_issue"
    DIALOGUE_WEAK = "dialogue_weak"


class GapSeverity(str, Enum):
    """Severity levels for gaps."""
    CRITICAL = "critical"
    MAJOR = "major"
    MINOR = "minor"


class GapDimension(str, Enum):
    """Analysis dimensions."""
    EMOTIONAL = "emotional"
    CHARACTER = "character"
    THEMATIC = "thematic"
    STRUCTURAL = "structural"


# ============================================================================
# Analysis Results
# ============================================================================

@dataclass
class CharacterAnalysisResult:
    """Result of character arc analysis."""
    player_id: str
    consistency_score: float
    arc_direction: str
    issues: List[str] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)


@dataclass
class ThematicAnalysisResult:
    """Result of thematic analysis."""
    theme: str
    presence_score: float
    coherence_score: float
    issues: List[str] = field(default_factory=list)


@dataclass 
class MultiDimensionalAnalysis:
    """Combined analysis across all dimensions."""
    beat_id: str
    
    # Individual analyses
    emotional: Optional[EmotionalAnalysis] = None
    character: Optional[CharacterAnalysisResult] = None
    thematic: Optional[ThematicAnalysisResult] = None
    
    # Overall scores
    overall_quality: float = 0.0
    
    # Identified gaps
    gaps: List[Gap] = field(default_factory=list)
    
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())


# ============================================================================
# Flow Routes
# ============================================================================

@dataclass
class FlowRoute:
    """Routing decision for gap remediation."""
    flow_id: str
    flow_name: str
    priority: int  # Lower = higher priority
    gap_types: List[GapType]
    handler: Optional[Callable] = None


# Default flow routes
DEFAULT_FLOW_ROUTES: List[FlowRoute] = [
    FlowRoute(
        flow_id="emotional_enrichment",
        flow_name="Emotional Beat Enrichment",
        priority=1,
        gap_types=[GapType.EMOTIONAL_WEAK, GapType.EMOTIONAL_MISMATCH],
    ),
    FlowRoute(
        flow_id="character_consistency",
        flow_name="Character Consistency Check",
        priority=2,
        gap_types=[GapType.CHARACTER_INCONSISTENT],
    ),
    FlowRoute(
        flow_id="character_development",
        flow_name="Character Development Boost",
        priority=3,
        gap_types=[GapType.CHARACTER_STATIC],
    ),
    FlowRoute(
        flow_id="thematic_weaving",
        flow_name="Thematic Integration",
        priority=4,
        gap_types=[GapType.THEME_MISSING, GapType.THEME_CONTRADICTION],
    ),
    FlowRoute(
        flow_id="dialogue_enhancement",
        flow_name="Dialogue Enhancement",
        priority=5,
        gap_types=[GapType.DIALOGUE_WEAK],
    ),
]


# ============================================================================
# Enrichment Container
# ============================================================================

@dataclass
class Enrichment:
    """Container for enrichment result."""
    gap_id: str
    flow_id: str
    original_content: str
    enriched_content: str
    improvement_score: float
    applied: bool = False
    notes: List[str] = field(default_factory=list)


# ============================================================================
# Analytical Feedback Loop
# ============================================================================

class AnalyticalFeedbackLoop:
    """
    Orchestrate the complete analysis → gap → enrichment → integration cycle.
    
    Implements specification from Analytical_Feedback_Loop_Specification.md
    """
    
    def __init__(
        self,
        emotional_enricher: EmotionalBeatEnricher,
        llm_provider: Any,
        config: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize with analyzer components.
        
        Args:
            emotional_enricher: Enricher for emotional quality
            llm_provider: LLM provider for analysis
            config: Configuration options
        """
        self.emotional_enricher = emotional_enricher
        self.llm_provider = llm_provider
        self.config = config or {}
        
        # Configuration
        self.gap_threshold = self.config.get('gap_threshold', 0.6)
        self.auto_remediate = self.config.get('auto_remediate', True)
        self.max_gaps_per_beat = self.config.get('max_gaps_per_beat', 3)
        
        # Flow routes
        self.flow_routes = DEFAULT_FLOW_ROUTES.copy()
        
        # Statistics
        self.stats = {
            'beats_analyzed': 0,
            'gaps_identified': 0,
            'gaps_remediated': 0,
        }
        
        logger.info("AnalyticalFeedbackLoop initialized")
    
    async def process_beat_with_analysis(
        self,
        beat: StoryBeat,
        ncp_state: NCPState,
    ) -> StoryBeat:
        """
        Complete analysis → enrichment pipeline for a beat.
        
        Args:
            beat: Story beat to process
            ncp_state: Current narrative state
        
        Returns:
            Processed (and possibly enriched) beat
        """
        self.stats['beats_analyzed'] += 1
        
        # Multi-dimensional analysis
        analysis = await self._analyze_beat(beat, ncp_state)
        
        # Identify gaps
        gaps = self._identify_gaps(analysis)
        analysis.gaps = gaps
        
        if gaps:
            self.stats['gaps_identified'] += len(gaps)
            logger.info(f"Beat {beat.beat_id}: {len(gaps)} gaps identified")
            
            # Auto-remediate if enabled
            if self.auto_remediate:
                beat = await self._remediate_gaps(beat, gaps, ncp_state)
        
        # Update beat quality score
        beat.quality_score = analysis.overall_quality
        
        return beat
    
    async def _analyze_beat(
        self,
        beat: StoryBeat,
        ncp_state: NCPState,
    ) -> MultiDimensionalAnalysis:
        """Perform multi-dimensional analysis on beat."""
        analysis = MultiDimensionalAnalysis(beat_id=beat.beat_id)
        
        # Emotional analysis
        analysis.emotional = await self.emotional_enricher.classify_emotion(beat)
        
        # Character analysis
        if beat.character_id and beat.character_id in ncp_state.character_states:
            analysis.character = await self._analyze_character(
                beat, ncp_state.character_states[beat.character_id]
            )
        
        # Thematic analysis
        if ncp_state.active_theme:
            analysis.thematic = await self._analyze_theme(beat, ncp_state.active_theme)
        
        # Calculate overall quality
        scores = []
        if analysis.emotional:
            scores.append(analysis.emotional.quality_score)
        if analysis.character:
            scores.append(analysis.character.consistency_score)
        if analysis.thematic:
            scores.append(analysis.thematic.presence_score)
        
        analysis.overall_quality = sum(scores) / len(scores) if scores else 0.5
        
        return analysis
    
    async def _analyze_character(
        self,
        beat: StoryBeat,
        character_state: CharacterArcState,
    ) -> CharacterAnalysisResult:
        """Analyze character consistency and development."""
        issues = []
        suggestions = []
        
        # Check arc consistency
        consistency_score = 1.0
        
        # Check if emotional tone aligns with character journey
        if character_state.arc_points:
            recent_emotions = [p.emotional_state for p in character_state.arc_points[-3:]]
            if beat.emotional_tone and beat.emotional_tone not in recent_emotions:
                # Not necessarily an issue, but worth noting
                pass
        
        # Determine arc direction
        arc_direction = "static"
        if len(character_state.arc_points) >= 2:
            recent = character_state.arc_points[-1]
            arc_direction = recent.arc_direction
        
        return CharacterAnalysisResult(
            player_id=character_state.player_id,
            consistency_score=consistency_score,
            arc_direction=arc_direction,
            issues=issues,
            suggestions=suggestions,
        )
    
    async def _analyze_theme(
        self,
        beat: StoryBeat,
        theme: str,
    ) -> ThematicAnalysisResult:
        """Analyze thematic presence and coherence."""
        # Simple keyword-based analysis (can be enhanced with LLM)
        theme_words = theme.lower().split()
        text_lower = beat.raw_text.lower()
        
        presence_score = sum(1 for w in theme_words if w in text_lower) / len(theme_words)
        
        # Use theme_resonance if available
        if beat.theme_resonance:
            coherence_score = 0.7  # Has explicit resonance
        else:
            coherence_score = presence_score * 0.5
        
        return ThematicAnalysisResult(
            theme=theme,
            presence_score=min(presence_score, 1.0),
            coherence_score=coherence_score,
        )
    
    def _identify_gaps(
        self,
        analysis: MultiDimensionalAnalysis,
    ) -> List[Gap]:
        """From analysis results, identify improvement areas."""
        gaps = []
        
        # Emotional gaps
        if analysis.emotional:
            if analysis.emotional.quality_score < self.gap_threshold:
                gaps.append(Gap(
                    gap_id=f"gap_{uuid.uuid4().hex[:8]}",
                    gap_type=GapType.EMOTIONAL_WEAK,
                    dimension=GapDimension.EMOTIONAL,
                    score=analysis.emotional.quality_score,
                    severity=self._determine_severity(analysis.emotional.quality_score),
                    confidence=analysis.emotional.confidence,
                    description=f"Emotional quality below threshold ({analysis.emotional.quality_score:.2f})",
                    evidence=analysis.emotional.improvement_areas,
                    suggested_flows=["emotional_enrichment"],
                    beat_id=analysis.beat_id,
                ))
        
        # Character gaps
        if analysis.character:
            if analysis.character.consistency_score < self.gap_threshold:
                gaps.append(Gap(
                    gap_id=f"gap_{uuid.uuid4().hex[:8]}",
                    gap_type=GapType.CHARACTER_INCONSISTENT,
                    dimension=GapDimension.CHARACTER,
                    score=analysis.character.consistency_score,
                    severity=self._determine_severity(analysis.character.consistency_score),
                    confidence=0.8,
                    description=f"Character consistency issues: {', '.join(analysis.character.issues)}",
                    evidence=analysis.character.issues,
                    suggested_flows=["character_consistency"],
                    beat_id=analysis.beat_id,
                ))
        
        # Thematic gaps
        if analysis.thematic:
            if analysis.thematic.presence_score < self.gap_threshold:
                gaps.append(Gap(
                    gap_id=f"gap_{uuid.uuid4().hex[:8]}",
                    gap_type=GapType.THEME_MISSING,
                    dimension=GapDimension.THEMATIC,
                    score=analysis.thematic.presence_score,
                    severity=self._determine_severity(analysis.thematic.presence_score),
                    confidence=0.7,
                    description=f"Theme '{analysis.thematic.theme}' underrepresented",
                    evidence=[f"Presence: {analysis.thematic.presence_score:.2f}"],
                    suggested_flows=["thematic_weaving"],
                    beat_id=analysis.beat_id,
                ))
        
        # Limit gaps
        gaps = sorted(gaps, key=lambda g: g.score)[:self.max_gaps_per_beat]
        
        return gaps
    
    def _determine_severity(self, score: float) -> str:
        """Determine gap severity from score."""
        if score < 0.3:
            return GapSeverity.CRITICAL
        elif score < 0.5:
            return GapSeverity.MAJOR
        else:
            return GapSeverity.MINOR
    
    async def _remediate_gaps(
        self,
        beat: StoryBeat,
        gaps: List[Gap],
        ncp_state: NCPState,
    ) -> StoryBeat:
        """Apply remediation for identified gaps."""
        current_beat = beat
        
        for gap in gaps:
            # Find appropriate flow
            flow = self._find_flow_for_gap(gap)
            if not flow:
                logger.warning(f"No flow found for gap type {gap.gap_type}")
                continue
            
            # Execute enrichment
            try:
                enrichment = await self._execute_enrichment_flow(
                    current_beat, flow, gap
                )
                
                if enrichment and enrichment.applied:
                    # Apply enrichment
                    current_beat = self._apply_enrichment(current_beat, enrichment)
                    self.stats['gaps_remediated'] += 1
                    
            except Exception as e:
                logger.error(f"Enrichment flow failed: {e}")
        
        return current_beat
    
    def _find_flow_for_gap(self, gap: Gap) -> Optional[FlowRoute]:
        """Find the appropriate flow route for a gap."""
        for flow in sorted(self.flow_routes, key=lambda f: f.priority):
            if gap.gap_type in flow.gap_types:
                return flow
        return None
    
    async def _execute_enrichment_flow(
        self,
        beat: StoryBeat,
        flow: FlowRoute,
        gap: Gap,
    ) -> Optional[Enrichment]:
        """Execute enrichment for a specific gap."""
        
        if flow.flow_id == "emotional_enrichment":
            # Use emotional enricher
            result = await self.emotional_enricher.analyze_and_enrich(beat)
            
            if result.was_enriched:
                return Enrichment(
                    gap_id=gap.gap_id,
                    flow_id=flow.flow_id,
                    original_content=beat.raw_text,
                    enriched_content=result.final_beat.raw_text,
                    improvement_score=result.improvement_delta,
                    applied=True,
                    notes=result.enrichment_notes,
                )
        
        elif flow.flow_id in ["character_consistency", "character_development"]:
            # Character-focused enrichment (simplified)
            logger.info(f"Character flow {flow.flow_id} - placeholder")
            # Would call character-specific enricher
        
        elif flow.flow_id == "thematic_weaving":
            # Theme-focused enrichment (simplified)
            logger.info(f"Thematic flow {flow.flow_id} - placeholder")
            # Would call thematic enricher
        
        return None
    
    def _apply_enrichment(
        self,
        beat: StoryBeat,
        enrichment: Enrichment,
    ) -> StoryBeat:
        """Integrate enrichment while preserving continuity."""
        return StoryBeat(
            beat_id=beat.beat_id,
            beat_index=beat.beat_index,
            raw_text=enrichment.enriched_content,
            character_id=beat.character_id,
            character_name=beat.character_name,
            dialogue=beat.dialogue,
            action=beat.action,
            internal=beat.internal,
            emotional_tone=beat.emotional_tone,
            theme_resonance=beat.theme_resonance,
            universe_analysis=beat.universe_analysis,
            enrichments_applied=beat.enrichments_applied + [enrichment.flow_id],
            quality_score=beat.quality_score + enrichment.improvement_score,
            ncp_metadata=beat.ncp_metadata,
            timestamp=beat.timestamp,
        )
    
    def register_flow(self, flow: FlowRoute) -> None:
        """Register a custom flow route."""
        self.flow_routes.append(flow)
        self.flow_routes.sort(key=lambda f: f.priority)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get processing statistics."""
        return self.stats.copy()


# ============================================================================
# Module Exports
# ============================================================================

__all__ = [
    # Enums
    "GapType",
    "GapSeverity",
    "GapDimension",
    
    # Data classes
    "CharacterAnalysisResult",
    "ThematicAnalysisResult",
    "MultiDimensionalAnalysis",
    "FlowRoute",
    "Enrichment",
    
    # Constants
    "DEFAULT_FLOW_ROUTES",
    
    # Classes
    "AnalyticalFeedbackLoop",
]
