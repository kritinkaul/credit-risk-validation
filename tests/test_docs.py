"""Catch broken relative file links in the authored documentation."""

import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]


def test_documentation_file_links_exist():
    documents = [ROOT / "README.md", ROOT / "CONTRIBUTING.md"]
    documents += list((ROOT / "docs").glob("*.md"))
    documents += [ROOT / folder / "README.md" for folder in ("data", "sql", "reports", "notebooks")]
    for document in documents:
        for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", document.read_text()):
            parsed = urlsplit(target)
            if parsed.scheme or not parsed.path:
                continue
            assert (document.parent / unquote(parsed.path)).is_file(), (document, target)
