# Plan: KINSHIP Hub + NARINTEL Consolidation + JS Parity

**Issues**: #21 (NarIntel PR), #22 (JS Parity), #23 (LLMS-txt)
**Branch**: `20-narintel`
**Session**: 2603011406
**Revised**: Post human review — ambiguities resolved

---

## Phase A: KINSHIP Hub Establishment

### A1. git mv MISSION_251231.md → KINSHIP.md
Preserve git history. The MISSION file contains 697 lines of narrative intelligence integration planning — seed material for transformation into a Kinship Hub charter.

### A2. Rewrite KINSHIP.md to Kinship Hub Schema
Following `llms/llms-kinship-hub-system.md` protocol:

1. **Identity and Purpose** — Storytelling as the narrative intelligence engine; NARINTEL codename for decolonized narrative intelligence (Indigenous E/O/M/A compatible)
2. **Lineage and Relations**
   - Ancestors: `/workspace/ava-*` (legacy paths)
   - Siblings: `/workspace/repos/avadisabelle/ava-lang{chain,graph,chainjs,graphjs}`, `/a/src/IAIP/rispecs`
   - Descendants: `rispecs/` (38 specs), `js/` (TypeScript parity), `storytelling/` (Python core)
   - Related hubs: `llms/docs` submodule (portfolio), IAIP apps (ceremonial-tech, relational-science) — future integration target
3. **Human and More-than-Human Accountabilities** — Communities, relational science, ceremony
4. **Responsibilities and Boundaries** — What storytelling must tend, reciprocity, NOs
5. **Accountability and Change Log** — Stewards, review rhythm

### A3. Commit KINSHIP.md

---

## Phase B: NARINTEL Consolidation (Single File)

**Human decision**: ALL NARINTEL_* files consolidate into **one file**: NARINTEL_README.md.

### B1. Consolidate all NARINTEL content into NARINTEL_README.md
Merge valuable content from:
- NARINTEL_OVERVIEW.txt
- NARINTEL_QUICK_START.md
- NARINTEL_USER_SCENARIOS.md
- NARINTEL_FILES_SUMMARY.txt

### B2. Rewrite NARINTEL_README.md
Substantive quality improvement — kinship-aligned framing, ceremonial-technology grounding, accurate ecosystem description. Single authoritative file.

### B3. Remove all redundant NARINTEL files
- Delete NARINTEL_OVERVIEW.txt
- Delete NARINTEL_QUICK_START.md
- Delete NARINTEL_USER_SCENARIOS.md
- Delete NARINTEL_FILES_SUMMARY.txt

### B4. Commit NARINTEL consolidation

---

## Phase C: JavaScript/TypeScript Parity (Issue #22)

**Human decision**: Python storytelling/ modules are the only reference. Inspect `/workspace/repos/avadisabelle/ava-langchain` and `ava-langgraph` for patterns. Also `/workspace/jgwill/medicine-wheel/src/*` for Four Directions reference.

### C1. Inspect ava-langchain, ava-langgraph, medicine-wheel for patterns

### C2. Analyze Python modules for actual implementation vs. stubs

### C3. Create foundation modules
- `js/src/data-models.ts` — Full NCP type system
- `js/src/prompts.ts` — Kinship-aware narrative prompts

### C4. Create narrative intelligence modules
- `js/src/graph.ts` — Story generation graph execution
- `js/src/rag.ts` — RAG integration
- `js/src/narrative-intelligence-integration.ts` — NCP-aware generator
- `js/src/character-arc-tracker.ts` — Persistent character state
- `js/src/emotional-beat-enricher.ts` — Emotional quality
- `js/src/analytical-feedback-loop.ts` — Gap identification
- `js/src/narrative-tracing.ts` — Langfuse integration
- `js/src/ceremonial-diary.ts` — Ceremonial mode
- `js/src/role-tooling.ts` — Role-based tooling

### C5. Update index.ts, package.json, MCP server

### C6. Build and test

### C7. Commit JS parity

---

## Phase D: LLMS-txt Update (Issue #23)

### D1. Update llms.txt and llms-full.txt to reflect new capabilities

---

## Resolved Ambiguities (from human review)

- ✅ NARINTEL_QUICK_START.md → merge into NARINTEL_README.md, then delete
- ✅ Python modules are sole reference; inspect ava-langchain/ava-langgraph for patterns
- ✅ KINSHIP.md is a relational charter, not an implementation plan — transform code examples into spec references
