# Narrative-Aware Story Graph Specification

**Status**: ⏳ PLANNED (Phase 3 Orchestration)

**Structural Tension**
- Desired Outcome: A unified orchestration layer that integrates NCP-aware generation, emotional analysis, character tracking, and analytical feedback into a coherent story generation pipeline.
- Current Reality: The existing story graph (`storytelling/graph.py`) generates stories through a linear pipeline without NCP awareness, emotional quality assessment, or feedback-driven enhancement.
- Natural Progression: Introduce NarrativeAwareStoryGraph that wraps the existing workflow with narrative intelligence capabilities while maintaining backward compatibility.

---

## 1. Overview

This specification defines the enhanced story generation graph that unifies all narrative intelligence components into a single orchestrated workflow. The graph:

1. **Initializes NCP State**: Sets up narrative tracking from the start
2. **Generates with Context**: Every beat aware of character arcs and themes
3. **Analyzes in Flight**: Real-time quality assessment during generation
4. **Enriches Dynamically**: Weak beats improved before proceeding
5. **Tracks Everything**: Full observability via Langfuse integration

## 2. Architecture Overview

### 2.1 Graph Structure

```
┌─────────────────────────────────────────────────────────────────────┐
│                    NarrativeAwareStoryGraph                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌──────────────────┐                                               │
│  │  setup_story     │ ← Initialize NCP state, characters, themes   │
│  └────────┬─────────┘                                               │
│           │                                                         │
│           ▼                                                         │
│  ┌──────────────────┐                                               │
│  │  generate_beat   │ ← NCP-aware beat generation                  │
│  └────────┬─────────┘                                               │
│           │                                                         │
│           ▼                                                         │
│  ┌──────────────────┐                                               │
│  │  analyze_beat    │ ← Multi-dimensional analysis + enrichment    │
│  └────────┬─────────┘                                               │
│           │                                                         │
│           ▼                                                         │
│  ┌──────────────────┐                                               │
│  │ track_character  │ ← Update character arcs                       │
│  └────────┬─────────┘                                               │
│           │                                                         │
│           ▼                                                         │
│  ┌──────────────────┐     ┌──────────────────┐                     │
│  │ should_continue? │────▶│  finalize_story  │                     │
│  └────────┬─────────┘     └──────────────────┘                     │
│           │                                                         │
│           │ (continue)                                              │
│           └────────────────────────────▲                           │
│                                        │                           │
│                        (loop back to generate_beat)                │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 2.2 State Flow

```python
NCPState flows through nodes:
  
setup_story:
  - Initializes NCP structures
  - Sets up character tracking
  - Configures theme state

generate_beat:
  - Receives current NCP state
  - Generates beat with full context
  - Returns state with new beat

analyze_beat:
  - Analyzes beat quality
  - Triggers enrichment if needed
  - Returns state with enriched beat

track_character:
  - Updates character arcs
  - Records relationship changes
  - Returns updated state

should_continue:
  - Evaluates narrative completeness
  - Routes to continue or finalize

finalize_story:
  - Calculates final metrics
  - Closes traces
  - Returns completed state
```

## 3. Core Components

### 3.1 NarrativeAwareStoryGraph

**Purpose**: Main orchestration class for narrative-intelligent story generation.

**Implementation Location**: `storytelling/narrative_aware_story_graph.py`

**Interface**:
```python
class NarrativeAwareStoryGraph:
    def __init__(self, config: NarrativeGraphConfig):
        """Initialize with configuration."""
        
    def build_graph(self) -> StateGraph:
        """Construct the LangGraph state machine."""
        
    async def invoke(
        self,
        initial_state: NCPState
    ) -> NCPState:
        """Execute complete story generation."""
        
    # Node implementations
    async def setup_story_node(self, state: NCPState) -> NCPState
    async def generate_beat_node(self, state: NCPState) -> NCPState
    async def analyze_beat_node(self, state: NCPState) -> NCPState
    async def track_character_node(self, state: NCPState) -> NCPState
    async def finalize_story_node(self, state: NCPState) -> NCPState
    
    # Routing
    def should_continue_story(self, state: NCPState) -> str
```

### 3.2 NarrativeGraphConfig

**Purpose**: Configuration for the narrative-aware graph.

**Schema**:
```python
@dataclass
class NarrativeGraphConfig:
    # LLM Configuration
    llm_provider: LLMProvider
    
    # Component configuration
    ncp_generator_config: NCPGeneratorConfig
    enricher_config: EnricherConfig
    tracker_config: TrackerConfig
    feedback_config: FeedbackLoopConfig
    
    # Graph behavior
    max_beats: int = 50
    quality_threshold: float = 0.75
    enable_enrichment: bool = True
    enable_tracing: bool = True
    
    # Ceremony World options
    ceremonial_mode: bool = False
    indigenous_prompts: bool = True
```

### 3.3 NCPState (Extended)

**Purpose**: Complete narrative state passed through graph nodes.

**Schema**:
```python
@dataclass
class NCPState:
    # Story identity
    story_id: str
    session_id: str
    trace_id: Optional[str]
    
    # Narrative content
    beats: List[StoryBeat]
    outline: str
    story_elements: Dict[str, Any]
    
    # NCP tracking
    active_perspective: Perspective
    active_theme: str
    dramatic_phase: str
    tension_level: float
    
    # Character tracking
    character_states: Dict[str, CharacterArcState]
    relationships: Dict[str, RelationshipState]
    
    # Theme tracking
    thematic_threads: List[ThematicThread]
    theme_resonance_history: List[float]
    
    # Quality metrics
    beat_quality_history: List[float]
    enrichment_count: int
    
    # Control flow
    current_chapter: int
    current_beat_index: int
    should_conclude: bool
    
    # Metadata
    generation_start_time: str
    last_checkpoint_time: str
```

## 4. Node Implementations

### 4.1 setup_story_node

**Purpose**: Initialize all NCP structures and tracking systems.

```python
async def setup_story_node(self, state: NCPState) -> NCPState:
    """
    Initialize story with NCP structure.
    
    1. Start Langfuse trace for story
    2. Load NCP schema if provided
    3. Initialize characters from story_elements
    4. Set up theme tracking
    5. Configure initial perspective
    6. Set dramatic phase to "setup"
    7. Return initialized state
    """
    with self.tracer.create_story_generation_root_trace(state.story_id) as trace:
        state.trace_id = trace.id
        
        # Initialize character tracking
        for character in state.story_elements.get("characters", []):
            self.arc_tracker.initialize_character(character)
            state.character_states[character.id] = self.arc_tracker.get_state(character.id)
        
        # Initialize theme tracking
        state.thematic_threads = self._extract_themes(state.story_elements)
        state.active_theme = state.thematic_threads[0].name if state.thematic_threads else "general"
        
        # Set initial perspective
        protagonist = self._identify_protagonist(state.story_elements)
        state.active_perspective = Perspective(
            player=protagonist,
            type="third_limited"
        )
        
        # Set dramatic phase
        state.dramatic_phase = "setup"
        state.tension_level = 0.3
        
        return state
```

### 4.2 generate_beat_node

**Purpose**: Generate next story beat with full NCP awareness.

```python
async def generate_beat_node(self, state: NCPState) -> NCPState:
    """
    Generate next beat with NCP context.
    
    1. Get current character and arc context
    2. Determine emotional target for phase
    3. Build context from previous beats
    4. Generate beat via NCPAwareStoryGenerator
    5. Add beat to state
    6. Return updated state
    """
    with self.tracer.span("generate_beat", beat_index=state.current_beat_index):
        # Get current perspective character
        current_character = state.active_perspective.player
        
        # Get arc context for character
        arc_context = self.arc_tracker.get_character_arc_context(
            current_character,
            depth=self.config.ncp_generator_config.context_depth
        )
        
        # Determine emotional target based on dramatic phase
        emotional_target = self._determine_emotional_target(
            state.dramatic_phase,
            state.tension_level
        )
        
        # Build story context from recent beats
        story_context = self._build_story_context(state.beats[-5:])
        
        # Generate beat
        beat = await self.ncp_generator.generate_beat_with_ncp(
            context=story_context,
            character_state=current_character,
            character_arc_context=arc_context,
            thematic_focus=state.active_theme,
            emotional_target=emotional_target
        )
        
        # Add to state
        beat.beat_index = state.current_beat_index
        state.beats.append(beat)
        state.current_beat_index += 1
        
        return state
```

### 4.3 analyze_beat_node

**Purpose**: Analyze beat and enrich if quality is insufficient.

```python
async def analyze_beat_node(self, state: NCPState) -> NCPState:
    """
    Analyze beat and trigger enrichment if needed.
    
    1. Get last generated beat
    2. Run through analytical feedback loop
    3. Update beat with enriched version
    4. Record quality metrics
    5. Return updated state
    """
    with self.tracer.span("analyze_beat"):
        beat = state.beats[-1]
        
        # Run through feedback loop
        enriched_result = await self.feedback_loop.process_beat_with_analysis(
            beat=beat,
            ncp_state=state
        )
        
        # Update beat in state
        state.beats[-1] = enriched_result.beat
        
        # Record metrics
        state.beat_quality_history.append(enriched_result.final_quality)
        if enriched_result.was_enriched:
            state.enrichment_count += 1
        
        # Log to trace
        self.tracer.log_beat_analysis(
            beat_id=beat.beat_id,
            initial_quality=enriched_result.initial_quality,
            final_quality=enriched_result.final_quality,
            enrichments_applied=len(enriched_result.enrichments)
        )
        
        return state
```

### 4.4 track_character_node

**Purpose**: Update character arcs based on beat content.

```python
async def track_character_node(self, state: NCPState) -> NCPState:
    """
    Update character arcs from beat.
    
    1. Get last beat
    2. Identify characters involved
    3. Record impact on each character's arc
    4. Update relationship states if applicable
    5. Advance dramatic phase if warranted
    6. Return updated state
    """
    with self.tracer.span("track_character"):
        beat = state.beats[-1]
        
        # Get characters involved in beat
        involved_characters = self._identify_involved_characters(beat, state)
        
        # Record impact for each
        for character in involved_characters:
            arc_point = self.arc_tracker.record_beat_impact(beat, character)
            state.character_states[character.id] = self.arc_tracker.get_state(character.id)
        
        # Update relationships
        self._update_relationships(beat, state)
        
        # Check for dramatic phase transition
        new_phase = self._evaluate_phase_transition(state)
        if new_phase != state.dramatic_phase:
            state.dramatic_phase = new_phase
            state.tension_level = self._get_tension_for_phase(new_phase)
        
        return state
```

### 4.5 finalize_story_node

**Purpose**: Complete story generation with final metrics and trace closure.

```python
async def finalize_story_node(self, state: NCPState) -> NCPState:
    """
    Complete story with final metrics.
    
    1. Calculate final quality metrics
    2. Generate story summary
    3. Close Langfuse trace with metrics
    4. Save final checkpoint
    5. Return completed state
    """
    with self.tracer.span("finalize_story"):
        # Calculate metrics
        metrics = self._calculate_final_metrics(state)
        
        # Generate summary
        story_text = self._compile_story(state.beats)
        
        # Close trace
        self.tracer.finalize_story_trace(
            trace_id=state.trace_id,
            story=story_text,
            metrics=metrics
        )
        
        # Mark complete
        state.should_conclude = True
        
        return state
```

### 4.6 should_continue_story

**Purpose**: Routing function to determine if story should continue or finalize.

```python
def should_continue_story(self, state: NCPState) -> str:
    """
    Determine if story should continue.
    
    Finalize if:
    - Max beats reached
    - Story explicitly concluded
    - All character arcs resolved
    - Theme resolution achieved
    - Dramatic phase is "resolution" and tension resolved
    
    Returns: "continue" or "finish"
    """
    # Check max beats
    if state.current_beat_index >= self.config.max_beats:
        return "finish"
    
    # Check explicit conclusion
    if state.should_conclude:
        return "finish"
    
    # Check chapter completion (if in chapter mode)
    if state.current_chapter > len(state.outline_chapters):
        return "finish"
    
    # Check dramatic resolution
    if state.dramatic_phase == "resolution" and state.tension_level < 0.2:
        return "finish"
    
    return "continue"
```

## 5. Graph Construction

### 5.1 build_graph Method

```python
def build_graph(self) -> StateGraph:
    """
    Construct the LangGraph state machine.
    """
    graph = StateGraph(NCPState)
    
    # Add nodes
    graph.add_node("setup_story", self.setup_story_node)
    graph.add_node("generate_beat", self.generate_beat_node)
    graph.add_node("analyze_beat", self.analyze_beat_node)
    graph.add_node("track_character", self.track_character_node)
    graph.add_node("finalize_story", self.finalize_story_node)
    
    # Set entry point
    graph.set_entry_point("setup_story")
    
    # Add edges
    graph.add_edge("setup_story", "generate_beat")
    graph.add_edge("generate_beat", "analyze_beat")
    graph.add_edge("analyze_beat", "track_character")
    
    # Add conditional routing
    graph.add_conditional_edges(
        "track_character",
        self.should_continue_story,
        {
            "continue": "generate_beat",
            "finish": "finalize_story"
        }
    )
    
    return graph.compile()
```

## 6. Integration with Existing System

### 6.1 Backward Compatibility

The NarrativeAwareStoryGraph can be used alongside or instead of the existing graph:

```python
# Existing usage (unchanged)
from storytelling.graph import StorytellingGraph
graph = StorytellingGraph(config)
result = await graph.invoke(state)

# New narrative-aware usage
from storytelling.narrative_aware_story_graph import NarrativeAwareStoryGraph
narrative_graph = NarrativeAwareStoryGraph(narrative_config)
result = await narrative_graph.invoke(initial_ncp_state)
```

### 6.2 Feature Flag Integration

```python
# In main entry point
if config.narrative_intelligence_enabled:
    graph = NarrativeAwareStoryGraph(config)
else:
    graph = StorytellingGraph(config)
```

### 6.3 State Conversion

```python
def convert_to_ncp_state(standard_state: Dict) -> NCPState:
    """Convert standard state to NCPState for narrative processing."""
    
def convert_from_ncp_state(ncp_state: NCPState) -> Dict:
    """Convert NCPState back to standard format for output."""
```

## 7. Langfuse Tracing Integration

### 7.1 NarrativeTracingHandler

```python
class NarrativeTracingHandler:
    """Handle Langfuse tracing for narrative-aware generation."""
    
    def create_story_generation_root_trace(self, story_id: str) -> Trace:
        """Create root trace for entire story generation."""
        
    def span(self, name: str, **kwargs) -> Span:
        """Create span within current trace."""
        
    def log_beat_analysis(self, **kwargs) -> None:
        """Log beat analysis results."""
        
    def log_enrichment(self, **kwargs) -> None:
        """Log enrichment activity."""
        
    def finalize_story_trace(self, **kwargs) -> None:
        """Close trace with final metrics."""
```

### 7.2 Trace Structure

```
Story Generation Trace
├── setup_story
│   ├── character_initialization (per character)
│   └── theme_setup
├── generate_beat (repeated)
│   ├── context_building
│   ├── llm_generation
│   └── beat_parsing
├── analyze_beat (repeated)
│   ├── character_analysis
│   ├── emotional_analysis
│   ├── thematic_analysis
│   └── enrichment (if triggered)
├── track_character (repeated)
│   └── arc_point_recording
└── finalize_story
    ├── metrics_calculation
    └── story_compilation
```

## 8. Ceremony World Mode

### 8.1 Ceremonial Mode Activation

```python
if config.ceremonial_mode:
    # Use indigenous-inspired prompts
    self.ncp_generator.use_ceremonial_prompts = True
    
    # Enable K'é relationship tracking
    self.arc_tracker.use_ke_relationships = True
    
    # Add sacred pause between beats
    self.pause_between_beats = True
    
    # Seven-generation theme awareness
    self.theme_tracker.seven_generation_mode = True
```

### 8.2 Ceremonial Prompts Integration

When ceremonial mode is active:
- Prompts incorporate spiral narrative structure
- Two-Eyed Seeing principles guide perspective shifts
- Relational science informs character interactions

## 9. Configuration

### 9.1 Configuration Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `narrative_graph_enabled` | bool | false | Enable narrative-aware graph |
| `max_beats_per_chapter` | int | 10 | Beats per chapter limit |
| `phase_transition_threshold` | float | 0.7 | Tension level for phase changes |
| `enable_beat_enrichment` | bool | true | Enable automatic enrichment |
| `enable_character_tracking` | bool | true | Enable arc tracking |
| `enable_langfuse_tracing` | bool | true | Enable observability |
| `ceremonial_mode` | bool | false | Enable Ceremony World features |

### 9.2 Graph Presets

| Preset | Description | Settings |
|--------|-------------|----------|
| `fast` | Quick generation | Enrichment off, minimal tracking |
| `balanced` | Standard quality | All features, moderate thresholds |
| `quality` | Maximum quality | All features, strict thresholds |
| `ceremonial` | Ceremony World | Ceremonial mode, indigenous prompts |

## 10. Success Criteria

- [ ] Graph compiles and executes end-to-end
- [ ] NCP state properly initialized with story elements
- [ ] Beats generated with character arc context
- [ ] Analysis runs on each generated beat
- [ ] Enrichment triggered for low-quality beats
- [ ] Character arcs updated after each beat
- [ ] Dramatic phase transitions appropriately
- [ ] Story concludes at appropriate point
- [ ] Full trace captured in Langfuse
- [ ] Backward compatibility maintained

---

**Related Specifications**:
- `Narrative_Intelligence_Integration_Specification.md`
- `Character_Arc_Tracking_Specification.md`
- `Emotional_Beat_Enrichment_Specification.md`
- `Analytical_Feedback_Loop_Specification.md`
- `ApplicationLogic.md`
- `Logging_And_Traceability_Specification.md`
