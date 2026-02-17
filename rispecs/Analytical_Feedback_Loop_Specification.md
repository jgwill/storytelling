# Analytical Feedback Loop Specification

**Status**: ⏳ PLANNED (Phase 2 Quality & Analysis)

**Structural Tension**
- Desired Outcome: A closed-loop system where analytical insights from generated content drive targeted improvements, creating progressively higher-quality narrative output.
- Current Reality: Story generation proceeds linearly without systematic analysis of generated content or feedback-driven enhancement cycles.
- Natural Progression: Introduce AnalyticalFeedbackLoop that orchestrates multi-dimensional analysis, identifies quality gaps, routes to appropriate enrichment flows, and integrates improvements.

---

## 1. Overview

This specification defines the analytical feedback loop that closes the generation-analysis-enrichment cycle. The loop:

1. **Analyzes Generated Content**: Multi-dimensional quality assessment
2. **Identifies Gaps**: Specific areas needing improvement
3. **Routes to Enrichment**: Selects appropriate flows for each gap
4. **Applies Improvements**: Integrates enriched content back into narrative
5. **Validates Results**: Ensures improvements meet quality standards

## 2. Core Components

### 2.1 AnalyticalFeedbackLoop

**Purpose**: Orchestrate the complete analysis → gap → enrichment → integration cycle.

**Implementation Location**: `storytelling/analytical_feedback_loop.py`

**Interface**:
```python
class AnalyticalFeedbackLoop:
    def __init__(
        self,
        character_arc_analyzer: CharacterArcAnalyzer,
        thematic_analyzer: ThematicAnalyzer,
        emotional_classifier: EmotionalClassifier,
        flow_router: NarrativeFlowRouter,
        llm_provider: LLMProvider
    ):
        """Initialize with all analyzer components."""
        
    async def process_beat_with_analysis(
        self,
        beat: StoryBeat,
        ncp_state: NCPState
    ) -> EnrichedBeat:
        """Complete analysis → enrichment pipeline."""
        
    def _identify_gaps(
        self,
        character_analysis: CharacterAnalysisResult,
        thematic_analysis: ThematicAnalysisResult,
        emotional_analysis: EmotionalAnalysis
    ) -> List[Gap]:
        """From analysis results, identify improvement areas."""
        
    async def _execute_enrichment_flow(
        self,
        beat: StoryBeat,
        flow: FlowRoute,
        gap: Gap
    ) -> Enrichment:
        """Execute enrichment for a specific gap."""
        
    def _apply_enrichment(
        self,
        beat: StoryBeat,
        enrichment: Enrichment
    ) -> StoryBeat:
        """Integrate enrichment while preserving continuity."""
```

### 2.2 Gap

**Purpose**: Represent a specific quality deficiency identified in analysis.

**Schema**:
```python
@dataclass
class Gap:
    gap_id: str                     # Unique identifier
    gap_type: str                   # Category of gap
    dimension: str                  # Analysis dimension (character/theme/emotion)
    
    # Assessment
    score: float                    # Quality score (0-1, low = needs improvement)
    severity: str                   # "critical" | "major" | "minor"
    confidence: float               # Confidence in gap identification
    
    # Context
    description: str                # Human-readable description
    evidence: List[str]             # Specific textual evidence
    suggested_flows: List[str]      # Recommended enrichment flows
    
    # Metadata
    beat_id: str                    # Associated beat
    timestamp: str                  # When identified
```

### 2.3 Enrichment

**Purpose**: Represent the result of an enrichment flow execution.

**Schema**:
```python
@dataclass
class Enrichment:
    enrichment_id: str              # Unique identifier
    gap_id: str                     # Gap this addresses
    flow_used: str                  # Flow that produced this
    
    # Content
    original_content: str           # What was enriched
    enriched_content: str           # Result of enrichment
    content_type: str               # "dialogue" | "action" | "full_beat"
    
    # Quality
    improvement_score: float        # Estimated improvement
    validation_passed: bool         # Did validation succeed
    
    # Metadata
    execution_time_ms: int          # Processing time
    llm_tokens_used: int            # Token consumption
```

### 2.4 EnrichedBeat

**Purpose**: Complete result of feedback loop processing.

**Schema**:
```python
@dataclass
class EnrichedBeat:
    # Beat content
    beat: StoryBeat                 # Final enriched beat
    original_beat: StoryBeat        # Input for comparison
    
    # Enrichment history
    enrichments: List[Enrichment]   # All enrichments applied
    gaps_identified: List[Gap]      # All gaps found
    gaps_addressed: List[Gap]       # Gaps successfully addressed
    gaps_remaining: List[Gap]       # Gaps that couldn't be addressed
    
    # Analysis records
    character_analysis: CharacterAnalysisResult
    thematic_analysis: ThematicAnalysisResult
    emotional_analysis: EmotionalAnalysis
    
    # Quality metrics
    initial_quality: float          # Pre-enrichment quality
    final_quality: float            # Post-enrichment quality
    quality_delta: float            # Improvement achieved
```

## 3. Multi-Dimensional Analysis

### 3.1 Analysis Dimensions

| Dimension | Analyzer | Aspects Assessed |
|-----------|----------|------------------|
| Character | CharacterArcAnalyzer | Arc consistency, motivation clarity, voice |
| Theme | ThematicAnalyzer | Theme resonance, symbolic depth, coherence |
| Emotion | EmotionalClassifier | Emotional quality, resonance, authenticity |
| Structure | StructuralAnalyzer | Pacing, tension, beat placement |

### 3.2 Parallel Analysis

```python
async def analyze_beat_multidimensional(
    self,
    beat: StoryBeat,
    ncp_state: NCPState
) -> AnalysisBundle:
    """
    Run all analyses in parallel for efficiency.
    """
    character_task = self.character_arc_analyzer.analyze_impact(beat, ncp_state)
    thematic_task = self.thematic_analyzer.analyze_resonance(beat, ncp_state)
    emotional_task = self.emotional_classifier.classify(beat)
    
    results = await asyncio.gather(
        character_task,
        thematic_task,
        emotional_task
    )
    
    return AnalysisBundle(
        character=results[0],
        thematic=results[1],
        emotional=results[2]
    )
```

## 4. Gap Identification

### 4.1 Gap Types

| Gap Type | Dimension | Trigger Condition | Severity |
|----------|-----------|-------------------|----------|
| `character_inconsistency` | Character | Consistency score < 0.6 | Major |
| `character_motivation_unclear` | Character | Motivation clarity < 0.5 | Critical |
| `character_voice_drift` | Character | Voice score < 0.7 | Minor |
| `emotional_beat_weak` | Emotion | Quality score < 0.6 | Major |
| `emotion_mismatch` | Emotion | Target vs actual mismatch | Major |
| `theme_not_resonant` | Theme | Resonance score < 0.5 | Minor |
| `theme_contradiction` | Theme | Contradiction detected | Critical |
| `pacing_issue` | Structure | Tension flow disrupted | Minor |
| `arc_regression` | Character | Unintended arc reversal | Major |

### 4.2 Gap Identification Logic

```python
def _identify_gaps(
    self,
    character_analysis: CharacterAnalysisResult,
    thematic_analysis: ThematicAnalysisResult,
    emotional_analysis: EmotionalAnalysis
) -> List[Gap]:
    """
    Systematically identify gaps from analysis results.
    
    Process:
    1. Check each dimension against thresholds
    2. Create Gap objects for deficiencies
    3. Prioritize by severity
    4. Attach suggested flows
    """
    gaps = []
    
    # Character dimension
    if character_analysis.consistency_score < 0.6:
        gaps.append(Gap(
            gap_type="character_inconsistency",
            dimension="character",
            score=character_analysis.consistency_score,
            severity="major",
            suggested_flows=["character_consistency_enhancer"]
        ))
    
    # Emotion dimension
    if emotional_analysis.emotional_quality < 0.6:
        gaps.append(Gap(
            gap_type="emotional_beat_weak",
            dimension="emotion",
            score=emotional_analysis.emotional_quality,
            severity="major",
            suggested_flows=["emotional_beat_enricher"]
        ))
    
    # Theme dimension
    if thematic_analysis.resonance_score < 0.5:
        gaps.append(Gap(
            gap_type="theme_not_resonant",
            dimension="theme",
            score=thematic_analysis.resonance_score,
            severity="minor",
            suggested_flows=["thematic_deepener"]
        ))
    
    return sorted(gaps, key=lambda g: severity_order(g.severity))
```

### 4.3 Severity Prioritization

```python
def severity_order(severity: str) -> int:
    """Return sort order for severity (lower = higher priority)."""
    return {"critical": 0, "major": 1, "minor": 2}.get(severity, 3)
```

## 5. Flow Routing

### 5.1 NarrativeFlowRouter

**Purpose**: Select appropriate enrichment flows for identified gaps.

**Interface**:
```python
class NarrativeFlowRouter:
    def select_flows(
        self,
        narrative_state: NCPState,
        gap_analysis: Gap
    ) -> List[FlowRoute]:
        """
        Select enrichment flows based on gap and narrative context.
        
        Considers:
        - Gap type and severity
        - Current narrative phase
        - Character involved
        - Available flows
        - Resource constraints
        """
```

### 5.2 Flow Registry

| Flow ID | Purpose | Gap Types Addressed |
|---------|---------|---------------------|
| `emotional_beat_enricher` | Strengthen emotional resonance | emotional_beat_weak |
| `character_consistency_enhancer` | Align with character arc | character_inconsistency, character_voice_drift |
| `motivation_clarifier` | Make motivations explicit | character_motivation_unclear |
| `thematic_deepener` | Strengthen theme connections | theme_not_resonant |
| `dialogue_enhancer` | Improve dialogue quality | character_voice_drift, emotional_beat_weak |
| `tension_adjuster` | Fix pacing issues | pacing_issue |

### 5.3 Flow Selection Logic

```python
def select_flows(
    self,
    narrative_state: NCPState,
    gap_analysis: Gap
) -> List[FlowRoute]:
    """
    Flow selection considers:
    1. Primary flow for gap type
    2. Supporting flows based on context
    3. Narrative phase appropriateness
    4. Resource budget
    """
    primary_flow = self.flow_registry.get(gap_analysis.gap_type)
    supporting_flows = self._get_supporting_flows(gap_analysis, narrative_state)
    
    return [primary_flow] + supporting_flows
```

## 6. Enrichment Execution

### 6.1 Flow Execution Pipeline

```python
async def _execute_enrichment_flow(
    self,
    beat: StoryBeat,
    flow: FlowRoute,
    gap: Gap
) -> Enrichment:
    """
    Execute single enrichment flow.
    
    Steps:
    1. Prepare flow input with beat and gap context
    2. Execute flow (LLM call or agent invocation)
    3. Parse flow output
    4. Validate enrichment
    5. Return enrichment result
    """
```

### 6.2 Flow Input Preparation

```python
def prepare_flow_input(
    self,
    beat: StoryBeat,
    gap: Gap,
    ncp_state: NCPState
) -> FlowInput:
    """
    Construct input for enrichment flow.
    
    Includes:
    - Original beat content
    - Gap description and evidence
    - Character arc context (if relevant)
    - Theme context (if relevant)
    - Specific improvement instructions
    """
```

### 6.3 Enrichment Validation

```python
def validate_enrichment(
    self,
    original: StoryBeat,
    enrichment: Enrichment
) -> ValidationResult:
    """
    Validate enrichment maintains narrative integrity.
    
    Checks:
    - Content not drastically different
    - Key plot elements preserved
    - Character identification maintained
    - Length within bounds
    - No new contradictions
    """
```

## 7. Enrichment Application

### 7.1 Merge Strategy

```python
def _apply_enrichment(
    self,
    beat: StoryBeat,
    enrichment: Enrichment
) -> StoryBeat:
    """
    Apply enrichment to beat.
    
    Strategies:
    - "replace": Full content replacement
    - "merge_dialogue": Replace dialogue only
    - "merge_action": Replace action only
    - "augment": Add to existing content
    """
```

### 7.2 Conflict Resolution

When multiple enrichments apply:

```python
def resolve_enrichment_conflicts(
    self,
    beat: StoryBeat,
    enrichments: List[Enrichment]
) -> StoryBeat:
    """
    Apply multiple enrichments with conflict resolution.
    
    Priority:
    1. Critical gap enrichments first
    2. Non-overlapping enrichments in parallel
    3. Overlapping enrichments merged by priority
    """
```

## 8. Quality Validation

### 8.1 Post-Enrichment Validation

```python
async def validate_final_quality(
    self,
    enriched_beat: EnrichedBeat
) -> ValidationReport:
    """
    Verify enrichment improved quality.
    
    Checks:
    - Original gaps addressed
    - No new gaps introduced
    - Overall quality improved
    - Narrative coherence maintained
    """
```

### 8.2 Rollback Mechanism

```python
def rollback_enrichment(
    self,
    enriched_beat: EnrichedBeat
) -> StoryBeat:
    """
    Rollback to original if enrichment degraded quality.
    
    Triggered when:
    - Validation fails
    - Quality decreased
    - New critical gaps introduced
    """
```

## 9. Orchestration Flow

### 9.1 Complete Pipeline

```
1. RECEIVE beat from generator
   │
2. ANALYZE beat (parallel)
   ├── Character Arc Analysis
   ├── Thematic Analysis
   └── Emotional Classification
   │
3. IDENTIFY gaps from analysis
   │
4. IF no gaps:
   │   └── RETURN beat unchanged
   │
5. FOR each gap (priority order):
   │   ├── SELECT enrichment flow(s)
   │   ├── EXECUTE flow(s)
   │   └── APPLY enrichment
   │
6. VALIDATE final quality
   │
7. IF validation fails:
   │   └── ROLLBACK and RETURN original
   │
8. RETURN enriched beat
```

### 9.2 Resource Management

```python
class FeedbackLoopResourceManager:
    """Manage resources for feedback loop execution."""
    
    def __init__(self, config: FeedbackLoopConfig):
        self.max_enrichments_per_beat = config.max_enrichments
        self.token_budget = config.token_budget
        self.time_budget_ms = config.time_budget_ms
    
    def can_execute_flow(self, flow: FlowRoute) -> bool:
        """Check if resources allow flow execution."""
    
    def record_usage(self, enrichment: Enrichment) -> None:
        """Track resource consumption."""
```

## 10. Integration Points

### 10.1 With Story Generation Graph

```python
# In narrative_aware_story_graph.py
async def analyze_beat_node(self, state: NCPState) -> NCPState:
    beat = state.get_last_beat()
    
    enriched_beat = await self.feedback_loop.process_beat_with_analysis(
        beat=beat,
        ncp_state=state
    )
    
    state.update_last_beat(enriched_beat)
    return state
```

### 10.2 With Langfuse Tracing

```python
# Trace feedback loop execution
with tracer.span("feedback_loop", beat_id=beat.beat_id) as span:
    # Log analysis results
    span.log_analysis(analysis_bundle)
    
    # Log gaps identified
    span.log_gaps(gaps)
    
    # Log enrichments applied
    for enrichment in enrichments:
        span.log_enrichment(enrichment)
    
    # Log final quality
    span.log_quality(initial=initial_quality, final=final_quality)
```

## 11. Ceremony World Alignment

The feedback loop embodies ceremonial principles:

- **Witnessing**: Analysis as witnessing the beat's qualities
- **Sacred Pause**: Gap identification as reflective pause
- **Transformation**: Enrichment as guided transformation
- **Integration**: Applying improvements with care for wholeness

## 12. Configuration

### 12.1 Configuration Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `feedback_loop_enabled` | bool | true | Enable feedback loop |
| `max_enrichments_per_beat` | int | 3 | Maximum enrichments per beat |
| `gap_severity_threshold` | str | "major" | Minimum severity to address |
| `quality_improvement_threshold` | float | 0.05 | Minimum improvement to accept |
| `parallel_analysis` | bool | true | Run analyses in parallel |
| `token_budget_per_beat` | int | 2000 | Token limit for enrichment |

### 12.2 Resource Presets

| Preset | Max Enrichments | Token Budget | Use Case |
|--------|-----------------|--------------|----------|
| `minimal` | 1 | 500 | Fast generation |
| `balanced` | 3 | 2000 | Standard quality |
| `thorough` | 5 | 5000 | High quality |
| `unlimited` | -1 | -1 | Maximum quality |

## 13. Success Criteria

- [ ] Multi-dimensional analysis executes in parallel
- [ ] Gaps identified with severity and flow mapping
- [ ] Flow router selects appropriate enrichment flows
- [ ] Enrichments applied without breaking narrative
- [ ] Quality validation prevents degradation
- [ ] Rollback mechanism functional
- [ ] Resource management respects budgets
- [ ] Full tracing in Langfuse

---

**Related Specifications**:
- `Narrative_Intelligence_Integration_Specification.md`
- `Character_Arc_Tracking_Specification.md`
- `Emotional_Beat_Enrichment_Specification.md`
- `Narrative_Aware_Story_Graph_Specification.md`
- `Logging_And_Traceability_Specification.md`
