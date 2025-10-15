# 3‑Chapter Test Preset (PROPOSED)

## Structural Tension
- Desired Outcome: Stable test runs that consistently create exactly 3 chapters with predictable time/cost.
- Current Reality: Chapter count can vary across runs/environments.
- Natural Progression: Provide a minimal preset that stabilizes chapter count across CLI/config/tests.

## Observations
- Tests and manual runs may diverge in chapter count handling.

## Structural Assessment
- Tendency to oscillate without an explicit preset that overrides chapter determination during tests.

## Advancing Moves
- Preset Name/Flag: `--TestPreset three_chapters` (CLI) and `TestPreset=three_chapters` (config).
- Enforcement Points:
  - Override chapter determination to 3 during preset activation (affects `CHAPTER_COUNT_PROMPT` consumption only in test mode).
  - Ensure downstream loops, scene expansion, and critique limits respect the fixed chapter count.
  - Test runner hint: `run_rag_tests.py` may pass the preset in quick/ci modes.
- Acceptance Criteria (DoD):
  - Given the preset, runs always output 3 chapters; logs reflect enforced count.
  - CI quick/ci modes use the preset by default; full mode may opt out.
  - Language in docs remains create-oriented (no problem-elimination phrasing).
