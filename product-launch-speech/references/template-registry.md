# Template Registry

## Immersive Launch

- Template path: `assets/templates/immersive-launch/index.html`
- Design notes path: `assets/templates/immersive-launch/page-design.md`
- Use for: product launch demos, AI assistant demos, IOC / operations platforms, IoT/control surfaces, code-product showcases, internal review pages, and keynote-style feature introductions.
- Structure: Hero, interactive live demo, multi-platform or entrypoint section, feature cards, how-it-works flow, data/action flow, governance or tenant story, and optional architecture board.
- Default style: dark stage with light-mode override, blue AI accent, green execution accent, amber/coral/violet supporting states, glass panels, dashboard/demo console, animated state transitions.

## Replacement Rules

When adapting the template:

- Replace product identity in `<title>`, header brand text, Hero copy, demo console, feature cards, footer, and `page-design.md`.
- Replace demo scenes in the `scenes` object before changing the visual shell.
- Keep section anchors or equivalent semantic markers for Hero, Live Demo, and Features.
- When changing the top navigation, keep anchors, section order, and `page-design.md` Page Sections in sync. The Hero can remain first-viewport content without appearing in top navigation.
- For products with a technical or platform story, adapt the architecture board instead of deleting it by default.
- Keep the page self-contained unless the user explicitly asks for a framework or external asset pipeline.
- Prefer root-scoped event listeners under `#page-root`. Do not add duplicate IDs or a second inline script.

## Future Template Slot

Add new templates as sibling folders under `assets/templates/<template-name>/` with:

- `index.html`
- `page-design.md`
- A registry entry with use cases, required sections, style defaults, and replacement rules.

Future candidates:

- `minimal-white-launch`: bright, editorial, low-motion product introduction.
- `enterprise-saas-demo`: dense workflow demo for B2B/operations products.
- `hardware-keynote`: object-first hero and physical product feature tour.
- `code-platform-launch`: developer-product demo with architecture and API evidence.
