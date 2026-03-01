# Prompt Decomposition

## Directions

- 🌅 **EAST** — VISION: What is being asked?
- 🔥 **SOUTH** — ANALYSIS: What needs to be learned?
- 🌊 **WEST** — VALIDATION: What needs reflection?
- ❄️ **NORTH** — ACTION: What executes the cycle?

## Original Prompt

> JavaScript/TypeScript Parity Implementation & Ecosystem Integration (Issue #22 JS Parity, Issue #23 LLMS-txt)

## Primary Intent

**Action:** implement
**Target:** TypeScript parity of Python storytelling package with kinship-aligned narrative intelligence
**Urgency:** session
**Confidence:** 92%

## Secondary Intents

1. **create** — narrative intelligence types module (NCP types, StoryBeat, CharacterArcState, Gap, enrichment types) _(explicit)_
2. **create** — prompts module with kinship-aware narrative prompts ported from Python prompts.py _(explicit)_
   - depends on: narrative intelligence types
3. **create** — data-models.ts with full NCP data model parity (data_models.py equivalent) _(explicit)_
   - depends on: narrative intelligence types
4. **create** — graph.ts — story generation graph execution (LangGraph JS or equivalent pattern) _(explicit)_
   - depends on: prompts module, data-models.ts
5. **create** — rag.ts — RAG integration for knowledge base retrieval _(explicit)_
   - depends on: data-models.ts
6. **create** — narrative-intelligence-integration.ts — NCP-aware story generator _(explicit)_
   - depends on: graph.ts, data-models.ts
7. **create** — emotional-beat-enricher.ts — emotional quality assessment and enrichment _(explicit)_
   - depends on: narrative-intelligence-integration.ts
8. **create** — character-arc-tracker.ts — persistent character state tracking _(explicit)_
   - depends on: data-models.ts
9. **create** — analytical-feedback-loop.ts — gap identification and enrichment routing _(explicit)_
   - depends on: emotional-beat-enricher.ts, character-arc-tracker.ts
10. **create** — narrative-tracing.ts — Langfuse integration for observability _(explicit)_
   - depends on: narrative-intelligence-integration.ts
11. **create** — ceremonial-diary.ts — ceremonial mode and diary integration _(explicit)_
   - depends on: data-models.ts
12. **create** — role-tooling.ts — role-based tooling interface (Architect, Structurist, Storyteller, etc.) _(explicit)_
   - depends on: data-models.ts
13. **update** — MCP server to expose narrative intelligence capabilities _(explicit)_
   - depends on: narrative-intelligence-integration.ts
14. **update** — js/src/index.ts to export all new modules _(implicit)_
   - depends on: all new modules created
15. **update** — js/package.json with any new dependencies (langfuse, etc.) _(implicit)_
16. **verify** — TypeScript build succeeds and tests pass _(explicit)_
   - depends on: all modules created
17. **update** — llms.txt and llms-full.txt to reflect new JS capabilities (Issue #23) _(explicit)_
   - depends on: JS parity implementation

## Context Requirements

### Files Needed
- storytelling/core.py
- storytelling/graph.py
- storytelling/rag.py
- storytelling/enhanced_rag.py
- storytelling/prompts.py
- storytelling/narrative_intelligence_integration.py
- storytelling/emotional_beat_enricher.py
- storytelling/analytical_feedback_loop.py
- storytelling/narrative_story_graph.py
- storytelling/ceremonial_diary.py
- storytelling/coaia_fuse.py
- storytelling/iaip_bridge.py
- storytelling/role_tooling.py
- storytelling/narrative_tracing.py
- storytelling/data_models.py
- js/src/index.ts
- js/src/core.ts
- js/src/types.ts
- js/src/config.ts
- js/package.json
- js/tsconfig.json
- .env

### Tools Required
- TypeScript compiler (tsc)
- npm
- node
- file editor
- git

### Assumptions
- Python storytelling modules are the reference implementation for JS parity
- JS implementation should follow TypeScript idioms, not direct Python port
- LangGraph JS (ava-langgraphjs) is the intended graph framework for TypeScript
- .env file contains API keys for LLM providers needed for testing
- MCP server is a key distribution mechanism for the JS package
- ESM module format is required (type: module in package.json)
- Parity means equivalent capability, not line-by-line translation
- The implementation should reflect kinship vision — not just technical feature parity

## Four Directions Analysis

### 🌅 EAST — VISION

- Envision JS package as a first-class kinship-aware narrative intelligence engine — not just a Python port [92%]
- JS parity enables ceremony-mode storytelling in browser and Node.js contexts — expanding access [85%] _(implicit)_

### 🔥 SOUTH — ANALYSIS

- Analyze each Python module to extract essential patterns for TypeScript implementation [95%]
- Study ava-langgraphjs for graph execution patterns in TypeScript [82%] _(implicit)_
- Review .env for available API keys and provider capabilities [88%]

### 🌊 WEST — VALIDATION

- Build TypeScript and verify no compilation errors [95%]
- Test MCP server with new capabilities [88%]
- Verify LLM integration works with .env API keys [85%]

### ❄️ NORTH — ACTION

- Create narrative intelligence types and data models [95%]
- Create prompts module with kinship-aware prompts [90%]
- Create graph execution module [85%]
- Create RAG integration [82%]
- Create narrative intelligence integration module [88%]
- Create emotional beat enricher [85%]
- Create character arc tracker [85%]
- Create analytical feedback loop [82%]
- Create narrative tracing [85%]
- Create ceremonial diary module [80%]
- Create role tooling [85%]
- Update MCP server [88%]
- Update exports and package.json [95%] _(implicit)_

## Action Stack

- [ ] Analyze Python modules for essential patterns to port
- [ ] Review .env for API key availability
- [ ] Create js/src/data-models.ts with full NCP type system
- [ ] Update js/src/types.ts with comprehensive narrative intelligence types (depends on: data-models.ts)
- [ ] Create js/src/prompts.ts with kinship-aware narrative prompts (depends on: data-models.ts)
- [ ] Create js/src/graph.ts for story generation graph execution (depends on: prompts.ts, data-models.ts)
- [ ] Create js/src/rag.ts for knowledge base RAG integration (depends on: data-models.ts)
- [ ] Create js/src/narrative-intelligence-integration.ts (depends on: graph.ts)
- [ ] Create js/src/character-arc-tracker.ts (depends on: data-models.ts)
- [ ] Create js/src/emotional-beat-enricher.ts (depends on: narrative-intelligence-integration.ts)
- [ ] Create js/src/analytical-feedback-loop.ts (depends on: emotional-beat-enricher.ts, character-arc-tracker.ts)
- [ ] Create js/src/narrative-tracing.ts with Langfuse integration (depends on: narrative-intelligence-integration.ts)
- [ ] Create js/src/ceremonial-diary.ts (depends on: data-models.ts)
- [ ] Create js/src/role-tooling.ts (depends on: data-models.ts)
- [ ] Update js/src/index.ts with all new exports (depends on: all modules)
- [ ] Update js/package.json with new dependencies
- [ ] Update MCP server to expose new capabilities (depends on: narrative-intelligence-integration.ts)
- [ ] Build TypeScript and fix any errors (depends on: all modules)
- [ ] Test with .env API keys (depends on: build succeeds)
- [ ] Update llms.txt and llms-full.txt for Issue #23 (depends on: JS parity complete)
- [ ] Commit all changes with meaningful messages (depends on: tests pass)

## Ambiguity Flags

- **"Depth of LangGraph JS integration — should we use @langchain/langgraph directly or build a lighter graph abstraction?"**
  - Suggestion: Check ava-langgraphjs for existing patterns; if no dependency available, build a minimal graph runner
- **"Which Python modules have actual implementation vs. placeholder stubs?"**
  - Suggestion: Inspect each .py file to determine what's real code vs. scaffolding before porting
- **"Scope of 'ceremonial mode' in TypeScript context — does this mean full COAIA fusion or just ceremony-aware prompts?"**
  - Suggestion: Start with ceremony-aware prompts and ceremonial diary; full COAIA fusion is a later phase
- **"RAG implementation — does JS need its own vector store integration or does it call a Python service?"**
  - Suggestion: Implement basic RAG with configurable backend; can call Python service or use JS vector store
- **"How much of prompts.py (55KB) needs direct porting vs. being loaded as data?"**
  - Suggestion: Port the prompt templates as TypeScript constants; load Indigenous-specific prompts from knowledge_base/

## Expected Outputs

### Artifacts
- js/src/data-models.ts
- js/src/prompts.ts
- js/src/graph.ts
- js/src/rag.ts
- js/src/narrative-intelligence-integration.ts
- js/src/emotional-beat-enricher.ts
- js/src/character-arc-tracker.ts
- js/src/analytical-feedback-loop.ts
- js/src/narrative-tracing.ts
- js/src/ceremonial-diary.ts
- js/src/role-tooling.ts

### Updates
- js/src/index.ts
- js/src/types.ts
- js/package.json
- llms.txt
- llms-full.txt

### Communications
- Git commits for each logical implementation step
