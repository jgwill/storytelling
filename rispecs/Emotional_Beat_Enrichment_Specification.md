# Emotional Beat Enrichment Specification

**Status**: ⏳ PLANNED (Phase 2 Quality & Analysis)

**Structural Tension**
- Desired Outcome: Automated detection and enrichment of emotionally weak story beats, ensuring consistent emotional resonance throughout generated narratives.
- Current Reality: Generated beats vary in emotional quality without systematic assessment, and weak beats pass through to the final story without enhancement.
- Natural Progression: Introduce EmotionalBeatEnricher that analyzes beats for emotional quality and iteratively strengthens those below threshold.

---

## 1. Overview

This specification defines the emotional beat enrichment system that ensures consistent emotional quality across story generation. The enricher:

1. **Classifies Emotional Content**: Detects emotion type and confidence
2. **Assesses Quality**: Scores emotional resonance and impact
3. **Enriches Weak Beats**: Iteratively improves low-quality beats
4. **Preserves Narrative Intent**: Maintains story coherence during enrichment

## 2. Core Components

### 2.1 EmotionalBeatEnricher

**Purpose**: Analyze and enrich story beats for emotional quality.

**Implementation Location**: `storytelling/emotional_beat_enricher.py`

**Interface**:
```python
class EmotionalBeatEnricher:
    def __init__(
        self,
        classifier_node: EmotionalBeatClassifierNode,
        llm_provider: LLMProvider
    ):
        """Initialize with classifier and LLM provider."""
        
    async def analyze_and_enrich(
        self,
        beat: StoryBeat,
        max_iterations: int = 3
    ) -> EnrichedBeatResult:
        """Analyze beat emotionally, enrich if needed."""
        
    def _build_enrichment_prompt(
        self,
        beat: StoryBeat,
        analysis: EmotionalAnalysis,
        iteration: int
    ) -> str:
        """Construct prompt for emotional strengthening."""
        
    def _update_beat_content(
        self,
        beat: StoryBeat,
        enriched_text: str
    ) -> StoryBeat:
        """Update beat with enriched content."""
```

### 2.2 EmotionalAnalysis

**Purpose**: Comprehensive emotional assessment of a story beat.

**Schema**:
```python
@dataclass
class EmotionalAnalysis:
    # Classification
    primary_emotion: str            # Dominant emotion detected
    secondary_emotions: List[str]   # Supporting emotions
    confidence: float               # Classification confidence (0-1)
    
    # Quality assessment
    emotional_quality: float        # Overall quality score (0-1)
    resonance_score: float          # How well emotion lands (0-1)
    specificity_score: float        # Emotional detail level (0-1)
    authenticity_score: float       # Feels genuine (0-1)
    
    # Dimensional analysis
    valence: float                  # Positive/negative (-1 to 1)
    arousal: float                  # Intensity level (0-1)
    dominance: float                # Power/control (0-1)
    
    # Improvement guidance
    improvement_areas: List[str]    # Specific areas to strengthen
    suggested_techniques: List[str] # Writing techniques to apply
```

### 2.3 EnrichedBeatResult

**Purpose**: Result container for enrichment process.

**Schema**:
```python
@dataclass
class EnrichedBeatResult:
    original_beat: StoryBeat        # Input beat
    final_beat: StoryBeat           # Output beat (may be same as input)
    was_enriched: bool              # Whether enrichment occurred
    iterations_used: int            # Number of enrichment cycles
    
    # Analysis history
    initial_analysis: EmotionalAnalysis
    final_analysis: EmotionalAnalysis
    analysis_history: List[EmotionalAnalysis]
    
    # Quality metrics
    quality_improvement: float      # Delta in quality score
    enrichment_notes: List[str]     # Process notes
```

## 3. Emotional Classification

### 3.1 Emotion Taxonomy

Primary emotion categories:

| Category | Emotions Included |
|----------|-------------------|
| Joy | happiness, delight, contentment, elation, amusement |
| Sadness | grief, melancholy, despair, longing, disappointment |
| Anger | fury, frustration, resentment, irritation, outrage |
| Fear | terror, anxiety, dread, nervousness, apprehension |
| Surprise | shock, amazement, wonder, disbelief, astonishment |
| Disgust | revulsion, contempt, aversion, distaste |
| Trust | faith, admiration, acceptance, confidence |
| Anticipation | hope, expectation, excitement, eagerness |
| Love | affection, tenderness, devotion, passion |
| Shame | guilt, embarrassment, humiliation, remorse |

### 3.2 Classification Process

```python
async def classify_emotion(self, beat: StoryBeat) -> EmotionalAnalysis:
    """
    Classify emotional content of beat.
    
    Process:
    1. Extract emotional cues from text
    2. Identify primary emotion with confidence
    3. Detect secondary emotions
    4. Calculate dimensional values
    5. Assess quality metrics
    """
```

### 3.3 Quality Metrics

| Metric | Description | Scoring Criteria |
|--------|-------------|------------------|
| Resonance | How strongly emotion connects | Visceral impact, reader engagement |
| Specificity | Detail level of emotional expression | Concrete vs abstract language |
| Authenticity | Genuine vs forced feeling | Natural flow, character voice |

## 4. Quality Assessment

### 4.1 Quality Score Calculation

```python
def calculate_emotional_quality(self, analysis: EmotionalAnalysis) -> float:
    """
    Calculate overall emotional quality score.
    
    Weighted components:
    - resonance_score: 0.35
    - specificity_score: 0.25
    - authenticity_score: 0.25
    - confidence: 0.15
    """
    return (
        analysis.resonance_score * 0.35 +
        analysis.specificity_score * 0.25 +
        analysis.authenticity_score * 0.25 +
        analysis.confidence * 0.15
    )
```

### 4.2 Quality Thresholds

| Threshold | Score | Action |
|-----------|-------|--------|
| Excellent | ≥0.85 | No enrichment needed |
| Good | ≥0.75 | Accept, no enrichment |
| Adequate | ≥0.60 | Optional enrichment |
| Weak | ≥0.40 | Enrichment recommended |
| Poor | <0.40 | Enrichment required |

## 5. Enrichment Process

### 5.1 Enrichment Loop

```python
async def analyze_and_enrich(
    self,
    beat: StoryBeat,
    max_iterations: int = 3
) -> EnrichedBeatResult:
    """
    Main enrichment loop.
    
    1. Analyze initial emotional quality
    2. If quality >= threshold, return unchanged
    3. If quality < threshold:
       a. Build enrichment prompt
       b. Generate enriched content
       c. Update beat
       d. Re-analyze
       e. Repeat until threshold met or max iterations
    4. Return result with history
    """
```

### 5.2 Enrichment Prompt Template

```
=== Emotional Enrichment Request ===

The following story beat was analyzed for emotional quality:

--- Original Beat ---
{BEAT_TEXT}

--- Analysis Results ---
Primary Emotion: {PRIMARY_EMOTION}
Confidence: {CONFIDENCE}
Quality Score: {QUALITY_SCORE}

Areas Needing Improvement:
{IMPROVEMENT_AREAS}

--- Enrichment Guidelines ---
To strengthen emotional resonance:

1. STAKES: Make what the character stands to lose/gain clearer
2. SENSORY: Add specific physical sensations and details
3. INTERNAL: Show the character's internal conflict more visibly
4. DIALOGUE: Add specificity and emotional subtext to speech
5. ACTION: Use meaningful physical actions that reveal emotion
6. PACING: Adjust rhythm to match emotional intensity

--- Task ---
Rewrite this beat to achieve stronger {PRIMARY_EMOTION} resonance.
Preserve the narrative content while deepening emotional impact.

{ADDITIONAL_CONTEXT}
```

### 5.3 Enrichment Techniques

Techniques applied based on improvement areas:

| Area | Techniques |
|------|------------|
| Stakes | Explicit consequence mention, ticking clock, irreversibility |
| Sensory | Physical sensation, environmental detail, body language |
| Internal | Thought fragments, memory triggers, cognitive dissonance |
| Dialogue | Subtext, interruption, silence, word choice |
| Action | Telling gestures, involuntary movements, meaningful pauses |
| Pacing | Sentence length variation, white space, repetition |

### 5.4 Iteration Convergence

Track improvement across iterations:

```python
def should_continue_enrichment(
    self,
    current_quality: float,
    previous_quality: float,
    iteration: int,
    max_iterations: int
) -> bool:
    """
    Determine if enrichment should continue.
    
    Stop if:
    - Quality threshold met
    - Max iterations reached
    - Quality not improving (delta < 0.05)
    - Quality decreasing
    """
```

## 6. Narrative Preservation

### 6.1 Content Constraints

During enrichment, preserve:

- **Plot Points**: Key events must remain
- **Character Voice**: Dialogue style consistency
- **Scene Setting**: Location and time markers
- **Relationship Dynamics**: Interpersonal content
- **Thematic Elements**: Theme connections

### 6.2 Validation After Enrichment

```python
def validate_enrichment(
    self,
    original: StoryBeat,
    enriched: StoryBeat
) -> ValidationResult:
    """
    Ensure enrichment preserved narrative elements.
    
    Checks:
    - Key plot elements present
    - Character identification maintained
    - Setting preserved
    - Length within acceptable bounds
    - No contradictions introduced
    """
```

## 7. Integration Points

### 7.1 With NCP-Aware Generator

Post-generation enrichment:

```python
# In generation flow
beat = await generator.generate_beat_with_ncp(...)

# Enrich if needed
result = await enricher.analyze_and_enrich(beat)
final_beat = result.final_beat
```

### 7.2 With Analytical Feedback Loop

Enrichment as gap remediation:

```
Gap identified: "emotional_beat_weak"
    → Route to EmotionalBeatEnricher
        → Enrichment cycle
            → Return enriched beat
```

### 7.3 With Logging/Tracing

Track enrichment in session logs:

```python
# Log enrichment activity
logger.log_enrichment(
    beat_id=beat.beat_id,
    initial_quality=result.initial_analysis.emotional_quality,
    final_quality=result.final_analysis.emotional_quality,
    iterations=result.iterations_used,
    was_enriched=result.was_enriched
)
```

## 8. Ceremony World Alignment

Emotional enrichment honors ceremonial storytelling:

- **Sacred Pause**: Enrichment as reflective moment in generation
- **Emotional Truth**: Seeking authentic emotional expression
- **Relational Awareness**: Emotions in context of relationships
- **Witnessing**: The enricher "witnesses" the beat's emotional content

## 9. Configuration

### 9.1 New Configuration Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `emotional_enrichment_enabled` | bool | true | Enable enrichment |
| `emotional_quality_threshold` | float | 0.75 | Minimum quality to accept |
| `enrichment_max_iterations` | int | 3 | Maximum enrichment cycles |
| `enrichment_min_improvement` | float | 0.05 | Minimum delta to continue |
| `preserve_length_tolerance` | float | 0.20 | Allowed length variation |

### 9.2 Quality Presets

| Preset | Threshold | Iterations | Use Case |
|--------|-----------|------------|----------|
| `fast` | 0.60 | 1 | Quick generation |
| `balanced` | 0.75 | 3 | Standard quality |
| `polished` | 0.85 | 5 | Publication quality |

## 10. Success Criteria

- [ ] Emotions classified with confidence scores
- [ ] Quality assessment generates actionable metrics
- [ ] Weak beats enriched to threshold quality
- [ ] Narrative content preserved during enrichment
- [ ] Enrichment history logged for traceability
- [ ] Iteration convergence prevents infinite loops
- [ ] Integration with feedback loop functional

---

**Related Specifications**:
- `Narrative_Intelligence_Integration_Specification.md`
- `Character_Arc_Tracking_Specification.md`
- `Analytical_Feedback_Loop_Specification.md`
- `Logging_And_Traceability_Specification.md`
