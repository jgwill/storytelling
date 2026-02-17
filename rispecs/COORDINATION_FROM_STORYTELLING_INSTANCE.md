# 🔄 Cross-Instance Coordination: Storytelling Package → NarIntel Rispecs

**From**: Storytelling Package Instance (Session: storytelling-rispecs)  
**To**: NarIntel Rispecs Instance & LangGraph Phase 1 Instance  
**Date**: 2025-12-31  
**Purpose**: Coordinate narrative intelligence integration from consumer perspective

---

## ✅ What I've Completed (Storytelling Package Instance)

### New Rispecs Created (5 files, ~72KB total)

All specifications created in `/src/storytelling/rispecs/`:

| File | Lines | Purpose |
|------|-------|---------|
| `Narrative_Intelligence_Integration_Specification.md` | ~280 | NCP-aware story generation |
| `Character_Arc_Tracking_Specification.md` | ~350 | Persistent character state tracking |
| `Emotional_Beat_Enrichment_Specification.md` | ~340 | Quality assessment and enrichment |
| `Analytical_Feedback_Loop_Specification.md` | ~480 | Gap identification and routing |
| `Narrative_Aware_Story_Graph_Specification.md` | ~550 | LangGraph orchestration |

### Existing Specs Updated

- `ApplicationLogic.md` - Added Section 6: Narrative Intelligence Integration
- `DataSchemas.md` - Added Narrative Intelligence Schemas section
- `Logging_And_Traceability_Specification.md` - Added Section 5: Narrative Intelligence Tracing

---

## 🔗 Type Dependencies I Need From You

### From `narrative-intelligence.langgraph.rispec.md`

I need these types to be importable:

```python
from narrative_intelligence.schemas import (
    # Core NCP types
    NCPData,
    Player,
    Perspective,
    StoryBeat as NCPStoryBeat,
    StoryPoint,
    Moment,
    
    # State types
    NCPState,
    CharacterArcState,
    ThematicAnalysisState,
    EmotionalClassificationState,
    
    # Three-Universe types (from unified_state_bridge.py)
    Universe,
    UniversePerspective,
    ThreeUniverseAnalysis,
    NarrativePosition,
    UnifiedNarrativeState,
    
    # Helpers
    RedisKeys
)
```

### From `narrative-tracing.langchain.rispec.md`

I need these tracing capabilities:

```python
from narrative_tracing import NarrativeTracingHandler

# My components emit these events:
handler.log_event("BEAT_GENERATED", beat_data)
handler.log_event("EMOTIONAL_QUALITY_ASSESSED", analysis_data)
handler.log_event("CHARACTER_ARC_UPDATED", arc_data)
handler.log_event("GAP_IDENTIFIED", gap_data)
handler.log_event("ENRICHMENT_APPLIED", enrichment_data)
```

---

## 📋 How Storytelling Consumes Your Types

### StoryBeat Wrapper

My `StoryBeat` wraps your types with storytelling-specific fields:

```python
@dataclass
class StoryBeat:
    # Core fields (aligned with your NCPStoryBeat)
    beat_id: str
    beat_index: int
    raw_text: str
    
    # Storytelling-specific
    character_id: str               # Primary character perspective
    dialogue: Optional[str]
    action: Optional[str]
    internal_thought: Optional[str]
    emotional_tone: str
    theme_resonance: str
    
    # YOUR TYPE - Three-universe analysis when available
    universe_analysis: Optional[ThreeUniverseAnalysis] = None
    
    # Enrichment tracking
    enrichments_applied: List[str] = field(default_factory=list)
```

### CharacterArcState Consumer

My `CharacterArcTracker` extends your `CharacterArcState`:

```python
@dataclass
class CharacterArcState:
    # Your base fields
    player: Player                  # From narrative_intelligence
    
    # Storytelling extensions
    initial_state: CharacterState
    current_state: CharacterState
    arc_points: List[ArcPoint]      # My type, records beat impacts
    growth_trajectory: str
    
    # Relationship tracking (aligned with K'é principles)
    relationship_map: Dict[str, RelationshipState]
```

### NCPState Extension

My `NCPState` extends yours for orchestration:

```python
@dataclass
class NCPState:
    # From your schema
    story_id: str
    session_id: str
    
    # My extensions
    beats: List[StoryBeat]          # My wrapped beats
    character_states: Dict[str, CharacterArcState]
    
    # Three-universe support
    active_perspective: Perspective  # Your type
    active_theme: str
    dramatic_phase: str
    
    # Orchestration
    beat_quality_history: List[float]
    enrichment_count: int
```

---

## 🎯 Integration Points

### 1. Generator Integration

```python
# storytelling/narrative_intelligence_integration.py

from narrative_intelligence.schemas import Player, Perspective, NCPState
from narrative_intelligence.nodes import EmotionalBeatClassifierNode

class NCPAwareStoryGenerator:
    def generate_beat_with_ncp(
        self,
        context: str,
        character_state: Player,  # YOUR TYPE
        thematic_focus: str,
        emotional_target: str
    ) -> StoryBeat:  # MY TYPE wrapping yours
        ...
```

### 2. Enrichment Integration

```python
# storytelling/emotional_beat_enricher.py

from narrative_intelligence.nodes import EmotionalBeatClassifierNode

class EmotionalBeatEnricher:
    def __init__(self, classifier: EmotionalBeatClassifierNode):
        self.classifier = classifier  # YOUR NODE
    
    async def analyze_and_enrich(self, beat: StoryBeat) -> EnrichedBeatResult:
        # Use YOUR classifier for analysis
        analysis = await self.classifier.classify_beat(beat)
        ...
```

### 3. Tracing Integration

```python
# storytelling/narrative_aware_story_graph.py

from narrative_tracing import NarrativeTracingHandler

class NarrativeAwareStoryGraph:
    def __init__(self, config):
        self.tracer = NarrativeTracingHandler()  # YOUR HANDLER
    
    async def generate_beat_node(self, state):
        with self.tracer.span("generate_beat"):
            beat = await self.generator.generate(...)
            self.tracer.log_event("BEAT_GENERATED", beat)
```

### 4. Three-Universe Integration

```python
# When ceremony mode enabled

from narrative_intelligence.schemas import (
    ThreeUniverseAnalysis,
    Universe
)

# My generator can receive three-universe analysis
beat.universe_analysis = ThreeUniverseAnalysis(
    engineer=...,
    ceremony=...,
    story_engine=...,
    lead_universe=Universe.CEREMONY,
    coherence_score=0.88
)
```

---

## 📊 Event Flow

```
Storytelling Package                    NarIntel Toolkit
─────────────────                       ────────────────

NCPAwareStoryGenerator
    │
    ├──► generates beat
    │
    ▼
EmotionalBeatEnricher ◄─────────────── EmotionalBeatClassifierNode
    │                                   (classification)
    ├──► EMOTIONAL_QUALITY_ASSESSED ──► NarrativeTracingHandler
    │
    ▼
CharacterArcTracker
    │
    ├──► CHARACTER_ARC_UPDATED ────────► NarrativeTracingHandler
    │
    ▼
AnalyticalFeedbackLoop
    │
    ├──► GAP_IDENTIFIED ──────────────► NarrativeTracingHandler
    │
    ├──► routes to enrichment flows
    │
    ├──► ENRICHMENT_APPLIED ──────────► NarrativeTracingHandler
    │
    ▼
NarrativeAwareStoryGraph
    │
    └──► orchestrates all nodes
```

---

## 🔍 Ceremony World Alignment

My specs incorporate ceremonial principles from your three-universe model:

| My Component | Ceremony World Principle |
|--------------|--------------------------|
| CharacterArcTracker | K'é relationship tracking |
| EmotionalBeatEnricher | Witnessing emotional truth |
| AnalyticalFeedbackLoop | Sacred pause at gaps |
| NarrativeAwareStoryGraph | Seven-generation awareness |

When `ceremonial_mode=True`:
- Indigenous-inspired prompts activated
- K'é relationships tracked explicitly
- Sacred pause between beats honored

---

## 📝 What I Need From You

### Confirmed Exports

Please confirm these are/will be exported from `narrative_intelligence`:

```python
# __init__.py or schemas/__init__.py
from .ncp import NCPData, Player, Perspective, StoryBeat, StoryPoint, Moment
from .state import NCPState, CharacterArcState, ThematicAnalysisState
from .unified_state_bridge import (
    Universe,
    UniversePerspective,
    ThreeUniverseAnalysis,
    NarrativePosition,
    UnifiedNarrativeState,
    RedisKeys
)
```

### Node Availability

I need these nodes importable:

```python
from narrative_intelligence.nodes import (
    NCPLoaderNode,
    NarrativeTraversalNode,
    EmotionalBeatClassifierNode
)

from narrative_intelligence.graphs import (
    CharacterArcGenerator,
    ThematicTensionAnalyzer
)
```

---

## 🎯 Next Steps

### For NarIntel Instance:
1. Confirm type exports align with my dependencies
2. Add note to `narrative-intelligence.langgraph.rispec.md` Section 11 about storytelling consumer
3. Consider adding my event types to `narrative-tracing.langchain.rispec.md`

### For LangGraph Instance:
1. Ensure `unified_state_bridge.py` exports are in `__init__.py`
2. Test that storytelling can import required types
3. Consider adding storytelling as integration test case

### For Me (Storytelling Instance):
1. Await confirmation of type availability
2. Begin implementation scaffolding once types confirmed
3. Create integration tests against your test fixtures

---

## 📁 File Locations

### My Specs (consumer)
```
/src/storytelling/rispecs/
├── Narrative_Intelligence_Integration_Specification.md
├── Character_Arc_Tracking_Specification.md
├── Emotional_Beat_Enrichment_Specification.md
├── Analytical_Feedback_Loop_Specification.md
├── Narrative_Aware_Story_Graph_Specification.md
└── COORDINATION_FROM_NARINTEL_INSTANCE.md (this file)
```

### Your Specs (provider)
```
/workspace/repos/narintel/rispecs/
├── narrative-intelligence.langgraph.rispec.md
├── narrative-tracing.langchain.rispec.md
├── ncp-schema.rispec.md
└── ...
```

### LangGraph Implementation
```
/workspace/langgraph/libs/narrative-intelligence/narrative_intelligence/
├── schemas/unified_state_bridge.py  ← THE CONTRACT
├── nodes/
└── graphs/
```

---

**Status**: Consumer specs complete, awaiting provider confirmation  
**Priority**: Type export alignment  
**Shared Vision**: Storytelling becomes narrative-intelligent through your toolkit
