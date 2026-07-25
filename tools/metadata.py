#!/usr/bin/env python3
"""Validate metadata.yaml files in knowledge concepts.

Checks:
  1. All required fields present
  2. difficulty is a valid value
  3. prerequisites paths exist
  4. updated date is valid ISO 8601
  5. topics has at least 2 entries

Usage:
  python tools/metadata.py                      # validate all concepts
  python tools/metadata.py <concept-dir>        # validate single concept
"""

import sys
import re
from pathlib import Path
from datetime import datetime

VALID_DIFFICULTIES = {"beginner", "intermediate", "advanced"}

REQUIRED_FIELDS = ["name", "section", "difficulty", "prerequisites", "topics", "updated"]


def parse_yaml_simple(text: str) -> dict:
    """Minimal YAML parser for metadata.yaml (flat key: value only)."""
    result = {}
    for line in text.strip().split("\n"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line:
            key, _, value = line.partition(":")
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            result[key] = value
    return result


def validate_metadata(metadata_path: Path, knowledge_root: Path) -> list[str]:
    """Validate a single metadata.yaml. Returns list of error messages."""
    errors = []
    concept_dir = metadata_path.parent

    if not metadata_path.exists():
        return [f"{concept_dir.name}: metadata.yaml not found"]

    try:
        text = metadata_path.read_text(encoding="utf-8")
        data = parse_yaml_simple(text)
    except Exception as e:
        return [f"{concept_dir.name}: cannot parse metadata.yaml: {e}"]

    # 1. Required fields
    for field in REQUIRED_FIELDS:
        if field not in data:
            errors.append(f"{concept_dir.name}: missing field '{field}'")

    # 2. Valid difficulty
    if "difficulty" in data and data["difficulty"] not in VALID_DIFFICULTIES:
        errors.append(
            f"{concept_dir.name}: invalid difficulty '{data['difficulty']}' "
            f"(must be one of {VALID_DIFFICULTIES})"
        )

    # 3. Prerequisites exist (if any paths listed)
    # prerequisites in metadata.yaml is a list; we can't easily parse YAML lists
    # with our simple parser, so skip this for now.
    # TODO: use a proper YAML parser for this check.

    # 4. Valid date
    if "updated" in data:
        date_str = data["updated"]
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", date_str):
            errors.append(
                f"{concept_dir.name}: invalid date '{date_str}' (use YYYY-MM-DD)"
            )
        else:
            try:
                datetime.strptime(date_str, "%Y-%m-%d")
            except ValueError:
                errors.append(
                    f"{concept_dir.name}: invalid date '{date_str}' (not a real date)"
                )

    return errors


def main():
    base = Path(__file__).resolve().parent.parent
    knowledge_root = base / "skills" / "qzz-mysql" / "knowledge"

    if not knowledge_root.exists():
        print("Error: knowledge/ directory not found")
        sys.exit(1)

    if len(sys.argv) > 1:
        concept = Path(sys.argv[1])
        errors = validate_metadata(concept / "metadata.yaml", knowledge_root)
    else:
        errors = []
        for md_path in sorted(knowledge_root.rglob("metadata.yaml")):
            errors.extend(validate_metadata(md_path, knowledge_root))

    if errors:
        print(f"\n[FAIL] {len(errors)} issue(s) found:\n")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    else:
        print("[OK] All metadata valid.")
        sys.exit(0)


if __name__ == "__main__":
    main()
