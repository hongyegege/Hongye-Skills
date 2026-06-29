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

## Scene Cards

Use for multi-step scenarios such as "watch TV", "deploy project", "create report", or "resolve alert".

- Show the user's natural-language request.
- Show the proposed steps before execution.
- Make one or two rows editable when that supports the product story.
- Include confirm/cancel or primary action.

## Parameter Editor

Use for launch moments where the system is powerful but still controllable.

- Open a focused overlay.
- Show one parameter: number, mode, time, audience, model, region, or policy.
- Commit back into the scene card.
- Preserve the main demo state after closing.

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


