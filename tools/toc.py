#!/usr/bin/env python3
"""Generate table of contents for the MySQL knowledge base.

Scans knowledge/ directories and outputs a structured outline
of chapters and concepts.

Usage:
  python tools/toc.py                          # print TOC to stdout
  python tools/toc.py --check                  # check for orphaned dirs
  python tools/toc.py --output toc.md          # write to file
"""

import sys
from pathlib import Path


def scan_knowledge(knowledge_root: Path) -> list[dict]:
    """Scan knowledge/ and return list of chapter dicts."""
    chapters = []

    for chapter_dir in sorted(knowledge_root.iterdir()):
        if not chapter_dir.is_dir():
            continue

        chapter = {
            "name": chapter_dir.name,
            "concepts": [],
        }

        for concept_dir in sorted(chapter_dir.iterdir()):
            if not concept_dir.is_dir():
                continue
            readme = concept_dir / "README.md"
            if readme.exists():
                # Extract first heading as concept title
                content = readme.read_text(encoding="utf-8")
                first_line = content.strip().split("\n")[0]
                title = first_line.lstrip("#").strip()
                chapter["concepts"].append({
                    "dir": concept_dir.name,
                    "title": title,
                })

        if chapter["concepts"]:
            chapters.append(chapter)

    return chapters


def main():
    base = Path(__file__).resolve().parent.parent
    knowledge_root = base / "skills" / "qzz-mysql" / "knowledge"

    if not knowledge_root.exists():
        print("Error: knowledge/ directory not found")
        sys.exit(1)

    chapters = scan_knowledge(knowledge_root)

    total_concepts = sum(len(c["concepts"]) for c in chapters)
    output_lines = [
        f"# MySQL 知识库目录",
        f"",
        f"{len(chapters)} 章 · {total_concepts} 个概念",
        f"",
    ]

    for chapter in chapters:
        output_lines.append(f"## {chapter['name']}")
        for concept in chapter["concepts"]:
            path = f"knowledge/{chapter['name']}/{concept['dir']}/README.md"
            output_lines.append(f"- [{concept['title']}]({path})")
        output_lines.append("")

    if "--output" in sys.argv:
        idx = sys.argv.index("--output")
        if idx + 1 < len(sys.argv):
            out_path = Path(sys.argv[idx + 1])
            out_path.write_text("\n".join(output_lines), encoding="utf-8")
            print(f"[OK] Written to {out_path}")
            return

    print("\n".join(output_lines))


if __name__ == "__main__":
    main()
