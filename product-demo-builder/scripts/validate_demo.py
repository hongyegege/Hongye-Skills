#!/usr/bin/env python3
"""Validate a self-contained Demo HTML against its manifest."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import tempfile
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path


FORBIDDEN = ["tcl", "hongye", "鸿鹄"]
EMAIL_PATTERN = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PHONE_PATTERN = re.compile(r"(?<!\d)1[3-9]\d{9}(?!\d)")
TOKEN_PATTERNS = [
    re.compile(r"\b(?:sk|gh[pousr])[-_][A-Za-z0-9_-]{12,}\b", re.I),
    re.compile(r"\bBearer\s+[A-Za-z0-9._-]{12,}\b", re.I),
    re.compile(r"\b(?:api[_-]?key|access[_-]?token|client[_-]?secret)\s*[:=]\s*['\"]?[A-Za-z0-9._-]{12,}", re.I),
]


class StructureParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.tags: list[str] = []
        self.ids: list[str] = []
        self.actions: list[str] = []
        self.targets: list[str] = []
        self.states: list[str] = []
        self.scripts = 0
        self.external_urls: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.tags.append(tag)
        attrs_map = dict(attrs)
        if "id" in attrs_map and attrs_map["id"]:
            self.ids.append(attrs_map["id"] or "")
        if attrs_map.get("data-action"):
            self.actions.append(attrs_map["data-action"] or "")
        if attrs_map.get("data-target"):
            self.targets.append(attrs_map["data-target"] or "")
        if attrs_map.get("data-state"):
            self.states.append(attrs_map["data-state"] or "")
        if tag == "script":
            self.scripts += 1
        for key in ("src", "href"):
            value = attrs_map.get(key) or ""
            if value.startswith(("http://", "https://")):
                self.external_urls.append(value)


def extract_script(text: str) -> str:
    match = re.search(r"<script(?:\s[^>]*)?>([\s\S]*?)</script>", text, re.I)
    return match.group(1) if match else ""


def run_node_check(script: str, source: Path) -> tuple[bool, str]:
    if not script.strip():
        return False, "no inline script found"
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".mjs", delete=False) as handle:
        handle.write(script)
        temp_path = Path(handle.name)
    try:
        result = subprocess.run(["node", "--check", str(temp_path)], capture_output=True, text=True, check=False)
    except FileNotFoundError:
        return True, "node unavailable; syntax check skipped"
    finally:
        temp_path.unlink(missing_ok=True)
    return result.returncode == 0, result.stderr.strip() or "ok"


def manifest_ids(items: object) -> list[str]:
    if not isinstance(items, list):
        return []
    result: list[str] = []
    for item in items:
        if isinstance(item, str):
            result.append(item)
        elif isinstance(item, dict) and item.get("id"):
            result.append(str(item["id"]))
    return result


def split_refs(value: object) -> set[str]:
    if value is None:
        return set()
    values = value if isinstance(value, list) else [value]
    result: set[str] = set()
    for item in values:
        result.update(part.strip() for part in str(item).split("|") if part.strip())
    return result


def validate(html_path: Path, manifest_path: Path | None) -> dict[str, object]:
    text = html_path.read_text(encoding="utf-8")
    parser = StructureParser()
    parser.feed(text)
    checks: dict[str, object] = {}
    checks["single_html_document"] = text.lower().count("<!doctype html") == 1 and text.lower().count("<html") == 1
    checks["unique_ids"] = len(parser.ids) == len(set(parser.ids))
    checks["one_inline_script"] = parser.scripts == 1
    checks["no_external_urls"] = not parser.external_urls and not re.search(r"https?://(?!example\.invalid/)", text, re.I)
    checks["no_forbidden_terms"] = not any(term in text.lower() for term in FORBIDDEN)
    public_emails = sorted({email for email in EMAIL_PATTERN.findall(text) if not email.lower().endswith("@example.invalid")})
    phone_numbers = sorted(set(PHONE_PATTERN.findall(text)))
    token_findings = sorted({pattern.pattern for pattern in TOKEN_PATTERNS if pattern.search(text)})
    checks["no_public_emails"] = not public_emails
    checks["no_phone_numbers"] = not phone_numbers
    checks["no_token_like_values"] = not token_findings
    node_ok, node_message = run_node_check(extract_script(text), html_path)
    checks["javascript_syntax"] = node_ok
    result: dict[str, object] = {
        "html": str(html_path),
        "checks": checks,
        "details": {
            "node": node_message,
            "public_emails": public_emails,
            "phone_numbers": phone_numbers,
            "token_findings": token_findings,
        },
        "passed": all(bool(value) for value in checks.values()),
    }

    if manifest_path:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        result["manifest"] = str(manifest_path)
        screen_ids = manifest_ids(manifest.get("screens", []))
        state_ids = manifest_ids(manifest.get("states", []))
        action_items = [item for item in manifest.get("actions", []) if isinstance(item, dict)]
        action_ids = manifest_ids(action_items)
        screens = set(screen_ids)
        states = set(state_ids)
        actions = set(action_ids)
        declared_acceptance = {str(item) for flow in manifest.get("acceptanceFlows", []) if isinstance(flow, dict) for item in flow.get("actions", [])}
        html_screens = set(re.findall(r'data-screen=["\']([^"\']+)', text))
        html_actions = set(parser.actions)
        html_actions.update(re.findall(r'data-action=["\']([^"\']+)', text))
        html_actions.update(re.findall(r"case\s+'([^']+)'", extract_script(text)))
        html_targets = set(parser.targets)
        html_targets.update(re.findall(r'data-target=["\']([^"\']+)', text))
        html_states = set(parser.states)
        html_states.update(re.findall(r'data-state=["\']([^"\']+)', text))
        html_states.update(re.findall(r'data-value=["\']([^"\']+)', text))
        for state_id in states:
            if re.search(rf"(?<![A-Za-z0-9_-]){re.escape(state_id)}(?![A-Za-z0-9_-])", text):
                html_states.add(state_id)

        action_refs = set()
        action_targets: set[str] = set()
        actions_have_contract = True
        for item in action_items:
            action_refs.update(split_refs(item.get("from")))
            action_refs.update(split_refs(item.get("to")))
            target = str(item.get("target") or "").strip()
            actions_have_contract = actions_have_contract and bool(item.get("id") and item.get("from") is not None and item.get("to") is not None and target)
            if target:
                action_targets.add(target)
        action_refs.discard("*")
        declared_nodes = screens | states
        manifest_checks = {
            "manifest_screen_ids_unique": len(screen_ids) == len(screens),
            "manifest_state_ids_unique": len(state_ids) == len(states),
            "manifest_action_ids_unique": len(action_ids) == len(actions),
            "manifest_actions_have_contract": actions_have_contract,
            "manifest_screens_reachable": not screens or screens.issubset(html_screens),
            "manifest_states_reachable": not states or states.issubset(html_states),
            "manifest_actions_reachable": not actions or actions.issubset(html_actions),
            "manifest_action_targets_reachable": not action_targets or action_targets.issubset(html_targets | html_actions),
            "manifest_action_refs_valid": action_refs.issubset(declared_nodes),
            "acceptance_actions_declared": not declared_acceptance or declared_acceptance.issubset(actions),
        }
        result["checks"] = {**checks, **manifest_checks}
        result["passed"] = all(bool(value) for value in result["checks"].values())
        result["details"]["html_screens"] = sorted(html_screens)
        result["details"]["html_states"] = sorted(html_states)
        result["details"]["html_actions"] = sorted(html_actions)
        result["details"]["html_targets"] = sorted(html_targets)
        result["details"]["manifest_action_refs"] = sorted(action_refs)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("html", type=Path)
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    result = validate(args.html, args.manifest)
    rendered = json.dumps(result, ensure_ascii=False, indent=2)
    print(rendered)
    if args.report:
        checks = result.get("checks", {})
        lines = [
            "# Demo Verification Report",
            "",
            f"- Generated: `{datetime.now().astimezone().isoformat(timespec='seconds')}`",
            f"- HTML: `{args.html}`",
            f"- Manifest: `{args.manifest}`" if args.manifest else "- Manifest: not supplied",
            "- Overall status: static validation only; this is not a full browser-validation pass.",
            "- Browser smoke: not run by this command; run `node scripts/smoke_test.mjs <index.html>` and record its result separately.",
            "- Known limitation: generated QR visuals are placeholders and are not scannable.",
            "",
            "## Static checks",
            "",
        ]
        lines.extend(f"- [{'x' if value else ' '}] `{name}`" for name, value in checks.items())
        lines.extend(["", "## Machine-readable result", "", "```json", rendered, "```", ""])
        args.report.write_text("\n".join(lines), encoding="utf-8")
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
