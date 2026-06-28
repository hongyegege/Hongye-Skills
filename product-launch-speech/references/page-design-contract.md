# Page Design Contract

Create or update `page-design.md` beside every generated `index.html`.

## Required Sections

Use these exact English headings so `scripts/validate_artifact.py` can validate the document. The body text may be Chinese or English.

### Visual Design

Describe the visual direction, palette, typography, surfaces, motion style, imagery, and first-viewport impression.

### Page Sections

List every major section in page order. Include each section's purpose and the main user-facing title.

### Interaction Design

Describe clickable elements, state changes, overlays, demo flow, animation triggers, and expected reset behavior.

### Copy Inventory

List the important titles, subtitles, CTA labels, scene prompts, card headings, and captions that future edits are likely to change.

### Change Notes

Explain how to request small edits through the MD. Include what should be changed together, such as brand name plus title, palette plus CSS variables, or demo scene plus card copy.

## Edit Priority

When editing from a revised `page-design.md`:

1. Follow the newest user message.
2. Follow the revised MD.
3. Preserve working HTML structure and interactions.
4. Preserve template quality when a requested change is underspecified.

## Minimum Detail

The MD must let a future Codex run make copy, section, color, and interaction changes without re-reading the original product docs. Do not summarize with vague labels like "modern style" or "several sections"; name concrete visual and content decisions.
