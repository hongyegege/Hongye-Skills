# Demo Verification Report

- Generated: `2026-08-21T15:56:04+08:00`
- HTML: `assets\demo-shell.template.html`
- Manifest: `examples\demo-manifest.json`
- Overall status: static validation only; this is not a full browser-validation pass.
- Browser smoke: not run by this command; run `node scripts/smoke_test.mjs <index.html>` and record its result separately.
- Browser smoke result in this environment: `skipped` — Playwright is not installed.
- Known limitation: generated QR visuals are placeholders and are not scannable.

## Sources and scope

- Inputs: two local interactive HTML attachments; source paths and organization-bearing folder names are intentionally omitted from this public-safe report.
- Confirmed: offline phone stage, two neutral product configurations, four screens, eight states, sixteen actions, four flows, and five acceptance flows.
- Placeholders: synthetic users, fixed demo timestamps, visual-only QR blocks, deterministic loading delays, and offline Toast feedback.
- Pending: no unresolved product decisions remain for this reference example. New product requests must pass `references/question-gate.md` independently.

## Sanitized reference copies

- `device-share-interactive-prototype-v2.html`: static validation passed; a fresh sanitization run matched the published copy byte-for-byte.
- `device-share-merged-interactive-prototype.html`: static validation passed; a fresh sanitization run matched the published copy byte-for-byte.
- Both copies contain no external URLs, public email addresses, phone numbers, token-like values, or forbidden organization terms.
- These copies preserve the original attachments' own screens and actions, so they are intentionally validated without the template-specific `demo-manifest.json`.

## Static checks

- [x] `single_html_document`
- [x] `unique_ids`
- [x] `one_inline_script`
- [x] `no_external_urls`
- [x] `no_forbidden_terms`
- [x] `no_public_emails`
- [x] `no_phone_numbers`
- [x] `no_token_like_values`
- [x] `javascript_syntax`
- [x] `manifest_screen_ids_unique`
- [x] `manifest_state_ids_unique`
- [x] `manifest_action_ids_unique`
- [x] `manifest_actions_have_contract`
- [x] `manifest_screens_reachable`
- [x] `manifest_states_reachable`
- [x] `manifest_actions_reachable`
- [x] `manifest_action_targets_reachable`
- [x] `manifest_action_refs_valid`
- [x] `acceptance_actions_declared`

## Machine-readable result

```json
{
  "html": "assets\\demo-shell.template.html",
  "checks": {
    "single_html_document": true,
    "unique_ids": true,
    "one_inline_script": true,
    "no_external_urls": true,
    "no_forbidden_terms": true,
    "no_public_emails": true,
    "no_phone_numbers": true,
    "no_token_like_values": true,
    "javascript_syntax": true,
    "manifest_screen_ids_unique": true,
    "manifest_state_ids_unique": true,
    "manifest_action_ids_unique": true,
    "manifest_actions_have_contract": true,
    "manifest_screens_reachable": true,
    "manifest_states_reachable": true,
    "manifest_actions_reachable": true,
    "manifest_action_targets_reachable": true,
    "manifest_action_refs_valid": true,
    "acceptance_actions_declared": true
  },
  "details": {
    "node": "ok",
    "public_emails": [],
    "phone_numbers": [],
    "token_findings": [],
    "html_screens": [
      "account",
      "manage",
      "qr",
      "share"
    ],
    "html_states": [
      "${enabled ? ",
      "${list.length ? ",
      "${state.qr}",
      "confirm",
      "empty",
      "expired",
      "failed",
      "filled",
      "loading",
      "normal",
      "productA",
      "productB",
      "success"
    ],
    "html_actions": [
      "${action}",
      "back",
      "clear-input",
      "clear-recent",
      "close-modal",
      "confirm-clear",
      "confirm-delete",
      "confirm-share",
      "delete-contact",
      "go-home",
      "lookup-user",
      "open-account",
      "open-manage",
      "open-qr",
      "refresh-qr",
      "reset",
      "select-user"
    ],
    "html_targets": [
      "phone-stage",
      "qr-stage",
      "screen-root",
      "toast-root"
    ],
    "manifest_action_refs": [
      "account",
      "confirm",
      "manage",
      "qr",
      "share"
    ]
  },
  "passed": true,
  "manifest": "examples\\demo-manifest.json"
}
```
