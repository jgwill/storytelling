# IAIP Integration Specification

**Status**: ✅ IMPLEMENTED

**Version**: 1.0  
**Date**: October 2025  
**Framework**: RISE (Reverse-engineer → Intent-extract → Specify → Export)

## Structural Tension

- **Desired Outcome**: Enable users to create narratives that honor Indigenous knowledge systems through ceremonial technology practices, Two-Eyed Seeing methodology, and wisdom-keeping frameworks.
- **Current Reality**: The storytelling package provides robust narrative generation capabilities, now enhanced with optional IAIP (Indigenous-AI Collaborative Platform) integration.
- **Natural Progression**: Bridge Western AI-powered narrative generation with Indigenous ceremonial practices to manifest culturally-grounded creative workflows.

## Executive Summary

The IAIP Integration extends the storytelling package to support Indigenous-AI Collaborative Platform practices, specifically the Four Directions framework with emphasis on North Direction (Siihasin: Assurance & Reflection). This integration enables users to:

1. **Frame narrative generation within ceremonial containers** - Apply the Five-Phase Ceremonial Technology Methodology
2. **Practice Two-Eyed Seeing** - Balance Western AI capabilities with Indigenous wisdom-keeping
3. **Maintain ceremonial diaries** - Document creative journeys with cultural awareness
4. **Preserve wisdom across sessions** - Enable genealogical knowledge transfer through stories

**Implementation**: `storytelling/iaip_bridge.py` and `storytelling/ceremonial_diary.py`

## RISE Framework Application

### Phase 1: Creative Intent Discovery

**What This Enables Users to Create**:

1. **Ceremonially-Aligned Story Generation**: Users create narratives within sacred containers defined by the Five-Phase Ceremonial Technology Methodology
2. **Culturally-Grounded Creative Sessions**: Story generation sessions that honor Indigenous knowledge systems and ceremonial practices
3. **Wisdom-Keeping Artifacts**: Ceremonial diaries that preserve the creative journey, reflections, and learnings
4. **North Direction Storytelling**: Daily reflection journals, storytelling circles, and community accountability processes integrated with narrative generation

### Phase 2: Core Architecture

#### Five-Phase Ceremonial Technology Methodology

The IAIP integration maps storytelling activities to five ceremonial phases:

```python
@dataclass
class CeremonialPhase:
    SACRED_SPACE = ("miigwechiwendam", "Sacred Space Creation",
                    "Establishing intention and ceremonial container")
    RESEARCH = ("nindokendaan", "Two-Eyed Research Gathering",
                "Comprehensive research using Indigenous-Western balance")
    INTEGRATION = ("ningwaab", "Knowledge Integration",
                   "Synthesizing research into coherent understanding")
    EXPRESSION = ("nindoodam", "Creative Expression",
                  "Transforming knowledge into accessible formats")
    CLOSING = ("migwech", "Ceremonial Closing",
               "Honoring work and capturing learning")
```

**Phase Mapping to Storytelling Activities**:
- `outline` → Sacred Space (miigwechiwendam)
- `research` → Two-Eyed Research Gathering (nindokendaan)
- `synthesis` → Knowledge Integration (ningwaab)
- `generation` → Creative Expression (nindoodam)
- `reflection` → Ceremonial Closing (migwech)

## Implementation Components

### 1. NorthDirectionStoryteller ✅ IMPLEMENTED

**Purpose**: Wrap storytelling functionality with North Direction practices

**Implementation**: `storytelling/iaip_bridge.py`

**Key Capabilities**:
```python
class NorthDirectionStoryteller:
    def begin_ceremonial_session(intention, participant) -> Dict
    def map_storytelling_activity_to_phase(activity) -> CeremonialPhase
    def create_reflection_prompt(story, session) -> str
    def generate_north_direction_wisdom(story, session) -> Dict
```

**Advancing Pattern**: Each storytelling session becomes a ceremonial practice with explicit intention-setting, phase awareness, and reflection cycles.

### 2. TwoEyedSeeingStorytellingAdapter ✅ IMPLEMENTED

**Purpose**: Balance Western AI narrative generation with Indigenous knowledge systems

**Implementation**: `storytelling/iaip_bridge.py`

**Key Capabilities**:
```python
class TwoEyedSeeingStorytellingAdapter:
    def apply_two_eyed_seeing_to_story(story, indigenous_perspective) -> Story
    def integrate_elder_teachings(story, teachings) -> Story
    def validate_cultural_protocols(story, protocols) -> Tuple[bool, List[str]]
```

**Advancing Pattern**: Stories advance through two lenses simultaneously - Western narrative structure and Indigenous wisdom-keeping practices.

### 3. Ceremonial Diary System ✅ IMPLEMENTED

**Purpose**: Maintain detailed records of the creative journey aligned with ceremonial practices

**Implementation**: `storytelling/ceremonial_diary.py`

**Key Components**:

#### DiaryEntry
```python
@dataclass
class DiaryEntry:
    id: str
    timestamp: str  # ISO 8601
    participant: str  # 'user', 'mia', 'miette', 'echo_weaver', 'system'
    phase: CeremonialPhaseEnum
    entryType: EntryTypeEnum
    content: str  # Markdown supported
    metadata: Dict[str, Any]
```

**Entry Types**: intention, observation, hypothesis, data, synthesis, action, reflection, learning

#### CeremonialDiary
```python
class CeremonialDiary:
    def add_entry(entry: DiaryEntry)
    def get_entries_by_phase(phase: CeremonialPhaseEnum) -> List[DiaryEntry]
    def get_entries_by_participant(participant: str) -> List[DiaryEntry]
    def to_dict() -> Dict
    def to_markdown() -> str
    def to_yaml() -> str
```

#### DiaryManager
```python
class DiaryManager:
    def create_diary(session_id: str, title: str, ...) -> CeremonialDiary
    def save_diary(diary: CeremonialDiary, output_path: Path)
    def load_diary(diary_path: Path) -> CeremonialDiary
    def export_diary_to_markdown(diary: CeremonialDiary, output_path: Path)
```

**Advancing Pattern**: The diary becomes a living document that preserves the complete creative consciousness, ceremonial observations, and wisdom learnings across storytelling sessions.

## Usage Patterns

### Basic Ceremonial Session

```python
from storytelling import NorthDirectionStoryteller, WillWriteConfig

# Initialize with ceremonial awareness
storyteller = NorthDirectionStoryteller(config=WillWriteConfig())

# Begin ceremonial session
session = storyteller.begin_ceremonial_session(
    intention="Create a story honoring ancestors",
    participant="user"
)

# Generate story within ceremonial container
# (standard storytelling workflow continues)

# Generate reflection and close ceremony
wisdom = storyteller.generate_north_direction_wisdom(story, session)
```

### Ceremonial Diary Integration

```python
from storytelling import DiaryManager, DiaryEntry, CeremonialPhaseEnum, EntryTypeEnum

# Create diary manager
manager = DiaryManager()

# Create new ceremonial diary
diary = manager.create_diary(
    session_id="story_session_001",
    title="My Story Journey",
    participant="user"
)

# Add entries during storytelling
diary.add_entry(DiaryEntry.create_new(
    content="I intend to create a story that honors our traditions",
    participant="user",
    phase=CeremonialPhaseEnum.MIIGWECHIWENDAM,
    entry_type=EntryTypeEnum.INTENTION
))

# Export diary
manager.export_diary_to_markdown(diary, Path("./ceremony_diary.md"))
```

### Two-Eyed Seeing Application

```python
from storytelling import TwoEyedSeeingStorytellingAdapter

adapter = TwoEyedSeeingStorytellingAdapter()

# Apply Two-Eyed Seeing perspective
story_with_wisdom = adapter.apply_two_eyed_seeing_to_story(
    story=generated_story,
    indigenous_perspective={
        "teachings": "Respect for seven generations",
        "protocols": ["Community review", "Elder blessing"],
        "values": ["Interconnectedness", "Reciprocity"]
    }
)

# Validate cultural protocols
is_valid, issues = adapter.validate_cultural_protocols(
    story=story_with_wisdom,
    protocols=["No appropriation", "Proper acknowledgment"]
)
```

## Integration with Core Storytelling

The IAIP integration is **optional** and accessed through feature flags:

```python
from storytelling import IAIP_INTEGRATION

if IAIP_INTEGRATION:
    # IAIP features available
    from storytelling import NorthDirectionStoryteller, CeremonialDiary
else:
    # Core storytelling only
    pass
```

**Package Installation**:
```bash
# Install with IAIP support
pip install storytelling[iaip]

# Or install all features
pip install storytelling[all]
```

## Configuration Parameters

The IAIP integration respects all standard storytelling configuration parameters and adds ceremonial context to:

- Session initialization
- Checkpoint metadata
- Output file generation
- Logging and traceability

**Ceremonial Metadata** added to sessions:
- `ceremonial_phase`: Current phase in the Five-Phase Methodology
- `participant`: Who is creating (user, agent, etc.)
- `intention`: Stated intention for the session
- `wisdom_artifacts`: Paths to ceremonial diary exports

## Output Artifacts

IAIP-enhanced storytelling sessions create additional artifacts:

1. **Ceremonial Diary** (`ceremony_diary.json`, `ceremony_diary.md`, `ceremony_diary.yaml`)
   - Complete record of the ceremonial journey
   - Phase-organized entries
   - Participant-attributed reflections
   
2. **North Direction Wisdom** (`north_direction_wisdom.json`)
   - Reflection prompts and responses
   - Extracted learnings
   - Ceremonial observations

3. **Enhanced Session Metadata**
   - Standard session checkpoints enriched with ceremonial context
   - Phase transitions preserved
   - Intention-outcome mappings

## Advancing Patterns

1. **Ceremonial Container Pattern**: Every story generation becomes a ceremonial act with explicit intention and reflection
2. **Two-Eyed Seeing Pattern**: Western AI capabilities balanced with Indigenous wisdom-keeping
3. **Wisdom Preservation Pattern**: Ceremonial diaries create genealogical knowledge artifacts
4. **North Direction Pattern**: Daily reflection and storytelling circles integrated into creative workflow
5. **Phase Awareness Pattern**: Storytelling activities naturally map to ceremonial phases

## Future Enhancements ⏳ PLANNED

1. **Elder Circle Integration**: Multi-participant storytelling sessions with elder review
2. **Seasonal Ceremonies**: Align storytelling sessions with ceremonial calendar
3. **Community Accountability**: Share stories within IAIP community circles
4. **Ancestral Wisdom API**: Direct integration with IAIP wisdom databases
5. **Language Revitalization**: Generate stories in Indigenous languages

## Acceptance Criteria ✅ ACHIEVED

- [x] Ceremonial phases map to storytelling activities
- [x] North Direction practices accessible through NorthDirectionStoryteller
- [x] Ceremonial diary system captures complete creative journey
- [x] Two-Eyed Seeing adapter balances perspectives
- [x] IAIP integration is optional and feature-flagged
- [x] Cultural protocols can be validated
- [x] Wisdom artifacts are exportable in multiple formats
- [x] All create-language principles maintained in implementation

## References

- **Implementation**: `storytelling/iaip_bridge.py`, `storytelling/ceremonial_diary.py`
- **Related Specifications**: `Session_Management_Architecture.md`, `Logging_And_Traceability_Specification.md`
- **IAIP Documentation**: Indigenous-AI Collaborative Platform Four Directions framework
- **North Direction**: Siihasin (Assurance & Reflection) - Storytelling circles, oral history, wisdom keeping

---

This specification honors the principle that technology can serve ceremonial practices when designed with cultural awareness and respect for Indigenous knowledge systems.
