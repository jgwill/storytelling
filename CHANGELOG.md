# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-01-30

### 🎉 Major Release: Narrative Intelligence Stack Integration

This release integrates storytelling with the complete Narrative Intelligence Stack
(LangChain tracing, LangGraph three-universe analysis, Miadi webhook consumption).

### Added

**Narrative Coherence Protocol (NCP) Integration**
- `StoryBeat` dataclass with full narrative metadata and three-universe analysis
- `CharacterArcState` for tracking character development journeys
- `CharacterArcTracker` for managing multiple character arcs
- `NCPState` container for session/story context
- `NCPAwareStoryGenerator` for coherent beat generation
- `ArcPoint` and `RelationshipState` for arc tracking
- `EmotionalAnalysis` for emotion detection and scoring

**Emotional Beat Enrichment**
- `EmotionalBeatEnricher` class for quality enhancement
- `QualityThreshold` constants (EXCELLENT, GOOD, ADEQUATE, WEAK)
- `ENRICHMENT_TECHNIQUES` dictionary (stakes, sensory, internal, dialogue, action, etc.)
- `EnrichedBeatResult` container for enrichment results

**Analytical Feedback Loop**
- `AnalyticalFeedbackLoop` for gap analysis and routing
- `GapType` enum (EMOTIONAL_WEAK, CHARACTER_INCONSISTENT, THEME_MISSING, etc.)
- `GapSeverity` enum (CRITICAL, MAJOR, MINOR)
- `GapDimension` enum for multi-dimensional analysis
- `FlowRoute` and `Enrichment` for gap resolution

**Narrative Story Graph**
- `NarrativeAwareStoryGraph` LangGraph-style orchestration
- `GraphState` for graph execution state
- `NodeResult` and `NodeStatus` for node tracking
- `create_narrative_story_graph()` factory function
- Automatic tracing integration via session_id

**Langfuse Tracing Integration**
- `StorytellingTracer` class for observability
- `TraceContext` for trace state management
- `STORYTELLING_EVENT_TYPES` taxonomy (BEAT_*, GAP_*, CHARACTER_*, etc.)
- `get_tracer()` singleton accessor
- Graceful degradation when Langfuse not available
- Correlation header support for cross-system tracing

### Changed
- CLI advanced mode now properly handles `--version` and `--help` flags
- Test suite expanded to 39 passing tests
- Package exports updated to include all NCP modules

### Technical Notes
- Three-Universe Analysis: Each beat can include `universe_analysis` field
- Correlation Headers: `X-Narrative-Trace-Id`, `X-Story-Id`, `X-Session-Id`
- Integration Point: Works with langchain narrative-tracing adapter

## [Unreleased]

### Added
- Initial package structure
- Core storytelling functionality
- Command-line interface
- Comprehensive development tooling
- Testing infrastructure
- Release automation

## [0.1.0] - 2024-09-07

### Added
- Initial release
- Story class for managing stories
- Basic CLI for creating stories
- Professional Python packaging setup
- Development environment with Makefile
- Automated testing with pytest
- Code quality tools (black, ruff, mypy)
- Release automation scripts