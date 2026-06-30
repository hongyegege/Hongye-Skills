# Style Presets

## ai-stage-dark

Use by default for the immersive launch template.

- Background: black or near-black presentation stage, with a complete `body[data-theme="light"]` override when the page will be shown in bright rooms or on projectors.
- Accent: saturated blue for AI recognition and routing, green for execution and energy/value results, amber for risk/data attention, coral for governance warnings, violet for access or architecture layers.
- Surfaces: translucent dark panels, dashboard consoles, architecture boards, subtle borders, restrained blur.
- Typography: system sans, compact tracking, large direct headline.
- Motion: status transitions, progressive step highlights, card expansion, theme-safe hover states, subtle background grid or console effects.
- Best for: AI assistants, IOC/control systems, smart building products, operations platforms, launch demos, futuristic product moments.

## minimal-white

- Background: white or very light neutral.
- Accent: one brand color plus black text.
- Surfaces: low-shadow white panels, thin borders, strong whitespace.
- Motion: minimal transitions only.
- Best for: productivity tools, developer tools, documentation-heavy launches.

## enterprise-saas

- Background: quiet dark or light work surface.
- Accent: brand color used sparingly.
- Surfaces: dashboards, tables, workflows, status chips, comparison panels.
- Motion: restrained state changes, no decorative animation.
- Best for: CRM, operations, analytics, finance, internal systems.

## brand-led

- Background: derived from user brand material.
- Accent: product or company primary color.
- Surfaces: adapt to brand tone while preserving launch-page readability.
- Motion: match brand personality.
- Best for: user provides clear brand colors, logo, or design guidelines.

## Choosing A Preset

If the user gives no style preference, choose `ai-stage-dark`. If the product is operational SaaS, choose `enterprise-saas`. If the user provides brand colors, choose `brand-led` and document the chosen palette in `page-design.md`.

For the default immersive template, keep dark and light token sets paired. When changing `:root` colors, also update `body[data-theme="light"]` component overrides and describe both modes in `page-design.md`.
