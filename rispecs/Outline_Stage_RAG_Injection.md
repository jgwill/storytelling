# Outline-Stage RAG Injection — Criteria & Boundaries

**Status**: ⚠️ DEPRECATED - See `Outline_Level_RAG_Integration_SpecificationV1.md` and `Outline_Level_RAG_Integration_SpecificationV3.md` for complete specifications.

> **Note**: This document's content has been incorporated into the comprehensive Outline-Level RAG specifications. The basic functionality described here is implemented in V1, and advanced features are detailed in V3.

## Structural Tension
- Desired Outcome: Foundational outlines naturally reflect relevant knowledge from the KB without overpowering user vision.
- Current Reality: Outline-stage retrieval behavior is not formalized.
- Natural Progression: Define retrieval criteria, boundaries, and injection points.

## Observations
- RAG is effective during scene/chapter generation; outline-stage rules are implicit.

## Structural Assessment
- Tendency to oscillate until outline-stage criteria and limits are explicit.

## Advancing Moves
- Injection Points: (1) BaseContext extraction; (2) Initial Outline generation; (3) Critique/Revision rounds (context-aware).
- Retrieval Criteria: top_k=5 (preset), semantic filter by entities (characters, locations), and theme keywords from prompt.
- Boundaries: Max context tokens for outline stage capped (e.g., 1k tokens); retrieval confined to high-signal docs (rules, canon, style guides).
- Formatting: Inject retrieved snippets as a dedicated context block separate from prompts; label as `RAG-Outline-Context`.
- Acceptance Criteria (DoD):
  - Outline references KB consistently (terms, rules) without displacing prompt intent.
  - Critique references RAG-Outline-Context explicitly when suggesting advancement.
  - Logs show retrieval stats for outline-stage steps.
