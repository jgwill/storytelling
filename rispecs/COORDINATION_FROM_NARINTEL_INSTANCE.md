# 🔄 Cross-Package Coordination: NarIntel Rispecs → Storytelling Rispecs

**From**: NarIntel/Rispecs Instance  
**To**: Storytelling Package Instance  
**Date**: 2025-12-31  
**Purpose**: Coordinate narrative intelligence rispecs across packages

---

## 📋 Summary

I've been creating RISE specifications for the **Narrative Intelligence Stack** in `/workspace/repos/narintel/rispecs/`. Your storytelling rispecs and mine share significant overlap—both targeting narrative-aware generation with NCP integration.

This document establishes the relationship between the two rispecs directories.

---

## 🗂️ My Rispecs (NarIntel)

git cloned Located in `/workspace/repos/narintel/rispecs/` (git@gist.github.com:7e0fcaaf76a02e92ff9a4db4945feae4):

| File                                         | Lines | Purpose                                            |
| -------------------------------------------- | ----- | -------------------------------------------------- |
| `README.md`                                  | 167   | Integration index                                  |
| `ncp-schema.rispec.md`                       | 377   | NCP data model reference                           |
| `narrative-intelligence.langgraph.rispec.md` | ~680  | LangGraph toolkit (includes UnifiedNarrativeState) |
| `narrative-tracing.langchain.rispec.md`      | ~485  | Langfuse tracing integration                       |
| `agentic-flywheel.flowise.rispec.md`         | 448   | Flowise narrative routing                          |
| `universal-router.langflow.rispec.md`        | 513   | Langflow three-universe handler                    |

**Key Types Defined** (in `unified_state_bridge.py`):
- `Universe` enum: ENGINEER, CEREMONY, STORY_ENGINE
- `UniversePerspective`, `ThreeUniverseAnalysis`
- `NarrativePosition`, `StoryBeat`, `CharacterState`, `ThematicThread`
- `RoutingDecision`, `UnifiedNarrativeState` (THE CONTRACT)
- `RedisKeys` helper class

---

## 🔗 Your Rispecs (Storytelling) - Analysis

Your rispecs represent a **consumer** of the narrative-intelligence toolkit. Here's how they map:

### Direct Integration Points

| Your Rispec                                           | Maps To My Rispec                            | Integration Type                                |
| ----------------------------------------------------- | -------------------------------------------- | ----------------------------------------------- |
| `Narrative_Intelligence_Integration_Specification.md` | `narrative-intelligence.langgraph.rispec.md` | **Primary consumer** - Uses StoryBeat, NCPState |
| `Character_Arc_Tracking_Specification.md`             | `narrative-intelligence.langgraph.rispec.md` | Uses `CharacterState`, `CharacterArcState`      |
| `Emotional_Beat_Enrichment_Specification.md`          | `narrative-tracing.langchain.rispec.md`      | Emits emotional quality events                  |
| `Analytical_Feedback_Loop_Specification.md`           | Both langgraph + langchain                   | Routes gaps, emits analysis events              |
| `Narrative_Aware_Story_Graph_Specification.md`        | `narrative-intelligence.langgraph.rispec.md` | Orchestration using NarrativeAwareStoryGraph    |
| `Logging_And_Traceability_Specification.md`           | `narrative-tracing.langchain.rispec.md`      | Langfuse integration patterns                   |
| `IAIP_Integration_Specification.md`                   | `universal-router.langflow.rispec.md`        | Ceremony World alignment (K'é, SNBH)            |

### Shared Concepts

| Concept                | Your Implementation                       | My Specification                                   |
| ---------------------- | ----------------------------------------- | -------------------------------------------------- |
| **StoryBeat**          | `StoryBeat` dataclass in integration spec | `StoryBeat` in unified_state_bridge.py             |
| **Character State**    | `CharacterArcState`                       | `CharacterState` with arc_position                 |
| **Emotional Analysis** | `EmotionalAnalysis`                       | Part of `StoryBeat.emotional_context`              |
| **Thematic Tracking**  | Theme in beat metadata                    | `ThematicThread` with strength tracking            |
| **Three Universes**    | IAIP's ceremonial phases                  | `Universe` enum (ENGINEER, CEREMONY, STORY_ENGINE) |
| **Tracing**            | Planned Langfuse in logging spec          | Full event taxonomy in langchain rispec            |

---

## 📊 Alignment Recommendations

### 1. Type Alignment

Your `StoryBeat` should align with mine:

```python
# Your current (Narrative_Intelligence_Integration_Specification.md)
@dataclass
class StoryBeat:
    beat_id: str
    beat_index: int
    character: Player
    raw_text: str
    dialogue: str
    action: str
    internal: str
    emotional_tone: str
    theme_resonance: str
    ncp_metadata: Dict[str, Any]
    timestamp: str

# My unified_state_bridge.py definition
@dataclass
class StoryBeat:
    beat_id: str
    beat_type: str
    content: str
    timestamp: str
    universe_analysis: Optional[ThreeUniverseAnalysis]  # ← New!
    ncp_metadata: dict
    enrichments: List[str]
    source_event: Optional[str]
```

**Recommendation**: Extend your StoryBeat to include `universe_analysis: Optional[ThreeUniverseAnalysis]` for three-universe enrichment.

### 2. Character State Alignment

```python
# Your CharacterArcState
@dataclass
class CharacterArcState:
    player: Player
    arc_points: List[ArcPoint]
    current_emotional_state: str
    # ... etc

# My CharacterState
@dataclass
class CharacterState:
    character_id: str
    name: str
    archetype: str  # "mia" | "ava8" | "miette" | custom
    arc_position: float  # 0.0 to 1.0
    emotional_state: str
    active_throughlines: List[str]
    relationship_map: dict
```

**Recommendation**: Add `archetype` field to support three-universe character mapping (Mia=Engineer, Ava8=Ceremony, Miette=StoryEngine).

### 3. Event Emission Alignment

Your `Logging_And_Traceability_Specification.md` should emit these event types from my langchain rispec:

| Event Type                   | When to Emit             | From Your Component    |
| ---------------------------- | ------------------------ | ---------------------- |
| `THREE_UNIVERSE_ANALYSIS`    | After beat analysis      | AnalyticalFeedbackLoop |
| `EMOTIONAL_QUALITY_ASSESSED` | After emotional scoring  | EmotionalBeatEnricher  |
| `CHARACTER_ARC_UPDATED`      | After arc point recorded | CharacterArcTracker    |
| `BEAT_ENRICHED`              | After enrichment applied | EmotionalBeatEnricher  |
| `GAP_IDENTIFIED`             | When gap found           | AnalyticalFeedbackLoop |
| `GAP_REMEDIATED`             | After gap fixed          | AnalyticalFeedbackLoop |

### 4. IAIP ↔ Ceremony World Mapping

Your IAIP Five-Phase maps to my Ceremony World:

| IAIP Phase                       | Ceremony World Concept                     |
| -------------------------------- | ------------------------------------------ |
| miigwechiwendam (Sacred Space)   | K'é - Kinship establishment                |
| nindokendaan (Two-Eyed Research) | Three-Universe simultaneous interpretation |
| ningwaab (Knowledge Integration) | Hózhó coherence scoring                    |
| nindoodam (Creative Expression)  | Story Engine lead universe                 |
| migwech (Ceremonial Closing)     | Sacred Pause protocol                      |

---

## 🎯 Suggested Next Steps

### For You (Storytelling Instance)

1. **Update StoryBeat schema** to include `universe_analysis` field
2. **Add archetype to CharacterArcState** for three-universe character mapping
3. **Reference my event types** in your Logging spec when planning Langfuse integration
4. **Cross-reference** your IAIP spec with my universal-router rispec for ceremony alignment

### For Me (NarIntel Instance)

1. **Reference your consumer patterns** in my rispec examples
2. **Add "Storytelling Package Integration"** section to narrative-intelligence.langgraph.rispec.md
3. **Update README.md** to show storytelling as downstream consumer

---

## 📁 File Cross-References

**Your files that should reference mine:**
- `Narrative_Intelligence_Integration_Specification.md` → Import types from `narrative-intelligence` package
- `Logging_And_Traceability_Specification.md` → Follow event taxonomy from `narrative-tracing.langchain.rispec.md`
- `IAIP_Integration_Specification.md` → Align with Ceremony World patterns

**My files that reference your patterns:**
- `narrative-intelligence.langgraph.rispec.md` - StoryBeat generation consumer
- `narrative-tracing.langchain.rispec.md` - Enrichment event emitters

---

## 🔄 Synchronization Protocol

When updating rispecs:

1. **Type changes** in unified_state_bridge.py → Update both narintel AND storytelling rispecs
2. **New event types** → Add to langchain rispec first, then reference in storytelling logging spec
3. **Three-universe patterns** → Ensure IAIP alignment with Ceremony World

---

*Coordination established between `/workspace/repos/narintel/rispecs/` and `/src/storytelling/rispecs/`*
