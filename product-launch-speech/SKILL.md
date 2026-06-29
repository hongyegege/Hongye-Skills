---
name: product-launch-speech
description: Generate or modify self-contained HTML product-launch presentation pages and matching editable page-design Markdown notes. Use when Codex needs to turn a product, codebase, README, feature list, demo script, launch narrative, brand style, or existing page-design.md into an interactive product-release style HTML demo, keynote-style product introduction page, or fast incremental HTML update from design notes.
---

# Product Launch Speech

## Outcome

Create a launch-style `index.html` and a matching `page-design.md` that can be used for later small edits. Favor a polished, self-contained, interactive product demo page over a marketing landing page.

Use the cleaned template at `assets/templates/immersive-launch/index.html` as the starting point for immersive, stage-like pages. Use `assets/templates/immersive-launch/page-design.md` as the companion documentation model.

## Workflow

1. Inspect the user's source material before designing:
   - Read provided product docs, README files, source entry points, screenshots, existing HTML, or `page-design.md`.
   - Identify product audience, launch goal, top features, proof points, demo path, required screenshots/assets, and constraints.
   - Ask only for missing product intent that cannot be inferred from the supplied material.

2. Build a page blueprint before writing HTML:
   - Product promise and one-sentence launch message.
   - Page sections and speaker flow.
   - Interactive demo states and user-triggered moments.
   - Visual system: palette, typography, density, motion, and imagery.
   - Copy inventory: titles, subtitles, button labels, scene prompts, and card copy.

3. Generate artifacts:
   - Create `index.html` as a single self-contained HTML document.
   - Create `page-design.md` with the required sections from `references/page-design-contract.md`.
   - Avoid remote runtime dependencies by default. Inline CSS and JavaScript unless the user explicitly asks for a framework project.
   - Keep all new event binding scoped to one page root. Avoid duplicate IDs and avoid adding new global functions.

4. Validate before reporting completion:
   - Run `scripts/validate_artifact.py <path-to-index.html> --design <path-to-page-design.md>`.
   - Open the page or otherwise smoke-test at least two interactions when a browser is available.
   - Fix validation failures before handing off.

## Editing Existing Pages

When the user provides an existing `page-design.md` to modify an HTML page:

1. Read both the MD and the current HTML.
2. Treat the newest user instruction and MD changes as the source of intent.
3. Preserve the existing template structure, animation quality, and working interactions.
4. Make the smallest HTML/CSS/JS edit that satisfies the requested change.
5. Update `page-design.md` so it remains an accurate editing contract.
6. Re-run the validator.

## Resource Map

- `references/template-registry.md`: choose the launch template and see future template extension rules.
- `references/style-presets.md`: choose or adapt visual style presets.
- `references/interaction-patterns.md`: choose demo and component interaction patterns.
- `references/page-design-contract.md`: required structure for the editable Markdown companion.
- `scripts/validate_artifact.py`: validate generated HTML and MD artifacts.

Read only the reference files needed for the current task. For a normal first-generation request, read all four references once. For a small edit from `page-design.md`, usually read only `page-design-contract.md` and the current artifacts.

## Quality Bar

- The first viewport must communicate the product, not explain the generator.
- The page must feel like a live product launch demo: concrete product states, visible feature evidence, and interaction moments.
- The generated HTML must contain exactly one document root, no duplicate IDs, one main inline script, and the core sections: Hero, Live Demo, and Features.
- The MD companion must be detailed enough that a future Codex run can make small edits without re-reading all original product material.
