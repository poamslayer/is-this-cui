#!/usr/bin/env python3
"""Check the is-this-cui state table.

Reads skills/is-this-cui/transitions.json through the skill's own
reducer, and fails when:

- a state cannot be reached from the start, or a path ends anywhere but an
  outcome or the holding status (an open end);
- a path breaks a guard in the table, such as reaching CUI without passing
  the authority state;
- a worked trace in scripts/is_this_cui_traces.json ends in a different status, or a trace that
  must be rejected is accepted;
- the state table in SKILL.md differs from the one the JSON produces.

Needs only Python 3 and no network.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "skills/is-this-cui"


def load_reducer():
    spec = importlib.util.spec_from_file_location("is_this_cui", SKILL / "is_this_cui.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def all_paths(m) -> list[list[tuple[str, str]]]:
    """Every path from the start to a stop, as (state, event) pairs plus the stop.

    `silence` resolves to whichever status the notice proposed, so the walk
    carries the reducer's state rather than reading `to` directly."""
    paths = []

    def walk(state, path):
        at = state["at"]
        if at in m.TABLE["outcomes"] or at not in m.TABLE["states"]:
            paths.append([*path, (at, None)])
            return
        for event in m.TABLE["states"][at]["on"]:
            walk(m.reduce(state, event), [*path, (at, event)])

    walk(m.initial(), [])
    return paths


def main() -> int:
    m = load_reducer()
    table = m.TABLE
    problems: list[str] = []

    for name, node in table["states"].items():
        for event, rule in node["on"].items():
            to = rule["to"]
            if to != "$proposed" and to not in table["states"] and to not in table["outcomes"]:
                problems.append(f"{name} --{event}--> {to}: not a state or an outcome")
            if to == "notice_open" and "proposed" not in rule:
                problems.append(f"{name} --{event}--> notice_open carries no proposed status")
            if "proposed" in rule and rule["proposed"] not in table["outcomes"]:
                problems.append(f"{name} --{event}: proposes {rule['proposed']!r}, not an outcome")

    paths = all_paths(m)
    reached = {state for path in paths for state, _ in path}
    for path in paths:
        stop = path[-1][0]
        if stop not in table["outcomes"]:
            route = " → ".join(str(s) for s, _ in path)
            problems.append(f"open end, the path stops at {stop!r}: {route}")
    for name in [*table["states"], *table["outcomes"]]:
        if name not in reached:
            problems.append(f"unreachable: {name}")

    for guard in table["guards"]:
        target = guard.get("outcome") or guard.get("state")
        for path in paths:
            for i, (state, _) in enumerate(path):
                if state == target and i and path[i - 1][0] not in guard["only_from"]:
                    route = " → ".join(f"{s}" for s, _ in path[: i + 1])
                    problems.append(f"guard broken, {target} reached from {path[i - 1][0]}: {route}")

    traces = json.loads((ROOT / "scripts/is_this_cui_traces.json").read_text())
    for trace in traces["traces"]:
        try:
            got = m.status(m.run(trace["events"]))
        except m.InvalidEvent as error:
            problems.append(f"trace rejected, {trace['item']}: {error}")
            continue
        if got != trace["status"]:
            problems.append(f"trace {trace['item']}: expected {trace['status']!r}, got {got!r}")
    for trace in traces["rejects"]:
        try:
            m.run(trace["events"])
            problems.append(f"accepted but must be rejected: {trace['item']}")
        except m.InvalidEvent:
            pass

    skill_text = (SKILL / "SKILL.md").read_text()
    if m.table_markdown() not in skill_text:
        problems.append("SKILL.md's state table differs from transitions.json; paste the output of is_this_cui.py --table")

    problems = list(dict.fromkeys(problems))
    for problem in problems:
        print(f"FAIL {problem}")
    print(f"is-this-cui: {len(paths)} paths, {len(traces['traces'])} traces, "
          f"{len(traces['rejects'])} rejects, {len(problems)} failures")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
