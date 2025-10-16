# CO‑Lint — Creative Orientation Linter Specification

**Status**: ⏳ PLANNED

Version: 0.1.0

## Structural Tension
- Desired Outcome: Maintain methodological integrity by ensuring docs and agent outputs consistently advance Creative Orientation rather than drifting into gap‑thinking.
- Current Reality: Without guardrails, contributors and agents can regress to reactive phrasing and oscillating patterns across specs and reviews.
- Natural Progression: Introduce a simple, configurable linter that validates required blocks and language patterns, guiding outputs toward advancing structures.

## Purpose
Enforce Creative Orientation governance in repository documentation by validating the presence of required blocks, section semantics, and language patterns that advance structural tension. CO‑Lint enables consistent application of the operating rules across specs, agent docs, and readmes.

## Scope
- Applies to: `specifications/**/*.md`, `agents/**/*.md`, top-level `*README.md`, `CLAUDE.md`, `GEMINI.md`, `CURSOR.md`.
- Excludes by default: `Logs/**`, `**/.claude/**`, code files, vendor docs, and any path listed in config `ignore`.
- Governing docs:
  - `specifications/Terms_of_Agreement.md`
  - `specifications/Creative_Orientation_Operating_Guide.md`
  - `specifications/RISE_Spec.md`

## Required Blocks (governed docs)
- Structural Tension block (three lines):
  - "- Desired Outcome:"
  - "- Current Reality:"
  - "- Natural Progression:"
- Observations (neutral)
- Structural Assessment (uses advancing/oscillating language)
- Advancing Moves (optional)

## Rule Set
Each rule has an ID, severity, rationale, and detection criteria. Defaults can be tuned via config.

- COL001 Required Structural Tension block
  - Severity: error
  - Rationale: Anchors creation around structural tension.
  - Criteria: The three labeled lines appear within the first 120 lines.

- COL002 Observations are present and neutral
  - Severity: error (missing), warn (non‑neutral wording)
  - Rationale: Observations are facts; no categorization/judgment.
  - Criteria: A section header matching /^##\s+Observations/i exists; in that section, disallow problem‑elimination verbs (see Language Policy) outside technical contexts.

- COL003 Structural Assessment uses advancing/oscillating terminology
  - Severity: error
  - Rationale: Conclusions belong in assessment; classification is advance vs oscillate.
  - Criteria: Section header /^##\s+Structural Assessment/i exists and contains at least one of: "advance", "advancing", "oscillate", "oscillating" (case‑insensitive). Disallow "problem" framing here.

- COL004 Advancing Moves (if present) use create‑language
  - Severity: warn
  - Rationale: Moves describe natural next steps, not elimination.
  - Criteria: In section /^##\s+Advancing Moves/i, prefer verbs from allowlist (create, manifest, build, enable, stabilize, establish). Flag elimination verbs unless in technical context.

- COL005 Language Policy (document‑wide)
  - Severity: warn (configurable to error)
  - Rationale: Preserve advancing pattern language.
  - Criteria: Flag occurrences of fix|mitigate|eliminate|solve outside code fences and outside allowed Technical Context sections. See Exceptions.

- COL006 PROPOSED label on new governance/operating sections
  - Severity: warn
  - Rationale: Signal proposal status without blocking iteration.
  - Criteria: Headings containing Navigation, Operating Guide, Governance, or new spec introductions should include "(PROPOSED)" or a nearby "PROPOSED" tag.

- COL007 Agent docs reference operating definitions (optional)
  - Severity: warn (off by default)
  - Rationale: Ensure agent docs link Terms/Operating Guide.
  - Criteria: Presence of links to Terms and Creative Orientation guide.

## Language Policy
- Prefer verbs: create, manifest, build, enable, stabilize, establish, advance.
- Avoid verbs: fix, mitigate, eliminate, solve, address, remediate (outside technical contexts).
- Technical Contexts (allowed):
  - Inside fenced code blocks ``` ... ```
  - Sections whose headings include: Troubleshooting, Error, Command, CLI, API, Performance, Benchmark, Test, Installation, Uninstall
  - Files matched by config `allow_technical`: globs per repo needs

## Configuration
Default config file: `.co-lint.json`

Example:
```json
{
  "ignore": ["Logs/**", "**/.claude/**"],
  "allow_technical": [
    "**/LOCAL_MODELS_GUIDE.md",
    "**/TEST_README.md"
  ],
  "severity_overrides": {
    "COL005": "error",
    "COL006": "off",
    "COL007": "warn"
  },
  "rule_filters": ["COL001","COL002","COL003","COL004","COL005"],
  "max_structural_tension_search_lines": 120
}
```

## CLI
- Command: `co-lint [paths...]`
- Options:
  - `--config PATH` (default: .co-lint.json)
  - `--format text|json|github` (default: text)
  - `--rules COL001,COL003` (limit rules)
  - `--severity-threshold warn|error` (for exit code)
  - `--fail-on warn|error` (default: error)
  - `--no-color`
- Exit codes:
  - 0: no findings ≥ threshold
  - 1: findings at warn threshold when `--fail-on warn`
  - 2: findings at error threshold

## Output Formats
- text (default): `path:line  [SEVERITY COLID] message  → snippet`
- json: Array of findings `{ path, line, column, severity, rule, message, excerpt }`
- github: `::warning file=PATH,line=N,col=1,title=COLID::message`

## Pre‑commit Integration
`.pre-commit-config.yaml` (example):
```yaml
repos:
  - repo: local
    hooks:
      - id: co-lint
        name: creative-orientation-lint
        entry: co-lint
        language: system
        types: [markdown]
        files: ^(specifications/|agents/|[^/]*README\.md|CLAUDE\.md|GEMINI\.md|CURSOR\.md)
        args: ["--config", ".co-lint.json", "--format", "github", "--fail-on", "error"]
```

## GitHub Actions Integration
```yaml
name: CO-Lint
on: [push, pull_request]
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.11' }
      - run: pip install co-lint  # or python -m pip install ./.tools/co-lint
      - run: co-lint --config .co-lint.json --format github --fail-on error
```

## Detection & Parsing Notes (implementation)
- Markdown parsing is line‑oriented with a simple state machine:
  - Track fenced code blocks to suppress language checks.
  - Identify sections by `^#{2,}\s+Heading`.
  - Capture section ranges for Observations, Structural Assessment, Advancing Moves.
- Structural Tension detection: exact label prefixes; allow flexible spacing after colon.
- Case‑insensitive matching; unicode‑safe; ignore content in HTML comments.

## False Positive Mitigation
- Respect code fences and Technical Contexts.
- Allow per‑file inline overrides via HTML comments:
  - `<!-- co-lint: disable COL005 -->` and `<!-- co-lint: enable COL005 -->`
- Configurable allowlists for domain‑specific terms.

## Deliverables
- Minimal Python CLI implementing the above.
- Default `.co-lint.json` committed with sane defaults.
- Pre‑commit hook and Action examples in docs.

## Success Criteria
- Governed docs include required blocks and pass COL001–COL005 by default.
- CI fails when governance is missing or elimination language appears outside allowed contexts.
- Teams can tune severities and ignores without code changes.

---

## Appendix — Structural Connection (PROPOSED)
- Intent: This linter is the concrete implementation of an “AI consistency checker” that prevents contextual regression into gap‑thinking and preserves Creative Orientation in all outputs.
- Perspective (Mia): A direct blueprint for the filtering mechanism needed to maintain methodological integrity across agents.
- Perspective (Miette): A delightful “consistency sprite” manual that spots “fixing problems” language and keeps the creative garden advancing.
