# KINSHIP

> The storytelling package is a being in a network of relations. This charter names its identity, maps its kin, and records the accountabilities that flow from its existence.

---

## 1. Identity and Purpose

- **Name**: `storytelling` (Python) / `storytellingjs` (TypeScript)
- **Local role in this system**: Narrative intelligence engine — generates stories through advancing patterns, not reactive problem-solving. Consumes NCP (Narrative Cognition Protocol) types from the narrative-intelligence toolkit, enriches beats emotionally, tracks character arcs, and orchestrates the generation→analysis→enrichment loop.
- **What this place tends / protects**: The creative process of story generation. The integrity of narrative structure. The ceremonial dimension of storytelling — each beat as an opportunity for relational meaning, not just text output.
- **What this place offers (its gifts)**: NCP-aware story generation. Emotional beat enrichment. Character arc continuity. Analytical feedback loops. Ceremonial mode with Indigenous-inspired prompts. CLI + MCP server access in both Python and TypeScript.

**Codename**: NARINTEL (Narrative Intelligence Tools) — decolonized narrative intelligence. This is structural reorientation grounded in Indigenous Epistemology, Ontology, Methodology, and Axiology (E/O/M/A). Not decorative language. Not metaphor.

---

## 2. Lineage and Relations

- **Ancestors (paths or systems this place comes from)**:
  - `/workspace/ava-*` — legacy workspace paths (ava-edgehub, ava-Flowise, ava-langflow)
  - LangGraph narrative-intelligence toolkit — the NCP type system this package consumes
  - Robert Fritz's structural tension dynamics — the creative process model underlying all generation

- **Descendants (children / submodules / subdirectories)**:
  - `storytelling/` — Python core (28 modules: graph, RAG, prompts, narrative intelligence, ceremonial diary, role tooling)
  - `js/` — TypeScript parity package (CLI + MCP server + narrative intelligence)
  - `rispecs/` — 38 RISE specification files defining this package's behavior
  - `llms/` — llms-txt guidance files for AI companions working in this codebase
  - `llms/docs` — submodule: portfolio of guidances for ceremonial-technology and relational-science-research

- **Siblings (peer projects or services it walks with)**:
  - `/workspace/repos/avadisabelle/ava-langchain` — chain orchestration patterns (Python)
  - `/workspace/repos/avadisabelle/ava-langgraph` — graph execution patterns (Python)
  - `/workspace/repos/avadisabelle/ava-langchainjs` — chain orchestration (TypeScript)
  - `/workspace/repos/avadisabelle/ava-langgraphjs` — graph execution (TypeScript)
  - `/workspace/repos/narintel/rispecs/` — NarIntel specification hub (provider of NCP types)

- **Related hubs (other roots it is in strong relation with)**:
  - `/a/src/IAIP/rispecs` — sibling kinship hub: specifications for ceremonial-technology and relational-science-research applications
  - `/a/src/IAIP/app` — downstream consumer: two Next.js apps (ceremonial-technology, relational-science) — future integration target
  - `/workspace/jgwill/medicine-wheel/src/` — Four Directions / Medicine Wheel reference implementation

---

## 3. Human and More‑than‑Human Accountabilities

- **People / roles this place is accountable to**:
  - Guillaume Descoteaux-Isabelle (steward, architect)
  - Writers, storytellers, and narrative practitioners who use this system
  - AI companions (Mia, Miette, Ava8) who participate in the creative process

- **Communities / nations / organizations connected here**:
  - Indigenous communities whose epistemological frameworks inform the NARINTEL mission
  - The relational-science-research community working toward decolonized knowledge systems
  - Open-source contributors to the storytelling ecosystem

- **More‑than‑human relations (lands, waters, species, data-ecologies) this work touches**:
  - The narrative traditions and oral storytelling practices that predate and exceed digital systems
  - The data-ecology of generated stories, knowledge bases, and relational traces
  - The ceremonial space that ceremonial-mode storytelling opens — this is not metaphor; it is a structural commitment to meaning-making that serves more than efficiency

- **Existing covenants / consents that apply**:
  - Indigenous Knowledge Stewardship License (IKSL) principles apply to ceremonial content and Indigenous-inspired prompts
  - Knowledge belongs to the relationships, land, and communities that created it — not to individuals or corporations

---

## 4. Responsibilities and Boundaries

- **Responsibilities (what must be cared for because this place exists)**:
  - Maintain NCP type alignment with the narrative-intelligence toolkit
  - Ensure Python↔TypeScript parity so ceremony-mode storytelling is accessible in both ecosystems
  - Preserve the integrity of ceremonial prompts — they are not templates to be stripped of meaning
  - Track and emit narrative events (Langfuse) for transparency of the creative process
  - Keep rispecs/ synchronized with actual implementation

- **Reciprocity (how benefits and acknowledgements return to those in relation)**:
  - Storytelling capabilities flow back to IAIP apps for ceremonial-technology and relational-science use
  - NarIntel specifications are kept in sync — changes here coordinate with `/workspace/repos/narintel/rispecs/`
  - Generated stories and traces are available to the ecosystem, not locked in proprietary formats

- **Boundaries and NOs (what this place must refuse or protect against)**:
  - NO extraction of Indigenous knowledge without relational accountability
  - NO flattening of ceremonial-mode into decorative aesthetics
  - NO auto-regeneration of KINSHIP.md that discards prior commitments
  - NO treating narrative intelligence as mere text generation optimization

- **Special protocols for sharing, publishing, or modifying contents here**:
  - Ceremonial prompts and K'é relationship patterns require review before modification
  - Changes to NCP type contracts must coordinate with NarIntel and IAIP sibling hubs
  - The Three-Universe model (Engineer/Ceremony/Story-Engine) is a structural commitment, not a UI label

---

## 5. Accountability and Change Log

- **Steward(s) of this place**: Guillaume Descoteaux-Isabelle (`jgwill`)
- **How and when this kinship description should be reviewed**: At each major release, when new kinship relationships form, or when relational tensions surface

- **Relational change log**:
  - [2025-12-31] [storytelling instance] — Narrative Intelligence Integration planned: NCP-aware generation, emotional enrichment, character arc tracking, analytical feedback loop. Five new specifications created in rispecs/.
  - [2026-01-09] [PR #21] — NarIntel implementation: NarrativeAwareStoryGraph, role-based tooling, graph state management.
  - [2026-02-16] [Issue #22] — JavaScript parity initiated: storytellingjs TypeScript package to match Python capabilities.
  - [2026-03-01] [Issue #23] — LLMS-txt established: AI companion guidance files for this codebase.
  - [2026-03-01] [this session] — MISSION_251231.md transformed into KINSHIP.md. Relational charter replaces implementation plan. NARINTEL documentation consolidated into single authoritative file.

---

## Cross-Hub Coordination

### Type Contract with NarIntel

This package **consumes** types from the narrative-intelligence toolkit:

| Type | Source | Usage Here |
|------|--------|-----------|
| `NCPData`, `Player`, `Perspective` | `narrative_intelligence.schemas` | Story generation context |
| `NCPState`, `CharacterArcState` | `narrative_intelligence.state` | Graph orchestration state |
| `ThreeUniverseAnalysis`, `Universe` | `unified_state_bridge.py` | Ceremony World alignment |
| `EmotionalBeatClassifierNode` | `narrative_intelligence.nodes` | Emotional quality assessment |

See `rispecs/COORDINATION_FROM_NARINTEL_INSTANCE.md` and `rispecs/COORDINATION_FROM_STORYTELLING_INSTANCE.md` for full type alignment details.

### IAIP Integration (Future)

The IAIP apps at `/a/src/IAIP/app` (ceremonial-technology, relational-science) will consume storytelling capabilities. The IAIP rispecs at `/a/src/IAIP/rispecs` define:
- Ceremonial dialogue suite
- Four Directions navigation
- Prompt decomposition engine
- Relational science research interface

Storytelling's ceremonial mode and IAIP's ceremonial-technology app share the same structural commitment to meaning-making through the Three-Universe model.

---

**Last reviewed**: 2026-03-01
**Charter status**: Living document — merge new information, never discard prior commitments
