#!/usr/bin/env python3
"""Validate portable structure and YoToConn development requirements."""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n") or "\n---\n" not in text[4:]:
        raise ValueError("missing YAML frontmatter")
    block = text.split("\n---\n", 1)[0][4:]
    values = {}
    for line in block.splitlines():
        if line and not line.startswith(" ") and ":" in line:
            key, value = line.split(":", 1)
            values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def main() -> int:
    errors = []
    if not SKILLS.exists():
        print("No development skills present; repository structure is valid.")
        return 0
    for skill in sorted(path for path in SKILLS.iterdir() if path.is_dir()):
        manifest = skill / "SKILL.md"
        if not manifest.is_file():
            errors.append(f"{skill.name}: missing SKILL.md")
            continue
        try:
            metadata = frontmatter(manifest)
        except ValueError as exc:
            errors.append(f"{skill.name}: {exc}")
            continue
        if not NAME.fullmatch(skill.name) or len(skill.name) > 64:
            errors.append(f"{skill.name}: invalid directory name")
        if metadata.get("name") != skill.name:
            errors.append(f"{skill.name}: frontmatter name must match directory")
        if not metadata.get("description"):
            errors.append(f"{skill.name}: missing description")
        evals = skill / "evals" / "evals.json"
        if not evals.is_file():
            errors.append(f"{skill.name}: missing evals/evals.json")
        else:
            try:
                cases = json.loads(evals.read_text(encoding="utf-8")).get("cases", [])
                if len(cases) < 5:
                    errors.append(f"{skill.name}: at least five eval cases required")
            except (json.JSONDecodeError, AttributeError) as exc:
                errors.append(f"{skill.name}: invalid evals JSON: {exc}")
    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors))
        return 1
    print("All development skills passed structural validation.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
