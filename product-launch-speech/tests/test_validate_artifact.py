import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_artifact.py"


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
  <section id="key-visual"><canvas id="orb-canvas"></canvas></section>
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
- Key Visual

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


if __name__ == "__main__":
    unittest.main()
