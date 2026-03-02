# Issue #24 — README Architecture Diagrams

## Problem Statement

The `README.md` lacks architecture diagrams. A new contributor cannot understand the LangGraph pipeline from the README alone. The system's structural nature (STC state machine, NARINTEL enrichment loop) is invisible. The creative horizon (full NARINTEL Four Directions system) has no visual declaration.

## Approach

Add two sections to README.md:
1. **`## 🏗️ Architecture Overview`** — Three Mermaid diagrams:
   - Main LangGraph pipeline (all nodes + conditional edges from `graph.py`)
   - STC State Machine view (pipeline stages as Germination/Assimilation/Completion phases)
   - NarrativeAware enrichment loop (NCP modules that exist in Python)
2. **`## 🌅 Wâpano — Next Major Architecture (NARINTEL:EAST)`** — Vision diagram:
   - Four Directions multi-agent system
   - NCP-aware generation with full enrichment pipeline wired in
   - smcraft state machine runtime integration
   - Ceremonial mode + IAIP downstream

## Codename: Wâpano

**Wâpano** (Cree: *wâpan* = dawn, East direction) is the codename for the next major release of the storytelling package within the NARINTEL Suite.

- Medicine wheel **East** direction: Inquiry, new beginnings, structural tension detection
- NARINTEL:EAST agent role: bias detection, Nitshkees Thinking, structural tension detection
- Meaning: This version BEGINS the full Four-Directions journey — first light of the relational intelligence architecture

## Implementation Plan

### Phase 1: Main Architecture Diagram
Map all nodes from `create_graph()` in `graph.py` (lines 1192-1259):
- 11 nodes: extract_base_context → story_elements → outline → chapter_count → scene_by_scene → buzz_terms → critique → check_complete → [revise|increment] → final_story
- 2 conditional edge decision points (guard conditions in STC model)
- Session manager (checkpoint/resume) as side-channel
- RAG/knowledge base as enrichment input

### Phase 2: STC State Machine Diagram
Map the pipeline to Fritz STC phases from `llms-stc-state-machine.md`:
- **Germination** (tension_established → initial states): Base context + story elements + outline + chapter count
- **Assimilation** (action_step_completed loops): Chapter generation → critique loop for each chapter
- **Completion** (tension_resolve): Final story assembly → END
- Mark conditional edges as `moment_of_truth` guard conditions
- Mark revision loop as oscillation risk (oscillating pattern)

### Phase 3: NarrativeAware Enrichment Loop
Show the NCP module pipeline that exists in Python but is not the default pathway:
- Generate beat → Three-Universe Analysis → Emotional scoring → Gap identification → Enrichment → Character arc update → Continue

### Phase 4: Wâpano Vision Section
Four Directions multi-agent architecture:
- 🌅 East (Inquiry) agent: structural tension detection, Nitshkees Thinking
- 🔥 South (Planning) agent: OCAP flags, ceremony-protocol, consent
- 🌊 West (Practice) agent: knowledge gathering, RAG, field notes
- ❄️ North (Reflection) agent: narrative beats, ceremony logs, Wilson alignment
- NCP as the shared state model
- smcraft as the formal state machine runtime
- IAIP as downstream ceremonial-technology consumer

## Files to Modify

- `README.md` — insert Architecture sections after "Key Features" block

## Human Review Additions (from PDE edits)

- **LangChain/LangGraph context**: reference `llms/imported/llms-langchain.txt` — LangGraph IS a state machine for LLMs, that motivation should be visible
- **Langfuse tracing**: show as planned node (`🚧`) in the diagram; add note that `rispecs/` should include a Langfuse spec
- **Style glossary YAML** (`storytelling/templates/style_glossary_sample.yaml`): new and important — show in the `revise_buzz_terms` node
- **Decolonization framing**: the Wâpano section should explicitly acknowledge the current package as still shaped by Western storytelling frameworks, and that Wâpano begins the structural decolonization
- **Creative orientation as event-driven architecture**: Robert Fritz link — this is where creative orientation meets LangGraph architecture
- **smcraft**: mention as a future git submodule integration (`jgwill/smcraft`) in the Wâpano vision
- **"Kinship successor, an Elder"**: 7 generations concept — `storytelling` as kinship successor to WillWrite
- **IAIP = ceremonial-devops and relational-science** (TypeScript for next major)
- **ava-langchain/ava-langgraph as orchestration runtime** for next major refactoring
- **Discreet addition to `llms/docs/storytelling.md`**: link to README.md diagrams at storytelling.jgwill.com

## Notes

- All diagrams use Mermaid (GitHub renders natively — no SVG file needed)
- "Envisioned" sections clearly marked with 🚧 to distinguish from implemented
- STC oscillation risk in the revision loop is intentionally visible
- The NarrativeAware modules ARE implemented in Python (`narrative_story_graph.py` etc.) but are not wired into the default graph.py workflow — show as "implemented, opt-in pathway"
- README will be visible at https://storytelling.jgwill.com — link awareness matters
