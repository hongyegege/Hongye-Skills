import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_artifact.py"
TEMPLATE_HTML = ROOT / "assets" / "templates" / "immersive-launch" / "index.html"
TEMPLATE_DESIGN = ROOT / "assets" / "templates" / "immersive-launch" / "page-design.md"


VALID_HTML = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>Demo Launch</title>
<style>.launch-root{color:#fff}</style>
</head>
<body>
<main class="launch-root">
  <section id="hero"><h1>Demo Product</h1></section>
  <section id="live-demo"><button data-scene="demo">Try</button></section>
  <section id="features"><article>Feature</article></section>
</main>
<script>
(() => {
  const root = document.querySelector('.launch-root');
  if (root) root.dataset.ready = 'true';
})();
</script>
</body>
</html>
"""


VALID_MD = """# Demo Product Page Design

## Visual Design
Dark stage with blue AI accent.

## Page Sections
- Hero
- Live Demo
- Features

## Interaction Design
The demo button changes the presentation state.

## Copy Inventory
- Demo Product

## Change Notes
Use this document to request small HTML changes.
"""


def run_validator(tmp_path: Path, html: str = VALID_HTML, md: str | None = VALID_MD):
    html_path = tmp_path / "index.html"
    html_path.write_text(html, encoding="utf-8")
    args = [sys.executable, str(SCRIPT), str(html_path)]
    if md is not None:
        md_path = tmp_path / "page-design.md"
        md_path.write_text(md, encoding="utf-8")
        args.extend(["--design", str(md_path)])
    return subprocess.run(args, text=True, capture_output=True)


class ValidateArtifactTests(unittest.TestCase):
    def with_tempdir(self, callback):
        with tempfile.TemporaryDirectory() as tmp:
            return callback(Path(tmp))

    def test_accepts_valid_launch_artifact(self):
        def check(tmp_path):
            result = run_validator(tmp_path)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("OK", result.stdout)

        self.with_tempdir(check)

    def test_rejects_multiple_html_documents(self):
        def check(tmp_path):
            result = run_validator(tmp_path, VALID_HTML + "\n" + VALID_HTML)
            self.assertEqual(result.returncode, 1)
            self.assertIn("Expected exactly one <html", result.stdout)

        self.with_tempdir(check)

    def test_rejects_duplicate_ids(self):
        def check(tmp_path):
            bad_html = VALID_HTML.replace(
                '<section id="features"><article>Feature</article></section>',
                '<section id="features"><article id="hero">Feature</article></section>',
            )
            result = run_validator(tmp_path, bad_html)
            self.assertEqual(result.returncode, 1)
            self.assertIn("Duplicate id values", result.stdout)

        self.with_tempdir(check)

    def test_rejects_missing_design_document(self):
        def check(tmp_path):
            result = run_validator(tmp_path, md=None)
            self.assertEqual(result.returncode, 1)
            self.assertIn("Design document is required", result.stdout)

        self.with_tempdir(check)

    def test_default_template_contains_ioc_launch_capabilities(self):
        html = TEMPLATE_HTML.read_text(encoding="utf-8")
        design = TEMPLATE_DESIGN.read_text(encoding="utf-8")

        required_html = [
            'id="page-root"',
            'body data-theme="dark"',
            'id="themeToggle"',
            'body[data-theme="light"]',
            "localStorage",
            'data-section="architecture"',
            "const scenes =",
            'data-scene="device_control"',
            'id="editOverlay"',
            "root.addEventListener",
        ]
        for needle in required_html:
            self.assertIn(needle, html)

        required_design = [
            "暗黑 UI",
            "浅色 UI",
            "scenes",
            "技术架构",
            "用户说一句话",
            "确认执行",
            "主题切换",
        ]
        for needle in required_design:
            self.assertIn(needle, design)


if __name__ == "__main__":
    unittest.main()
