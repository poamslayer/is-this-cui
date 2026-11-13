#!/usr/bin/env python3
"""Check every SKILL.md's frontmatter against the Agent Skills spec.

Claude Code loads a skill whose frontmatter does not parse as YAML with no
fields set, so the description that decides when the skill runs is silently
gone. This parses each frontmatter strictly and holds it to the spec at
https://agentskills.io/specification: only the spec's fields, a name that
matches its folder, a description of 1 to 1024 characters, and metadata that
maps strings to strings.

    python3 scripts/check_frontmatter.py

Needs PyYAML and no network.
"""

from __future__ import annotations

import re
from pathlib import Path

import yaml

SKILLS_ROOT = Path("skills")
FIELDS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
NAME_PATTERN = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def problems_in(path: Path) -> list[str]:
    """Return what is wrong with one SKILL.md's frontmatter."""
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n") or "\n---\n" not in text[4:]:
        return ["no frontmatter between --- markers on the first lines"]
    block = text[4:].split("\n---\n", 1)[0]
    try:
        data = yaml.safe_load(block)
    except yaml.YAMLError as error:
        return [f"frontmatter is not valid YAML: {str(error).splitlines()[0]}"]
    if not isinstance(data, dict):
        return ["frontmatter is not a mapping"]

    problems = [f"field not in the spec: {key}" for key in sorted(set(data) - FIELDS)]
    name = data.get("name")
    if not isinstance(name, str) or not NAME_PATTERN.match(name) or len(name) > 64:
        problems.append(f"name {name!r} is not 1-64 lowercase letters, digits and single hyphens")
    elif name != path.parent.name:
        problems.append(f"name {name!r} does not match the folder {path.parent.name!r}")
    description = data.get("description")
    if not isinstance(description, str) or not 1 <= len(description) <= 1024:
        problems.append("description is not a string of 1-1024 characters")
    compatibility = data.get("compatibility")
    if compatibility is not None and (not isinstance(compatibility, str) or len(compatibility) > 500):
        problems.append("compatibility is not a string of at most 500 characters")
    metadata = data.get("metadata")
    if metadata is not None and not (
        isinstance(metadata, dict)
        and all(isinstance(k, str) and isinstance(v, str) for k, v in metadata.items())
    ):
        problems.append("metadata is not a map from strings to strings")
    return problems


def main() -> int:
    """Check every skill and report each problem."""
    paths = sorted(SKILLS_ROOT.glob("*/SKILL.md"))
    failed = 0
    for path in paths:
        problems = problems_in(path)
        failed += bool(problems)
        for problem in problems:
            print(f"FAIL {path}: {problem}")
    print(f"frontmatter: {len(paths)} skills, {failed} with problems")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
