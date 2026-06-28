#!/usr/bin/env python3
"""Validate product-launch-speech generated artifacts."""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path


TAG_PATTERNS = {
    "html": re.compile(r"<html\b", re.IGNORECASE),
    "head": re.compile(r"<head\b", re.IGNORECASE),
    "body": re.compile(r"<body\b", re.IGNORECASE),
    "script": re.compile(r"<script\b(?![^>]*\bsrc\s*=)", re.IGNORECASE),
}

SECTION_PATTERNS = {
    "hero": [
        re.compile(r'id=["\']hero["\']', re.IGNORECASE),
        re.compile(r'class=["\'][^"\']*\bintro\b', re.IGNORECASE),
        re.compile(r'data-section=["\']hero["\']', re.IGNORECASE),
    ],
    "live demo": [
        re.compile(r'id=["\']live-demo["\']', re.IGNORECASE),
        re.compile(r'id=["\']s1["\']', re.IGNORECASE),
        re.compile(r"Live Interaction", re.IGNORECASE),
        re.compile(r'data-section=["\']live-demo["\']', re.IGNORECASE),
    ],
    "features": [
        re.compile(r'id=["\']features["\']', re.IGNORECASE),
        re.compile(r'id=["\']s2["\']', re.IGNORECASE),
        re.compile(r"Component Library", re.IGNORECASE),
        re.compile(r'data-section=["\']features["\']', re.IGNORECASE),
    ],
    "key visual": [
        re.compile(r'id=["\']key-visual["\']', re.IGNORECASE),
        re.compile(r'id=["\']s3["\']', re.IGNORECASE),
        re.compile(r"Key Visual", re.IGNORECASE),
        re.compile(r'data-section=["\']key-visual["\']', re.IGNORECASE),
    ],
}

DESIGN_SECTIONS = [
    "Visual Design",
    "Page Sections",
    "Interaction Design",
    "Copy Inventory",
    "Change Notes",
]


def fail(message: str, failures: list[str]) -> None:
    failures.append(message)


def read_text(path: Path, failures: list[str], label: str) -> str:
    if not path.exists():
        fail(f"{label} does not exist: {path}", failures)
        return ""
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        fail(f"{label} must be UTF-8 encoded: {path}", failures)
        return ""


def validate_single_document(html: str, failures: list[str]) -> None:
    for tag_name in ("html", "head", "body"):
        count = len(TAG_PATTERNS[tag_name].findall(html))
        if count != 1:
            fail(f"Expected exactly one <{tag_name}> tag, found {count}.", failures)

    script_count = len(TAG_PATTERNS["script"].findall(html))
    if script_count != 1:
        fail(f"Expected exactly one inline <script> tag, found {script_count}.", failures)


def validate_duplicate_ids(html: str, failures: list[str]) -> None:
    ids = re.findall(r"\bid\s*=\s*['\"]([^'\"]+)['\"]", html, re.IGNORECASE)
    duplicates = sorted(name for name, count in Counter(ids).items() if count > 1)
    if duplicates:
        fail("Duplicate id values: " + ", ".join(duplicates), failures)


def validate_required_sections(html: str, failures: list[str]) -> None:
    for section_name, patterns in SECTION_PATTERNS.items():
        if not any(pattern.search(html) for pattern in patterns):
            fail(f"Missing required launch section: {section_name}.", failures)


def validate_no_remote_dependencies(html: str, failures: list[str]) -> None:
    remote_patterns = [
        r"<script\b[^>]*\bsrc\s*=\s*['\"]https?://",
        r"<link\b[^>]*\bhref\s*=\s*['\"]https?://",
        r"<img\b[^>]*\bsrc\s*=\s*['\"]https?://",
        r"fetch\s*\(\s*['\"]https?://",
    ]
    for pattern in remote_patterns:
        if re.search(pattern, html, re.IGNORECASE):
            fail("HTML should be self-contained and avoid remote runtime dependencies.", failures)
            return


def extract_inline_scripts(html: str) -> list[str]:
    return [
        match.group(1)
        for match in re.finditer(
            r"<script\b(?![^>]*\bsrc\s*=)[^>]*>([\s\S]*?)</script>",
            html,
            re.IGNORECASE,
        )
    ]


def find_node() -> str | None:
    configured = os.environ.get("NODE_EXE")
    if configured and Path(configured).exists():
        return configured
    return shutil.which("node")


def validate_javascript(html: str, failures: list[str]) -> None:
    node = find_node()
    if not node:
        fail("Node.js executable not found; cannot validate inline JavaScript syntax.", failures)
        return

    for index, script in enumerate(extract_inline_scripts(html), start=1):
        with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as tmp:
            tmp.write(script)
            tmp_path = Path(tmp.name)
        try:
            result = subprocess.run(
                [node, "--check", str(tmp_path)],
                text=True,
                capture_output=True,
            )
        finally:
            tmp_path.unlink(missing_ok=True)
        if result.returncode != 0:
            fail(
                f"Inline script {index} has invalid JavaScript syntax: "
                + (result.stderr or result.stdout).strip(),
                failures,
            )


def validate_design_doc(design_path: Path | None, failures: list[str]) -> None:
    if design_path is None:
        fail("Design document is required. Pass --design page-design.md.", failures)
        return
    design = read_text(design_path, failures, "Design document")
    if not design:
        return
    for section in DESIGN_SECTIONS:
        if not re.search(r"^#+\s+" + re.escape(section) + r"\b", design, re.MULTILINE):
            fail(f"Design document missing section: {section}.", failures)


def validate(html_path: Path, design_path: Path | None) -> list[str]:
    failures: list[str] = []
    html = read_text(html_path, failures, "HTML file")
    if html:
        validate_single_document(html, failures)
        validate_duplicate_ids(html, failures)
        validate_required_sections(html, failures)
        validate_no_remote_dependencies(html, failures)
        validate_javascript(html, failures)
    validate_design_doc(design_path, failures)
    return failures


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate launch-style HTML artifacts.")
    parser.add_argument("html", type=Path, help="Path to generated index.html")
    parser.add_argument("--design", type=Path, help="Path to generated page-design.md")
    args = parser.parse_args(argv)

    failures = validate(args.html, args.design)
    if failures:
        print("Validation failed:")
        for item in failures:
            print(f"- {item}")
        return 1

    print("OK: launch HTML artifact and design document passed validation.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
