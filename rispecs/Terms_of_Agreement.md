# Terms of Agreement — Operating Definitions (PROPOSED)

Purpose: Provide common, non-legal operating definitions that all specs, agents, and contributions follow. Complements `specifications/Creative_Orientation_Operating_Guide.md` and `specifications/RISE_Spec.md`.

## Scope
- Applies to: specs in `specifications/`, agent docs in `agents/`, and agent outputs.
- Intent: Alignment and clarity, not legal contract; governs terminology and expectations for contributions.

## Core Terms (PROPOSED)
- Agent: A specialized, goal-directed component that, given inputs and shared state, applies a policy (prompts, tools, models) to produce outputs that advance a specific desired outcome. It operates autonomously within its scope and composes with other agents via clear input/output contracts and orchestration patterns.
- Observations: Neutral statements of fact about artifacts or behavior. No categorization or judgment.
- Structural Assessment: A concise conclusion, based on observations, indicating whether a structure tends to advance or oscillate relative to the desired outcome.
- Structural Tension: The relationship between Desired Outcome, Current Reality, and Natural Progression.
- Advancing Move: An optional next step that naturally advances structural tension toward the desired outcome; not an attempt to “fix” or “eliminate.”
- Constraints: Explicit boundaries (e.g., time, cost, chapters) that define the field in which advancement occurs; used to stabilize behavior, not to problem-frame.

## Required Blocks in Governed Docs (PROPOSED)
- Structural Tension block
- Observations (neutral)
- Structural Assessment (advance or oscillate)
- Advancing Moves (optional)

## Language Policy (summary)
- Prefer: create, manifest, build, enable, stabilize.
- Avoid: fix, mitigate, eliminate, solve (unless quoting or in strictly technical contexts).

## Compliance
- Agents and contributors include the required blocks and follow language policy.
- CI may lint for presence of required blocks and language patterns.

This document standardizes terms so that teams, agents, and CI interpret specs and outputs consistently under Creative Orientation and RISE principles.