"""
Narrative Intelligence Integration for Storytelling Package

This module provides NCP-aware story generation by integrating with the
narrative_intelligence toolkit from langgraph.

Implements specifications from:
- rispecs/Narrative_Intelligence_Integration_Specification.md
- rispecs/Character_Arc_Tracking_Specification.md
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, TYPE_CHECKING

# Graceful import of narrative_intelligence
try:
    from narrative_intelligence import (
        # Core NCP types
        NCPData,
        Player,
        Perspective,
        NCPStoryBeat,
        StoryPoint,
        Moment,
        # Three-Universe types
        Universe,
        UniversePerspective,
        ThreeUniverseAnalysis,
        NarrativePosition,
        StoryBeat as NCPBeat,
        CharacterState,
        ThematicThread,
        UnifiedNarrativeState,
        create_new_narrative_state,
        RedisKeys,
        HAS_LANGGRAPH,
    )
    HAS_NARRATIVE_INTELLIGENCE = True
except ImportError:
    HAS_NARRATIVE_INTELLIGENCE = False
    HAS_LANGGRAPH = False
    # Define placeholder types
    Universe = None
    UniversePerspective = None
    ThreeUniverseAnalysis = None
    NarrativePosition = None
    CharacterState = None
    UnifiedNarrativeState = None
    RedisKeys = None

logger = logging.getLogger(__name__)


# ============================================================================
# Emotional Taxonomy (from Emotional_Beat_Enrichment_Specification.md)
# ============================================================================

class EmotionCategory(str, Enum):
    """Primary emotion categories for beat classification."""
    JOY = "joy"
    SADNESS = "sadness"
    ANGER = "anger"
    FEAR = "fear"
    SURPRISE = "surprise"
    DISGUST = "disgust"
    TRUST = "trust"
    ANTICIPATION = "anticipation"
    LOVE = "love"
    SHAME = "shame"


# ============================================================================
# Story Beat (storytelling-specific wrapper)
# ============================================================================

@dataclass
class StoryBeat:
    """
    Structured representation of a narrative moment with full metadata.
    
    This wraps the NCP StoryBeat with storytelling-specific fields for
    generation, enrichment, and tracking.
    """
    beat_id: str
    beat_index: int
    raw_text: str
    
    # Character and perspective
    character_id: str
    character_name: Optional[str] = None
    
    # Structured content
    dialogue: Optional[str] = None
    action: Optional[str] = None
    internal: Optional[str] = None
    
    # Analysis results
    emotional_tone: Optional[str] = None
    emotion_confidence: float = 0.0
    theme_resonance: Optional[str] = None
    
    # Three-Universe analysis (from narrative_intelligence)
    universe_analysis: Optional[Dict[str, Any]] = None
    
    # Enrichment tracking
    enrichments_applied: List[str] = field(default_factory=list)
    quality_score: float = 0.0
    
    # Metadata
    ncp_metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "StoryBeat":
        """Deserialize from dictionary."""
        return cls(**data)
    
    def to_json(self) -> str:
        """Serialize to JSON string."""
        return json.dumps(self.to_dict())
    
    @classmethod
    def from_json(cls, json_str: str) -> "StoryBeat":
        """Deserialize from JSON string."""
        return cls.from_dict(json.loads(json_str))


# ============================================================================
# Character Arc State (from Character_Arc_Tracking_Specification.md)
# ============================================================================

@dataclass
class ArcPoint:
    """Represent a single moment of character development."""
    beat_id: str
    beat_index: int
    timestamp: str
    
    # Development tracking
    emotional_state: str
    arc_direction: str  # "ascending", "descending", "static", "crisis", "resolution"
    impact_magnitude: float  # 0.0 to 1.0
    
    # What changed
    goals_affected: List[str] = field(default_factory=list)
    relationships_affected: List[str] = field(default_factory=list)
    lessons_learned: List[str] = field(default_factory=list)
    
    # Alignment check
    consistency_score: float = 1.0


@dataclass
class RelationshipState:
    """Track character-to-character relationships."""
    character_a_id: str
    character_b_id: str
    relationship_type: str  # "ally", "rival", "mentor", "protege", "neutral"
    trust_level: float  # -1.0 to 1.0
    history: List[str] = field(default_factory=list)
    current_dynamic: str = "neutral"


@dataclass
class CharacterArcState:
    """
    Comprehensive state container for a character's narrative journey.
    
    Implements specification from Character_Arc_Tracking_Specification.md
    """
    player_id: str
    name: str
    
    # Core character elements
    wound: Optional[str] = None
    desire: Optional[str] = None
    arc_description: Optional[str] = None
    role: str = "supporting"
    
    # Current state
    current_emotional_state: str = "neutral"
    active_goals: List[str] = field(default_factory=list)
    active_fears: List[str] = field(default_factory=list)
    
    # Development tracking
    arc_points: List[ArcPoint] = field(default_factory=list)
    arc_position: float = 0.0  # 0.0 (beginning) to 1.0 (resolved)
    
    # Relationships (K'é tracking)
    relationship_map: Dict[str, RelationshipState] = field(default_factory=dict)
    
    # Three-universe archetype (if applicable)
    archetype: Optional[str] = None  # "mia", "ava8", "miette", or custom
    
    def add_arc_point(self, arc_point: ArcPoint) -> None:
        """Add a development point to the character's arc."""
        self.arc_points.append(arc_point)
        # Update arc position based on direction
        if arc_point.arc_direction == "ascending":
            self.arc_position = min(1.0, self.arc_position + arc_point.impact_magnitude * 0.1)
        elif arc_point.arc_direction == "descending":
            self.arc_position = max(0.0, self.arc_position - arc_point.impact_magnitude * 0.1)
    
    def get_arc_context(self, depth: int = 3) -> str:
        """
        Generate context summary for prompts.
        
        Args:
            depth: Number of recent arc points to include (-1 for all)
        """
        points = self.arc_points[-depth:] if depth > 0 else self.arc_points
        
        context = f"""=== Character Arc Context for {self.name} ===

Starting Point:
- Wound: {self.wound or 'Unknown'}
- Desire: {self.desire or 'Unknown'}
- Role: {self.role}

Current State:
- Emotional State: {self.current_emotional_state}
- Arc Position: {self.arc_position:.1%} through journey
- Active Goals: {', '.join(self.active_goals) or 'None specified'}

Recent Developments:
"""
        for point in points:
            context += f"- [{point.arc_direction}] {point.emotional_state} (impact: {point.impact_magnitude:.2f})\n"
        
        return context


# ============================================================================
# Emotional Analysis (from Emotional_Beat_Enrichment_Specification.md)
# ============================================================================

@dataclass
class EmotionalAnalysis:
    """Comprehensive emotional assessment of a story beat."""
    beat_id: str
    
    # Classification
    primary_emotion: str
    secondary_emotions: List[str] = field(default_factory=list)
    confidence: float = 0.0
    
    # Quality metrics
    resonance_score: float = 0.0  # How strongly emotion connects
    specificity_score: float = 0.0  # Detail level of expression
    authenticity_score: float = 0.0  # Genuine vs forced
    
    # Overall quality
    quality_score: float = 0.0
    
    # Improvement guidance
    improvement_areas: List[str] = field(default_factory=list)
    suggested_techniques: List[str] = field(default_factory=list)
    
    def calculate_quality(self) -> float:
        """Calculate overall emotional quality score."""
        weights = {
            'confidence': 0.20,
            'resonance': 0.35,
            'specificity': 0.25,
            'authenticity': 0.20,
        }
        self.quality_score = (
            self.confidence * weights['confidence'] +
            self.resonance_score * weights['resonance'] +
            self.specificity_score * weights['specificity'] +
            self.authenticity_score * weights['authenticity']
        )
        return self.quality_score


# ============================================================================
# Gap Identification (from Analytical_Feedback_Loop_Specification.md)
# ============================================================================

@dataclass
class Gap:
    """Represent a specific quality deficiency identified in analysis."""
    gap_id: str
    gap_type: str  # "emotional_weak", "character_inconsistent", "theme_missing"
    dimension: str  # "character", "theme", "emotion"
    
    # Assessment
    score: float  # 0-1, low = needs improvement
    severity: str  # "critical", "major", "minor"
    confidence: float
    
    # Context
    description: str
    evidence: List[str] = field(default_factory=list)
    suggested_flows: List[str] = field(default_factory=list)
    
    # Metadata
    beat_id: str = ""
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())


# ============================================================================
# NCP State for Storytelling
# ============================================================================

@dataclass
class NCPState:
    """
    Narrative state maintained across beat generation.
    
    Extends the narrative_intelligence NCPState for storytelling workflows.
    """
    # Beat tracking
    beats: List[StoryBeat] = field(default_factory=list)
    current_beat_index: int = 0
    
    # Perspective and theme
    active_perspective: Optional[str] = None  # "main_character", "influence", etc.
    active_theme: Optional[str] = None
    
    # Character states (K'é tracking)
    character_states: Dict[str, CharacterArcState] = field(default_factory=dict)
    
    # Narrative position
    dramatic_phase: str = "setup"  # "setup", "confrontation", "resolution"
    act_number: int = 1
    tension_level: float = 0.0
    
    # Three-universe state (if enabled)
    universe_analysis: Optional[Dict[str, Any]] = None
    lead_universe: Optional[str] = None
    coherence_score: float = 0.0
    
    # Gap tracking
    identified_gaps: List[Gap] = field(default_factory=list)
    enrichment_count: int = 0
    
    # Metadata
    story_id: Optional[str] = None
    session_id: Optional[str] = None
    
    def add_beat(self, beat: StoryBeat) -> None:
        """Add a beat to the state."""
        self.beats.append(beat)
        self.current_beat_index = len(self.beats)
    
    def get_character_state(self, player_id: str) -> Optional[CharacterArcState]:
        """Get character state by player ID."""
        return self.character_states.get(player_id)
    
    def update_character_state(self, state: CharacterArcState) -> None:
        """Update or add character state."""
        self.character_states[state.player_id] = state


# ============================================================================
# NCP-Aware Story Generator
# ============================================================================

class NCPAwareStoryGenerator:
    """
    Wrap LLM generation with NCP context to produce structured story beats.
    
    Implements specification from Narrative_Intelligence_Integration_Specification.md
    """
    
    def __init__(
        self,
        llm_provider: Any,
        graph_executor: Optional[Any] = None,
        config: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize with LLM provider and optional graph executor.
        
        Args:
            llm_provider: LLM provider instance (from storytelling.llm_providers)
            graph_executor: Optional LangGraph executor for workflows
            config: Configuration options
        """
        self.llm_provider = llm_provider
        self.graph_executor = graph_executor
        self.config = config or {}
        
        # Initialize state
        self.ncp_state = NCPState()
        
        # Initialize character tracker
        self.character_tracker = CharacterArcTracker()
        
        # Feature flags
        self.ncp_aware_generation = self.config.get('ncp_aware_generation', True)
        self.emotional_targeting = self.config.get('ncp_emotional_targeting', True)
        self.theme_tracking = self.config.get('ncp_theme_tracking', True)
        self.character_context_depth = self.config.get('ncp_character_context_depth', 3)
        self.ceremonial_mode = self.config.get('ceremonial_mode', False)
        
        logger.info(f"NCPAwareStoryGenerator initialized (NCP={self.ncp_aware_generation})")
    
    def initialize_from_story_elements(
        self,
        characters: List[Dict[str, Any]],
        themes: List[str],
        perspective: str = "third_limited",
    ) -> None:
        """
        Initialize NCP state from story elements.
        
        Args:
            characters: List of character dictionaries
            themes: List of theme strings
            perspective: Narrative perspective
        """
        # Initialize character states
        for char_data in characters:
            char_state = CharacterArcState(
                player_id=char_data.get('id', char_data.get('name', 'unknown')),
                name=char_data.get('name', 'Unknown'),
                wound=char_data.get('wound'),
                desire=char_data.get('desire'),
                arc_description=char_data.get('arc'),
                role=char_data.get('role', 'supporting'),
            )
            self.ncp_state.character_states[char_state.player_id] = char_state
        
        # Set active theme
        if themes:
            self.ncp_state.active_theme = themes[0]
        
        # Set perspective
        self.ncp_state.active_perspective = perspective
        
        logger.info(f"Initialized NCP state with {len(characters)} characters")
    
    def generate_beat_with_ncp(
        self,
        context: str,
        character_id: str,
        theme: Optional[str] = None,
        emotional_target: Optional[str] = None,
    ) -> StoryBeat:
        """
        Generate a story beat with full NCP context.
        
        Args:
            context: Story context/previous content
            character_id: Primary character for this beat
            theme: Thematic focus (or use active theme)
            emotional_target: Target emotion for the beat
        
        Returns:
            Generated StoryBeat with full metadata
        """
        # Get character state
        character_state = self.ncp_state.get_character_state(character_id)
        
        # Build NCP-aware prompt
        prompt = self._build_ncp_prompt(
            context=context,
            character=character_state,
            theme=theme or self.ncp_state.active_theme,
            emotional_target=emotional_target,
        )
        
        # Generate via LLM
        response = self._generate_llm_response(prompt)
        
        # Parse into structured beat
        beat = self._parse_beat(
            response=response,
            character_id=character_id,
        )
        
        # Record beat impact on character arc
        if character_state:
            arc_point = ArcPoint(
                beat_id=beat.beat_id,
                beat_index=beat.beat_index,
                timestamp=beat.timestamp,
                emotional_state=beat.emotional_tone or "neutral",
                arc_direction=self._determine_arc_direction(beat, character_state),
                impact_magnitude=0.3,  # Default moderate impact
            )
            character_state.add_arc_point(arc_point)
        
        # Add to state
        self.ncp_state.add_beat(beat)
        
        return beat
    
    def _build_ncp_prompt(
        self,
        context: str,
        character: Optional[CharacterArcState],
        theme: Optional[str],
        emotional_target: Optional[str],
    ) -> str:
        """Build NCP-aware generation prompt."""
        
        perspective = self.ncp_state.active_perspective or "third_limited"
        char_name = character.name if character else "the character"
        
        prompt = f"""You are writing for the {perspective} perspective of {char_name}.

=== Character State ===
{character.get_arc_context(self.character_context_depth) if character else "No character context available."}

=== Narrative Moment ===
- Phase: {self.ncp_state.dramatic_phase}
- Theme Focus: {theme or "Not specified"}
- Emotional Beat Needed: {emotional_target or "Contextually appropriate"}
- Tension Level: {self.ncp_state.tension_level:.0%}

=== Story Context ===
{context}

=== Generation Instructions ===
Write dialogue and action that:
1. Advances {char_name}'s arc appropriately
2. Explores the theme of {theme or "the central conflict"}
3. Creates {emotional_target or "appropriate emotional"} tone
4. Maintains consistency with established narrative

=== Response Format ===
<beat>
<dialogue>Character speech here (or "None" if no dialogue)</dialogue>
<action>Physical action and scene description</action>
<internal>Character's internal thoughts if applicable (or "None")</internal>
<emotional_tone>The dominant emotion of this beat</emotional_tone>
<theme_resonance>How this beat connects to the theme</theme_resonance>
</beat>
"""
        
        # Add ceremonial elements if enabled
        if self.ceremonial_mode:
            prompt += """

=== Ceremonial Guidance (K'é) ===
Honor the relationships between characters. Consider:
- How does this moment affect the web of kinship?
- What obligations are being honored or challenged?
- How does this serve seven-generation thinking?
"""
        
        return prompt
    
    def _generate_llm_response(self, prompt: str) -> str:
        """Generate response from LLM."""
        try:
            # Use the llm_provider to generate
            # This should match the storytelling package's LLM interface
            response = self.llm_provider.generate(prompt)
            return response
        except Exception as e:
            logger.error(f"LLM generation failed: {e}")
            return ""
    
    def _parse_beat(
        self,
        response: str,
        character_id: str,
    ) -> StoryBeat:
        """Parse LLM response into structured StoryBeat."""
        import re
        import uuid
        
        beat_index = self.ncp_state.current_beat_index + 1
        
        # Try to parse XML format
        dialogue = self._extract_tag(response, "dialogue")
        action = self._extract_tag(response, "action")
        internal = self._extract_tag(response, "internal")
        emotional_tone = self._extract_tag(response, "emotional_tone")
        theme_resonance = self._extract_tag(response, "theme_resonance")
        
        # Handle "None" values
        if dialogue and dialogue.lower() == "none":
            dialogue = None
        if internal and internal.lower() == "none":
            internal = None
        
        return StoryBeat(
            beat_id=f"beat_{beat_index}_{uuid.uuid4().hex[:8]}",
            beat_index=beat_index,
            raw_text=response,
            character_id=character_id,
            dialogue=dialogue,
            action=action,
            internal=internal,
            emotional_tone=emotional_tone,
            theme_resonance=theme_resonance,
        )
    
    def _extract_tag(self, text: str, tag: str) -> Optional[str]:
        """Extract content from XML-like tag."""
        import re
        pattern = f"<{tag}>(.*?)</{tag}>"
        match = re.search(pattern, text, re.DOTALL)
        return match.group(1).strip() if match else None
    
    def _determine_arc_direction(
        self,
        beat: StoryBeat,
        character: CharacterArcState,
    ) -> str:
        """Determine arc direction from beat content."""
        emotion = (beat.emotional_tone or "").lower()
        
        # Simple heuristic - can be enhanced with LLM analysis
        ascending_emotions = {"hope", "joy", "triumph", "love", "confidence"}
        descending_emotions = {"despair", "fear", "grief", "shame", "defeat"}
        crisis_emotions = {"crisis", "confrontation", "turning", "revelation"}
        
        if any(e in emotion for e in ascending_emotions):
            return "ascending"
        elif any(e in emotion for e in descending_emotions):
            return "descending"
        elif any(e in emotion for e in crisis_emotions):
            return "crisis"
        else:
            return "static"


# ============================================================================
# Character Arc Tracker
# ============================================================================

class CharacterArcTracker:
    """
    Track character development across generated beats.
    
    Implements specification from Character_Arc_Tracking_Specification.md
    """
    
    def __init__(self):
        """Initialize tracker."""
        self.character_states: Dict[str, CharacterArcState] = {}
    
    def initialize_character(
        self,
        player_id: str,
        name: str,
        **kwargs,
    ) -> CharacterArcState:
        """Initialize tracking for a character."""
        state = CharacterArcState(
            player_id=player_id,
            name=name,
            **kwargs,
        )
        self.character_states[player_id] = state
        return state
    
    def record_beat_impact(
        self,
        beat: StoryBeat,
        player_id: str,
    ) -> Optional[ArcPoint]:
        """Record how a beat affects a character's arc."""
        state = self.character_states.get(player_id)
        if not state:
            logger.warning(f"No character state for {player_id}")
            return None
        
        arc_point = ArcPoint(
            beat_id=beat.beat_id,
            beat_index=beat.beat_index,
            timestamp=beat.timestamp,
            emotional_state=beat.emotional_tone or "neutral",
            arc_direction="static",  # Will be analyzed
            impact_magnitude=0.3,
        )
        
        state.add_arc_point(arc_point)
        return arc_point
    
    def get_arc_context(
        self,
        player_id: str,
        depth: int = 3,
    ) -> str:
        """Get character arc context for generation prompts."""
        state = self.character_states.get(player_id)
        if not state:
            return f"No arc context available for character {player_id}"
        return state.get_arc_context(depth)
    
    def validate_consistency(
        self,
        beat: StoryBeat,
        player_id: str,
    ) -> Dict[str, Any]:
        """Validate beat consistency with character arc."""
        state = self.character_states.get(player_id)
        if not state:
            return {"is_consistent": True, "score": 1.0, "issues": []}
        
        issues = []
        score = 1.0
        
        # Check emotional consistency
        if state.arc_points:
            recent_emotions = [p.emotional_state for p in state.arc_points[-3:]]
            if beat.emotional_tone:
                # Simple check - can be enhanced
                pass
        
        return {
            "is_consistent": score >= 0.7,
            "score": score,
            "issues": issues,
        }


# ============================================================================
# Module Exports
# ============================================================================

__all__ = [
    # Enums
    "EmotionCategory",
    
    # Data classes
    "StoryBeat",
    "ArcPoint",
    "RelationshipState",
    "CharacterArcState",
    "EmotionalAnalysis",
    "Gap",
    "NCPState",
    
    # Classes
    "NCPAwareStoryGenerator",
    "CharacterArcTracker",
    
    # Feature flags
    "HAS_NARRATIVE_INTELLIGENCE",
    "HAS_LANGGRAPH",
]
