# Plan: KINSHIP Hub + NARINTEL Upgrade + JS Parity

**Issues**: #21 (NarIntel PR), #22 (JS Parity), #23 (LLMS-txt)
**Branch**: `20-narintel`
**Session**: 2603011406

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
   - Related hubs: `llms/docs` submodule (portfolio), IAIP apps (ceremonial-tech, relational-science)
3. **Human and More-than-Human Accountabilities** — Communities, relational science, ceremony
4. **Responsibilities and Boundaries** — What storytelling must tend, reciprocity, NOs
5. **Accountability and Change Log** — Stewards, review rhythm

### A3. Commit KINSHIP.md

---

## Phase B: NARINTEL Documentation Upgrade

### B1. Consolidate NARINTEL_OVERVIEW.txt into NARINTEL_README.md
The .txt is a structural summary; merge valuable content into README.

### B2. Upgrade NARINTEL_README.md
Substantive quality improvement — kinship-aligned framing, ceremonial-technology grounding, accurate ecosystem description. Replace shallow marketing language with structural precision.

### B3. Upgrade NARINTEL_USER_SCENARIOS.md
Deepen ceremonial-technology alignment. Add scenarios that reflect Indigenous epistemological foundations — not just Western writer personas.

### B4. Clean up redundant files
- Remove NARINTEL_OVERVIEW.txt (consolidated)
- Remove NARINTEL_FILES_SUMMARY.txt (redundant)
- Keep NARINTEL_QUICK_START.md if it serves as distinct entry point

### B5. Commit documentation upgrades

---

## Phase C: JavaScript/TypeScript Parity (Issue #22)

### C1. Analyze Python modules for port scope
Many Python modules may be stubs vs. real implementations. Port what's real.

### C2. Create foundation modules
- `js/src/data-models.ts` — Full NCP type system
- `js/src/prompts.ts` — Kinship-aware narrative prompts

### C3. Create narrative intelligence modules
- `js/src/graph.ts` — Story generation graph execution
- `js/src/rag.ts` — RAG integration
- `js/src/narrative-intelligence-integration.ts` — NCP-aware generator
- `js/src/character-arc-tracker.ts` — Persistent character state
- `js/src/emotional-beat-enricher.ts` — Emotional quality
- `js/src/analytical-feedback-loop.ts` — Gap identification
- `js/src/narrative-tracing.ts` — Langfuse integration
- `js/src/ceremonial-diary.ts` — Ceremonial mode
- `js/src/role-tooling.ts` — Role-based tooling

### C4. Update index.ts, package.json, MCP server

### C5. Build and test

### C6. Commit JS parity

---

## Phase D: LLMS-txt Update (Issue #23)

### D1. Update llms.txt and llms-full.txt to reflect new capabilities

---

## Ambiguities Requiring Human Review

1. Should NARINTEL_QUICK_START.md be merged or kept?
2. Depth of LangGraph JS integration — direct dependency or lightweight abstraction?
3. Scope of ceremonial mode in TypeScript — full COAIA fusion or ceremony-aware prompts?
4. KINSHIP.md — should code examples from MISSION be preserved as spec references?
