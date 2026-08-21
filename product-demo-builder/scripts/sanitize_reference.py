#!/usr/bin/env python3
"""Create a neutral, public-safe copy of a reference HTML file."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


REPLACEMENTS = [
    # Code identifiers must be rewritten before the broader case-insensitive
    # display-name patterns; otherwise an unquoted object key such as tclhome
    # would become an invalid key containing a space.
    (re.compile(r"tclhome", re.I), "productA"),
    (re.compile(r"tclplus", re.I), "productB"),
    (re.compile(r"TCL\s*Home\s*APP", re.I), "产品 A APP"),
    (re.compile(r"TCL\s*Home", re.I), "产品 A"),
    (re.compile(r"TCLHome\s*API", re.I), "Product A API"),
    (re.compile(r"TCLHome", re.I), "productA"),
    (re.compile(r"TCL\+", re.I), "产品 B"),
    (re.compile(r"TCLer", re.I), "Demo User"),
    (re.compile(r"TCL\s*ID", re.I), "Demo ID"),
    (re.compile(r"TCL\s*Account", re.I), "Demo Account"),
    (re.compile(r"国内版", re.I), "产品 B"),
    (re.compile(r"TCL", re.I), "产品 A"),
    (re.compile(r"Hongye", re.I), "Demo Organization"),
    (re.compile(r"鸿鹄", re.I), "示例组织"),
    (re.compile(r"thome-IN4@end\.tw", re.I), "demo-user@example.invalid"),
    (re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"), "demo-user@example.invalid"),
    (re.compile(r"15877367638"), "00000000000"),
]

FORBIDDEN = [
    r"TCL",
    r"TCLHome",
    r"TCL Home",
    r"TCL\+",
    r"TCLer",
    r"TCL ID",
    r"TCL Account",
    r"Hongye",
    r"鸿鹄",
]


def sanitize(text: str) -> tuple[str, list[dict[str, object]]]:
    changes: list[dict[str, object]] = []
    result = text
    for pattern, replacement in REPLACEMENTS:
        count = len(pattern.findall(result))
        if count:
            result = pattern.sub(replacement, result)
            changes.append({"pattern": pattern.pattern, "replacement": replacement, "count": count})
    return result, changes


def scan(text: str) -> dict[str, list[str]]:
    findings: dict[str, list[str]] = {}
    for pattern in FORBIDDEN:
        matches = sorted(set(re.findall(pattern, text, re.I)))
        if matches:
            findings.setdefault("forbidden_terms", []).extend(matches)
    if re.search(r"\b(?:sk|gh[pousr])[-_][A-Za-z0-9_-]{12,}\b", text):
        findings.setdefault("tokens", []).append("token-like value")
    if re.search(r"\bBearer\s+[A-Za-z0-9._-]{12,}\b", text, re.I):
        findings.setdefault("tokens", []).append("Bearer token")
    if re.search(r"(?<!\d)1[3-9]\d{9}(?!\d)", text):
        findings.setdefault("phone_like", []).append("11-digit phone-like value")
    emails = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
    if [email for email in emails if not email.lower().endswith("@example.invalid")]:
        findings.setdefault("email_like", []).append("email-like value")
    if re.search(r"https?://(?!example\.invalid/)[^\"'<>\s]+", text, re.I):
        findings.setdefault("external_urls", []).append("external URL")
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()

    original = args.source.read_text(encoding="utf-8")
    sanitized, changes = sanitize(original)
    findings = scan(sanitized)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(sanitized, encoding="utf-8")
    report = {
        "source": str(args.source),
        "output": str(args.output),
        "changes": changes,
        "findings": findings,
        "passed": not findings,
    }
    if args.report:
        args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if not findings else 2


if __name__ == "__main__":
    raise SystemExit(main())
