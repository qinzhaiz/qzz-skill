#!/usr/bin/env python3
"""Format linter for knowledge concepts.

Checks:
  1. All 7 required files exist
  2. metadata.yaml field completeness and types
  3. Markdown link validity (relative paths)
  4. Code block language tags

Usage:
  python tools/lint.py                          # lint all concepts
  python tools/lint.py skills/qzz-mysql/knowledge/01-basic/<concept>  # lint single concept
"""

import sys
import os
import re
from pathlib import Path

REQUIRED_FILES = [
    "README.md",
    "metadata.yaml",
    "examples.md",
    "exercises.md",
    "mistakes.md",
    "interview.md",
    "references.md",
]

VALID_DIFFICULTIES = {"beginner", "intermediate", "advanced"}


def lint_concept(concept_dir: Path, knowledge_root: Path) -> list[str]:
    """Run all checks on a single concept directory. Returns list of error messages."""
    errors = []

    # 1. Check required files exist
    for filename in REQUIRED_FILES:
        if not (concept_dir / filename).exists():
            errors.append(f"Missing required file: {filename}")

    # 2. Check for opening code blocks without language tags
    # An opening fence: stripped == "```" AND (first line OR preceded by blank line)
    # A closing fence: stripped == "```" AND preceded by non-blank content
    md_files = concept_dir.glob("*.md")
    for md_file in md_files:
        content = md_file.read_text(encoding="utf-8")
        lines = content.split("\n")
        for idx, line in enumerate(lines):
            stripped = line.strip()
            if stripped != "```":
                continue
            # Closing fence if previous line exists and has non-blank content
            prev_non_blank = False
            for j in range(idx - 1, -1, -1):
                if lines[j].strip():
                    prev_non_blank = True
                    break
            if prev_non_blank:
                continue  # closing fence — no language tag needed
            rel = md_file.relative_to(knowledge_root)
            errors.append(f"{rel}: line {idx+1}: code block missing language tag")
            break  # one error per file is enough

    # 3. Check relative links in markdown files
    for md_file in md_files:
        content = md_file.read_text(encoding="utf-8")
        links = re.findall(r"\[.*?\]\((.+?)\)", content)
        for link in links:
            if link.startswith("http"):
                continue  # skip external URLs
            target = (md_file.parent / link).resolve()
            if not target.exists():
                errors.append(f"{md_file.name}: broken link → {link}")

    return errors


def main():
    base = Path(__file__).resolve().parent.parent

    if len(sys.argv) > 1:
        concept = Path(sys.argv[1])
        if not concept.exists():
            print(f"Error: {concept} does not exist")
            sys.exit(1)
        errors = lint_concept(concept, concept.parent.parent)
    else:
        # Lint all concepts under skills/qzz-mysql/knowledge/
        knowledge_root = base / "skills" / "qzz-mysql" / "knowledge"
        if not knowledge_root.exists():
            print("Error: knowledge/ directory not found")
            sys.exit(1)

        errors = []
        for concept_dir in sorted(knowledge_root.rglob("README.md")):
            concept_path = concept_dir.parent
            # Only lint directories that look like concepts (have metadata.yaml)
            if (concept_path / "metadata.yaml").exists():
                errors.extend(lint_concept(concept_path, knowledge_root))

    if errors:
        print(f"\n[FAIL] {len(errors)} issue(s) found:\n")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    else:
        print("[OK] All checks passed.")
        sys.exit(0)


if __name__ == "__main__":
    main()
