# Template Registry

## Immersive Launch

- Template path: `assets/templates/immersive-launch/index.html`
- Design notes path: `assets/templates/immersive-launch/page-design.md`
- Use for: product launch demos, AI assistant demos, IoT/control surfaces, code-product showcases, internal review pages, and keynote-style feature introductions.
- Structure: Hero, interactive live demo, flow controls, generated UI component library.
- Default style: dark stage, blue AI accent, glass panels, phone/demo device frame, animated state transitions.

## Replacement Rules

When adapting the template:

- Replace product identity in `<title>`, header brand text, Hero copy, demo cards, and component titles.
- Replace demo scenes in the `SCENES` object before changing the visual shell.
- Keep section anchors or equivalent semantic markers for Hero, Live Demo, and Features.
- Keep the page self-contained unless the user explicitly asks for a framework or external asset pipeline.
- Prefer root-scoped event listeners for new interactions. Do not add duplicate IDs.

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
