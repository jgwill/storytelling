# NARINTEL: Narrative Intelligence for Decolonized Storytelling

> **NARINTEL** (Narrative Intelligence Tools) — structural reorientation of AI-assisted storytelling toward Indigenous Epistemology, Ontology, Methodology, and Axiology. Not decorative language. Not metaphor.

---

## What NARINTEL Is

NARINTEL transforms story generation from text production into relational co-creation. The system generates narrative beats with persistent character memory, emotional quality assurance, thematic thread tracking, and ceremonial mode awareness.

The name carries intent: **Nar**rative **Intel**ligence tools built within a decolonized framework. Knowledge belongs to the relationships, land, and communities that created it.

---

## Core Architecture

### NCP (Narrative Cognition Protocol)
A structured representation for stories: characters carry state (emotions, relationships, arc position), beats carry metadata (emotional tone, thematic resonance, universe analysis), and the generation process tracks continuity across the full narrative.

### Three-Universe Model
Every beat is analyzable from three simultaneous perspectives:

| Universe | Orientation | Core Question |
|----------|------------|---------------|
| **Engineer** 🔧 | Structural | Does the plot logic hold? Are motivations clear? |
| **Story Engine** 📖 | Narrative | Is the prose alive? Does the pacing work? |
| **Ceremony** 🙏 | Relational | What does this moment mean? Who does it serve? |

This is not a UI feature — it is a structural commitment to meaning-making that informs generation, analysis, and enrichment.

### Generation → Analysis → Enrichment Loop
1. **Generate** beat with NCP context (character state, theme, emotional target)
2. **Analyze** emotional quality, character arc impact, thematic resonance
3. **Identify gaps** where the beat needs strengthening
4. **Enrich** weak beats automatically (sensory detail, emotional specificity, dialogue authenticity)
5. **Track** character arc impact and update state
6. **Continue** generation with full awareness of what came before

---

## Capabilities

### Character Memory & Arc Tracking
Characters carry persistent state across all beats. Growth is cumulative. Inconsistencies are caught. Relationships evolve. Speech patterns shift with character development. A character who starts guarded doesn't suddenly become open without the intervening beats earning that transition.

### Emotional Beat Enrichment
Every emotionally significant moment is scored for quality (0–1). Beats below threshold are enriched: stakes made clearer, sensory detail strengthened, internal conflict made visible, dialogue made specific. This happens before the writer sees it.

### Thematic Thread Awareness
Themes introduced early are tracked, reinforced at key moments, and brought to resolution. A theme of "what does home mean?" seeded in beat 1 is recognized when a character finds refuge in beat 5, questioned in beat 9, and redefined in beat 15.

### Analytical Feedback
Multi-dimensional assessment after each beat: character arc impact ✓/⚠️, emotional authenticity ✓/⚠️, dialogue consistency ✓/⚠️, thematic resonance ✓/⚠️. Specific suggestions, not vague complaints.

### Ceremonial Mode
When `ceremonial_mode=True`:
- Indigenous-inspired prompts activated (Spiral of Memory, Two-Eyed Seeing, Seven-Generation Thinking)
- K'é relationship tracking honored explicitly
- Sacred pause between beats — the generation process holds space
- COAIA (Ceremonial Diary) integration connects diary to narrative structure

### Role-Based Tooling
Seven narrative roles, each with specialized tools:

| Role | Function |
|------|----------|
| **Architect** | Structural integrity, plot logic, pacing |
| **Structurist** | NCP schema management, data model alignment |
| **Storyteller** | Prose generation, voice, atmosphere |
| **Editor** | Quality assessment, enrichment, refinement |
| **Reader** | Audience perspective, emotional impact testing |
| **Collaborator** | Cross-role coordination, session management |
| **Witness** | Ceremonial accountability, relational meaning |

---

## Technical Foundation

### Python Package (`storytelling/`)
28 modules including:
- `graph.py` — LangGraph story generation graph
- `prompts.py` — 55KB of narrative prompts (including Indigenous-inspired templates)
- `narrative_intelligence_integration.py` — NCP-aware story generator
- `emotional_beat_enricher.py` — Emotional quality assessment and enrichment
- `analytical_feedback_loop.py` — Gap identification and routing
- `narrative_story_graph.py` — NarrativeAwareStoryGraph orchestration
- `character_arc_tracker.py` — Persistent character state
- `ceremonial_diary.py` — Ceremonial mode and COAIA integration
- `role_tooling.py` — Role-based tool registry
- `narrative_tracing.py` — Langfuse observability integration
- `rag.py` / `enhanced_rag.py` — Knowledge base retrieval

### TypeScript Package (`js/`)
Parity implementation for Node.js and browser contexts. CLI (`storyjs`) and MCP server access.

### Specifications (`rispecs/`)
38 RISE specification files defining behavior:
- `Narrative_Intelligence_Integration_Specification.md`
- `Character_Arc_Tracking_Specification.md`
- `Emotional_Beat_Enrichment_Specification.md`
- `Analytical_Feedback_Loop_Specification.md`
- `Narrative_Aware_Story_Graph_Specification.md`
- `IAIP_Integration_Specification.md`
- Full list in `rispecs/`

### Ecosystem Integration
- **LLM Providers**: Claude, GPT, Gemini (pluggable via provider abstraction)
- **Langfuse**: Story generation tracing and analytics
- **NarIntel Toolkit** (`/workspace/repos/narintel/`): NCP type provider
- **IAIP** (`/a/src/IAIP/`): Ceremonial-technology and relational-science-research apps

---

## Getting Started

```bash
# Python
pip install storytelling
storytelling generate --prompt "A story about returning home" --ceremonial

# TypeScript
npx storytellingjs generate --prompt "A story about returning home" --ceremonial

# MCP Server
storytellingjs --mcp
```

### Configuration
Environment variables in `.env`:
- `LLM_PROVIDER` — Model provider (anthropic, openai, openrouter)
- `LLM_API_KEY` — API key for the provider
- `LANGFUSE_PUBLIC_KEY` / `LANGFUSE_SECRET_KEY` — Observability
- `CEREMONIAL_MODE` — Enable ceremonial-mode generation

---

## Relational Context

NARINTEL exists within a kinship network described in [`KINSHIP.md`](KINSHIP.md). The storytelling package is accountable to:
- Indigenous communities whose epistemological frameworks inform its design
- Writers and narrative practitioners who use it
- AI companions (Mia, Miette, Ava8) who participate in the creative process
- The narrative traditions and oral storytelling practices that predate digital systems

See [`KINSHIP.md`](KINSHIP.md) for the full relational charter.

---

**Package**: [github.com/jgwill/storytelling](https://github.com/jgwill/storytelling)
**Specifications**: `rispecs/`
**Issue tracking**: GitHub Issues #20 (NarIntel), #21 (Implementation), #22 (JS Parity), #23 (LLMS-txt)
