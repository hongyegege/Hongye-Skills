# Interaction Patterns

## Launch State Machine

Use when the product has a demoable workflow.

Recommended states:

- `idle`: product or assistant is ready.
- `listening` or `input`: user intent appears.
- `thinking` or `resolving`: system interprets data.
- `presenting`: generated recommendation, UI, or workflow appears.
- `editing`: user adjusts a parameter.
- `executing` or `done`: result is confirmed.

For the default immersive template, model scenes in one `scenes` object. Each scene should own the user query, narrative, metrics, action plan, evidence, step labels, confirm-button copy, and any rule such as hiding the parameter editor.

## Scene Cards

Use for multi-step scenarios such as "watch TV", "deploy project", "create report", or "resolve alert".

- Show the user's natural-language request.
- Show the proposed steps before execution.
- Make one or two rows editable when that supports the product story.
- Include confirm/cancel or primary action.
- For control or operations scenes, show confirmation before execution and a clear completed state after confirmation.

## Parameter Editor

Use for launch moments where the system is powerful but still controllable.

- Open a focused overlay.
- Show one parameter: number, mode, time, audience, model, region, or policy.
- Commit back into the scene card.
- Preserve the main demo state after closing.

## Non-Technical Launch Narrative

Use when the audience includes executives, managers, operators, or non-technical staff.

- Explain capability as "the user says one thing, the assistant understands, routes to an agent, asks for confirmation, and leaves traceable results."
- Put technical proof in evidence panels, data-flow sections, and architecture boards, not in the hero headline.
- Keep scene prompts close to real operational language.

## Theme Toggle

Use when a launch page may be shown in both dark-room keynote and bright meeting-room settings.

- Use one toggle such as `#themeToggle` and store preference with `localStorage` when possible.
- Keep `body[data-theme]`, labels, ARIA state, CSS variables, and `page-design.md` synchronized.
- Do not add a second inline script for theme-only changes.

## Architecture Board

Use when the product has platform, agent, data, or governance depth.

- Show layers such as entrypoints, orchestration, agents, capabilities, and data.
- Keep the board near the end of the page after audience-facing value is clear.
- Update navigation anchors and Copy Inventory when layer names change.

## Digest Or Summary Sheet

Use for AI products that summarize a larger context.

- Start with a generated-by label.
- Group urgent items first.
- Include at least one recommended action.
- Add a short caveat when the content is inferred.

## Feature Evidence Panel

Use when adapting the template to code products.

- Show concrete inputs and outputs.
- Include architecture, API, config, or test evidence only when it helps the launch story.
- Avoid dumping raw code unless the audience is technical.

## Screenshot Frame

Include a stable frame when the user needs slide screenshots.

- It should contain the product identity, core UI state, and one proof of value.
- It should not be a generic decorative hero.
- Keep it visually consistent with the live demo section.
