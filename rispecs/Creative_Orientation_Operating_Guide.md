# Creative Orientation Operating Guide

**Status**: ✅ IMPLEMENTED

**Purpose**: Operationalize Creative Orientation within WillWrite by defining short, enforceable rules and templates that align with the RISE framework without reframing observations as problems.

---

## Operating Rules
- Structural Tension block appears at the top of major docs and agent outputs.
- Observations are recorded neutrally (including Risks & Issues) without categorization.
- Structural Assessment states whether a structure tends to advance or oscillate.
- Advancing Moves (optional) propose the next natural step that advances tension toward the desired outcome.
- Use create-language (create, manifest, build, enable, stabilize); avoid problem-elimination phrasing (fix, mitigate, eliminate).
- When helpful, tag phase: germination, assimilation, completion.

### Structural Tension Block
```
- Desired Outcome: <one sentence>
- Current Reality: <one sentence>
- Natural Progression: <one sentence>
```

### Section Structure
1) Observations (neutral facts)  
2) Structural Assessment (advance or oscillate)  
3) Advancing Moves (optional)

### Acceptance Checklist (DoD)
- Structural Tension block present.  
- Observations stated neutrally.  
- Structural Assessment uses “advancing/oscillating” language.  
- Language patterns adhere to create-language rules.  
- If Advancing Moves are provided, they describe natural progression, not elimination.

### Doc-Lint Policy
- Allow neutral Observations; flag problem-elimination verbs outside of technical contexts.  
- Require “advancing/oscillating” only in Structural Assessment.  
- Require Structural Tension block in governed docs.

---

## Agent Application Matrix
- vision-agent: produces the Structural Tension block first.  
- architect-agent: outlines reflect advancing patterns; Observations kept separate.  
- writer-agent: prompts and staging described in create-language.  
- critic-agent: findings recorded as Observations; assessment states advance/oscillate; suggestions become Advancing Moves.  
- revisor-agent: enforces Acceptance Checklist before completion.  
- rag-agent: retrieval intent framed as context that advances the Desired Outcome.  
- editor/meta agents: preserve advancing pattern language in polish and metadata.

---

## Examples
- Reactive: “Fix chapter over-generation in tests.”  
  Creative: “Create a 3‑chapter test preset that stabilizes chapter count during test runs.”
- Reactive: “Eliminate outline inconsistency.”  
  Creative: “Enable outline-stage RAG injection to stabilize foundational consistency.”

---

This guide governs specs in `specifications/` and agent outputs in `agents/`. It complements `LLMS/llms-rise-framework.txt` and `specifications/RISE_Spec.md` by making Creative Orientation operational and testable.