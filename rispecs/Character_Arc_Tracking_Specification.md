# Character Arc Tracking Specification

**Status**: ⏳ PLANNED (Phase 1 Foundation)

**Structural Tension**
- Desired Outcome: Persistent character state tracking across all generated beats, enabling consistent character behavior, cumulative growth, and arc-aware generation.
- Current Reality: Each story beat is generated independently without awareness of the character's journey, resulting in potential inconsistencies and non-cumulative development.
- Natural Progression: Introduce CharacterArcTracker that maintains per-character state, analyzes beat impacts, and provides arc context for subsequent generations.

---

## 1. Overview

This specification defines the character arc tracking system that maintains narrative continuity for characters across story generation. The tracker:

1. **Initializes Character State**: Establishes baseline for each character
2. **Records Beat Impacts**: Analyzes how each beat affects character development
3. **Provides Arc Context**: Generates context summaries for generation prompts
4. **Validates Consistency**: Checks beats against established character arcs

## 2. Core Components

### 2.1 CharacterArcTracker

**Purpose**: Track character development across generated beats.

**Implementation Location**: `storytelling/character_arc_tracker.py`

**Interface**:
```python
class CharacterArcTracker:
    def __init__(self):
        """Initialize tracker with empty character states."""
        
    def initialize_character(self, character: Player) -> None:
        """Set up tracking for a character with initial state."""
        
    def record_beat_impact(
        self,
        beat: StoryBeat,
        character: Player
    ) -> ArcPoint:
        """Analyze and record a beat's impact on character arc."""
        
    def get_character_arc_context(
        self,
        character: Player,
        depth: int = 3
    ) -> str:
        """Generate context summary for generation prompts."""
        
    def check_arc_consistency(
        self,
        beat: StoryBeat,
        character: Player
    ) -> ConsistencyReport:
        """Validate beat against established character arc."""
```

### 2.2 CharacterArcState

**Purpose**: Comprehensive state container for a character's narrative journey.

**Schema**:
```python
@dataclass
class CharacterArcState:
    player: Player                  # Character reference
    initial_state: CharacterState   # Starting point
    current_state: CharacterState   # Present moment
    arc_points: List[ArcPoint]      # Journey milestones
    growth_trajectory: str          # Direction of change
    unresolved_threads: List[str]   # Open narrative threads
    relationship_map: Dict[str, RelationshipState]  # Character relationships
```

### 2.3 ArcPoint

**Purpose**: Represent a single moment of character development.

**Schema**:
```python
@dataclass
class ArcPoint:
    beat_id: str                    # Associated beat
    beat_index: int                 # Position in narrative
    timestamp: str                  # When recorded
    
    # Development dimensions
    realization: Optional[str]      # What character learns/realizes
    perspective_shift: Optional[str] # How worldview changes
    capability_gained: Optional[str] # New skill or strength
    emotional_transition: str       # Emotional state change
    goal_progress: Dict[str, float] # Progress toward goals (-1 to 1)
    
    # Narrative impact
    impact_magnitude: float         # Significance (0-1)
    arc_direction: str              # "advancing" | "regressing" | "stable"
    consistency_score: float        # Alignment with arc (0-1)
```

### 2.4 ConsistencyReport

**Purpose**: Report on beat's alignment with established character arc.

**Schema**:
```python
@dataclass
class ConsistencyReport:
    is_consistent: bool             # Overall consistency verdict
    consistency_score: float        # Numerical score (0-1)
    
    # Specific assessments
    behavior_alignment: float       # Does character act in character?
    arc_progression: str           # Does beat advance arc appropriately?
    dialogue_voice: float          # Is dialogue voice consistent?
    motivation_clarity: float      # Are motivations clear and consistent?
    
    # Guidance for correction
    issues: List[str]              # Specific inconsistency descriptions
    suggestions: List[str]         # Recommendations for alignment
```

## 3. Character Initialization

### 3.1 Initial State Extraction

When a character is introduced, extract baseline state:

```python
@dataclass
class CharacterState:
    name: str
    emotional_baseline: str         # Default emotional state
    core_beliefs: List[str]         # Foundational worldview
    active_goals: List[Goal]        # What character wants
    fears: List[str]                # Internal obstacles
    strengths: List[str]            # Character capabilities
    weaknesses: List[str]           # Character limitations
    voice_markers: List[str]        # Distinctive speech patterns
    relationship_stance: str        # Default interpersonal mode
```

### 3.2 Integration with Story Elements

Character initialization pulls from story elements:

```
story_elements.characters[N] 
    → CharacterArcTracker.initialize_character()
        → CharacterArcState created
            → Ready for beat tracking
```

## 4. Beat Impact Analysis

### 4.1 Impact Extraction Process

After each beat, analyze character impact:

1. **Identify Involvement**: Determine if character participates in beat
2. **Extract Actions**: What did character do?
3. **Extract Dialogue**: What did character say?
4. **Extract Reactions**: How did character respond?
5. **Assess Change**: What changed for the character?
6. **Record ArcPoint**: Persist the development moment

### 4.2 Impact Magnitude Calculation

Factors affecting impact magnitude:

| Factor | Weight | Description |
|--------|--------|-------------|
| Dialogue Length | 0.15 | Character speech volume |
| Action Significance | 0.25 | Importance of actions taken |
| Emotional Intensity | 0.20 | Strength of emotional content |
| Goal Relevance | 0.25 | Connection to character goals |
| Relationship Impact | 0.15 | Effect on relationships |

### 4.3 Arc Direction Determination

```python
def determine_arc_direction(
    beat: StoryBeat,
    arc_state: CharacterArcState
) -> str:
    """
    Determine if beat advances, regresses, or stabilizes arc.
    
    Returns:
    - "advancing": Character grows toward goals/resolution
    - "regressing": Character moves away from growth
    - "stable": Character maintains current state
    """
```

## 5. Arc Context Generation

### 5.1 Context Summary Format

Generated context for prompts:

```
=== Character Arc Context for {CHARACTER} ===

Starting Point:
- Began as: {INITIAL_STATE_SUMMARY}
- Core motivation: {PRIMARY_GOAL}

Journey So Far:
- Key realizations: {LESSONS_LEARNED}
- Growth path: {STATE_A} → {STATE_B}
- Emotional journey: {EMOTIONAL_PROGRESSION}

Current State:
- Present emotional state: {CURRENT_EMOTION}
- Active goals: {CURRENT_GOALS}
- Unresolved threads: {OPEN_THREADS}

Recent Developments (last {N} beats):
{RECENT_ARCPOINTS_SUMMARY}
```

### 5.2 Depth Configuration

Context depth controls how much history is included:

| Depth | History Included | Use Case |
|-------|------------------|----------|
| 1 | Last beat only | Fast generation, minimal context |
| 3 | Last 3 beats | Standard generation (default) |
| 5 | Last 5 beats | Complex scenes, major moments |
| -1 | Full history | Final scenes, arc resolution |

## 6. Consistency Validation

### 6.1 Validation Checks

Before finalizing a beat, validate consistency:

1. **Behavior Check**: Does character act consistently with established patterns?
2. **Dialogue Check**: Does voice match established speech patterns?
3. **Motivation Check**: Are actions aligned with goals and fears?
4. **Relationship Check**: Are interactions consistent with relationships?
5. **Growth Check**: Does development follow natural progression?

### 6.2 Consistency Thresholds

| Threshold | Value | Action |
|-----------|-------|--------|
| Excellent | ≥0.85 | Accept beat |
| Acceptable | ≥0.70 | Accept with minor notes |
| Concerning | ≥0.50 | Route to enrichment |
| Inconsistent | <0.50 | Flag for regeneration |

### 6.3 Consistency Remediation

When consistency is low:

```
Beat with low consistency
    → ConsistencyReport generated
        → Issues identified
            → Route to Enrichment Flow
                → Prompt includes:
                    - Original beat
                    - Consistency issues
                    - Character arc context
                    - Correction suggestions
                → Regenerated beat
                    → Re-validate
```

## 7. Relationship Tracking

### 7.1 RelationshipState

Track character-to-character relationships:

```python
@dataclass
class RelationshipState:
    character_a_id: str
    character_b_id: str
    relationship_type: str          # friend, rival, mentor, etc.
    trust_level: float              # -1 to 1
    conflict_level: float           # 0 to 1
    shared_history: List[str]       # Key shared moments
    current_dynamic: str            # Current relationship state
```

### 7.2 Relationship Impact Recording

Beats affecting relationships update RelationshipState:

- Dialogue between characters
- Actions affecting relationships
- Conflict or cooperation moments
- Trust-building or trust-breaking events

## 8. Integration Points

### 8.1 With NCP-Aware Generator

```python
# Before generation
arc_context = tracker.get_character_arc_context(character, depth=3)
prompt = generator._build_ncp_prompt(
    context=story_context,
    character=character,
    character_arc_context=arc_context,  # Injected
    ...
)

# After generation
beat = generator.generate_beat_with_ncp(...)
tracker.record_beat_impact(beat, character)
```

### 8.2 With Analytical Feedback Loop

Character arc analysis feeds into gap identification:

- Low consistency → "character_inconsistency" gap
- Arc regression without purpose → "arc_regression" gap
- Missing development → "character_static" gap

### 8.3 With Ceremony World Principles

Relationship tracking incorporates K'é (kinship) principles:

- Relationships tracked not just by type but by relational quality
- Seven-generation awareness in long-arc planning
- Reciprocity and balance considered in relationship dynamics

## 9. Persistence

### 9.1 State Serialization

CharacterArcState persists to session checkpoints:

```python
def serialize_arc_state(state: CharacterArcState) -> dict:
    """Serialize for checkpoint storage."""
    
def deserialize_arc_state(data: dict) -> CharacterArcState:
    """Restore from checkpoint."""
```

### 9.2 Resume Behavior

On session resume:
1. Load CharacterArcState from checkpoint
2. Reconstruct tracker with loaded states
3. Continue tracking from last position

## 10. Configuration

### 10.1 New Configuration Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `character_arc_tracking` | bool | true | Enable arc tracking |
| `arc_context_depth` | int | 3 | Default context depth |
| `consistency_threshold` | float | 0.70 | Minimum consistency score |
| `track_relationships` | bool | true | Enable relationship tracking |
| `arc_checkpoint_frequency` | int | 5 | Beats between arc checkpoints |

## 11. Success Criteria

- [ ] Character states initialized from story elements
- [ ] Beat impacts recorded with ArcPoint objects
- [ ] Arc context generated for generation prompts
- [ ] Consistency validation catches character breaks
- [ ] Relationships tracked across beats
- [ ] State persists across session checkpoints
- [ ] Graceful resume from checkpoints

---

**Related Specifications**:
- `Narrative_Intelligence_Integration_Specification.md`
- `Emotional_Beat_Enrichment_Specification.md`
- `Analytical_Feedback_Loop_Specification.md`
- `Session_Management_Architecture.md`
- `DataSchemas.md`
