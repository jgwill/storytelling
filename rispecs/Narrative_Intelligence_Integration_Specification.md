# Narrative Intelligence Integration Specification

**Status**: ⏳ PLANNED (Phase 1-3 Integration)

**Structural Tension**
- Desired Outcome: Story generation that is NCP-aware from inception, producing structured beats with metadata that enable analysis, enrichment, and character arc tracking.
- Current Reality: Current generation produces freestyle narrative text without NCP structure awareness, character state tracking, or thematic intent specification.
- Natural Progression: Introduce NCPAwareStoryGenerator that wraps generation with narrative context, producing StoryBeat objects ready for analytical feedback loops.

---

## 1. Overview

This specification defines the integration layer between the storytelling system and the Narrative Cognition Protocol (NCP). The integration enables:

1. **Structured Beat Generation**: Story beats produced as typed objects with metadata
2. **Character State Awareness**: Generation context includes character arc history
3. **Thematic Intent**: Each beat generated with explicit thematic focus
4. **Emotional Targeting**: Generation directed toward specific emotional tones
5. **Analysis Readiness**: Output structured for downstream enrichment flows

## 2. Core Components

### 2.1 NCPAwareStoryGenerator

**Purpose**: Wrap LLM generation with NCP context to produce structured story beats.

**Implementation Location**: `storytelling/narrative_intelligence_integration.py`

**Dependencies**:
- `narrative_intelligence`: StoryBeat, NCPState, Player, Perspective (from toolkit)
- `storytelling.llm_provider`: LLMProvider interface
- `storytelling.graph`: Graph executor for state management

**Interface**:
```python
class NCPAwareStoryGenerator:
    def __init__(self, llm_provider, graph_executor):
        """Initialize with LLM provider and graph executor."""
        
    def generate_beat_with_ncp(
        self,
        context: str,
        character_state: Player,
        thematic_focus: str,
        emotional_target: str
    ) -> StoryBeat:
        """Generate a story beat with full NCP context."""
        
    def _build_ncp_prompt(
        self,
        context: str,
        character: Player,
        theme: str,
        emotion: str
    ) -> str:
        """Construct NCP-aware generation prompt."""
        
    def _parse_beat(
        self,
        response: str,
        character: Player
    ) -> StoryBeat:
        """Parse LLM response into structured StoryBeat."""
```

### 2.2 StoryBeat Data Structure

**Purpose**: Structured representation of a narrative moment with full metadata.

**Schema**:
```python
@dataclass
class StoryBeat:
    beat_id: str                    # Unique identifier
    beat_index: int                 # Position in sequence
    character_id: str               # Primary character perspective
    dialogue: Optional[str]         # Character speech
    action: Optional[str]           # Character/scene action
    internal_thought: Optional[str] # Character internal state
    emotional_tone: str             # Detected/intended emotion
    theme_resonance: str            # Connection to active theme
    raw_text: str                   # Full generated content
    metadata: Dict[str, Any]        # Additional context
    timestamp: str                  # Generation timestamp
```

### 2.3 NCPState Tracker

**Purpose**: Maintain narrative state across beat generation.

**Key State Elements**:
- `beats`: List[StoryBeat] - All generated beats
- `active_perspective`: Perspective - Current narrative viewpoint
- `active_theme`: str - Current thematic focus
- `character_states`: Dict[str, CharacterArcState] - Per-character state
- `dramatic_phase`: str - Current narrative phase (setup/crisis/resolution)

## 3. NCP-Aware Prompt Construction

### 3.1 Prompt Template Structure

The NCP-aware prompt includes structured sections:

```
You are writing for the {PERSPECTIVE} of {CHARACTER}.

=== Character State ===
- Arc Progress: {CHARACTER_ARC_SUMMARY}
- Current Emotional State: {CURRENT_EMOTION}
- Active Goals: {CHARACTER_GOALS}
- Relationships: {KEY_RELATIONSHIPS}

=== Narrative Moment ===
- Phase: {DRAMATIC_PHASE}
- Theme Focus: {THEMATIC_FOCUS}
- Emotional Beat Needed: {EMOTIONAL_TARGET}
- Tension Level: {TENSION_LEVEL}

=== Story Context ===
{STORY_CONTEXT}

=== Generation Instructions ===
Write dialogue and action that:
1. Advances {CHARACTER}'s arc from {STATE_A} toward {STATE_B}
2. Explores the theme of {THEME}
3. Creates {EMOTIONAL_TARGET} tone
4. Maintains consistency with established narrative

=== Response Format ===
<beat>
<dialogue>Character speech here</dialogue>
<action>Physical action and scene description</action>
<internal>Character's internal thoughts if applicable</internal>
<emotional_tone>The dominant emotion of this beat</emotional_tone>
<theme_resonance>How this beat connects to the theme</theme_resonance>
</beat>
```

### 3.2 Prompt Variables

| Variable | Source | Description |
|----------|--------|-------------|
| PERSPECTIVE | NCPState.active_perspective | First-person, third-limited, etc. |
| CHARACTER | Player.name | Character name |
| CHARACTER_ARC_SUMMARY | CharacterArcTracker | Arc progress summary |
| CURRENT_EMOTION | Player.emotional_state | Current emotional state |
| CHARACTER_GOALS | Player.goals | Active character goals |
| KEY_RELATIONSHIPS | NCPState | Relevant relationships |
| DRAMATIC_PHASE | NCPState.dramatic_phase | Setup/crisis/resolution |
| THEMATIC_FOCUS | NCPState.active_theme | Current theme |
| EMOTIONAL_TARGET | Determined by phase | Target emotion for beat |
| TENSION_LEVEL | NCPState | Current dramatic tension |
| STORY_CONTEXT | Previous beats summary | Narrative context |

## 4. Beat Parsing Logic

### 4.1 XML Response Parsing

The generator parses structured XML responses:

```python
def _parse_beat(self, response: str, character: Player) -> StoryBeat:
    """
    Parse structured response into StoryBeat.
    
    Handles:
    - Well-formed XML <beat> blocks
    - Partial/malformed responses (fallback to raw text)
    - Missing optional elements
    """
    # Extract beat block
    # Parse sub-elements
    # Construct StoryBeat with defaults for missing elements
    # Preserve raw_text for fallback
```

### 4.2 Fallback Behavior

When parsing fails:
1. Log parsing warning
2. Create StoryBeat with `raw_text` populated
3. Set `emotional_tone` and `theme_resonance` to "unclassified"
4. Mark for downstream analysis/classification

## 5. Integration Points

### 5.1 With Story Generation Graph

The NCPAwareStoryGenerator integrates with the existing LangGraph workflow:

```
generate_story_elements_node
        ↓
generate_initial_outline_node
        ↓
[NEW] setup_ncp_state_node          # Initialize NCP tracking
        ↓
[ENHANCED] generate_single_chapter_node
        ↓
    uses NCPAwareStoryGenerator.generate_beat_with_ncp()
        ↓
[NEW] analyze_beat_node             # Emotional/thematic analysis
        ↓
[NEW] track_character_node          # Update character arcs
```

### 5.2 With Character Arc Tracker

- Generator queries tracker for character context before generation
- Generator reports beat to tracker after generation
- See: `Character_Arc_Tracking_Specification.md`

### 5.3 With Emotional Beat Enricher

- Generated beats sent to enricher for quality assessment
- Low-quality beats regenerated with enhanced prompts
- See: `Emotional_Beat_Enrichment_Specification.md`

### 5.4 With Analytical Feedback Loop

- Beats analyzed for gaps (emotional, thematic, character)
- Gaps route to appropriate enrichment flows
- See: `Analytical_Feedback_Loop_Specification.md`

## 6. Configuration

### 6.1 New Configuration Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `ncp_aware_generation` | bool | false | Enable NCP-aware generation |
| `ncp_emotional_targeting` | bool | true | Enable emotional beat targeting |
| `ncp_theme_tracking` | bool | true | Enable thematic continuity |
| `ncp_character_context_depth` | int | 3 | Number of previous beats for character context |
| `ncp_beat_format` | str | "xml" | Response format (xml/json) |

### 6.2 Environment Variables

| Variable | Description |
|----------|-------------|
| `WILLWRITE_NCP_ENABLED` | Global NCP feature flag |
| `WILLWRITE_NCP_DEBUG` | Enable NCP debug logging |

## 7. Ceremony World Integration

This specification aligns with the Ceremony World (Ava8) perspective:

- **Indigenous-Inspired Prompts**: NCP prompts can incorporate ceremonial storytelling elements
- **Sacred Pause**: Each beat generation becomes an opportunity for narrative reflection
- **Relational Awareness**: Character relationships tracked with K'é principles
- **Seven-Generation Thinking**: Theme tracking considers long-arc narrative impact

## 8. Success Criteria

- [ ] StoryBeat objects produced with full metadata
- [ ] Character state context injected into generation prompts
- [ ] Thematic focus maintained across beat sequences
- [ ] Emotional targeting influences generated content
- [ ] Beats parseable for downstream analysis
- [ ] Graceful degradation when NCP features disabled

---

**Related Specifications**:
- `Character_Arc_Tracking_Specification.md`
- `Emotional_Beat_Enrichment_Specification.md`
- `Analytical_Feedback_Loop_Specification.md`
- `Narrative_Aware_Story_Graph_Specification.md`
- `ApplicationLogic.md`
- `Logging_And_Traceability_Specification.md`
