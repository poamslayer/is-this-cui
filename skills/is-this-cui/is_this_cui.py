#!/usr/bin/env python3
"""Run one item through the is-this-cui state table.

The table is transitions.json, next to this file. `reduce` is a pure function:
it takes a state and one event and returns the next state, or raises
InvalidEvent when the event does not fit the state. The agent chooses each
event; this script keeps the order and writes the path.

    python3 is_this_cui.py nonpublic gov clue propose_fci silence
    python3 is_this_cui.py --json nonpublic reuse reuses marked yes
    python3 is_this_cui.py --table
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

TABLE = json.loads((Path(__file__).parent / "transitions.json").read_text())


class InvalidEvent(ValueError):
    pass


def initial() -> dict:
    return {"at": TABLE["start"], "proposed": None, "trail": []}


def status(state: dict) -> str:
    """What to record for the item now: an outcome, the holding status, or 'undecided'."""
    at = state["at"]
    if at in TABLE["outcomes"]:
        return at
    return TABLE["holding"].get(at, "undecided")


def allowed(state: dict) -> list[str]:
    at = state["at"]
    if at in TABLE["outcomes"]:
        return [TABLE["reopen"]["event"]]
    return list(TABLE["states"][at]["on"])


def reduce(state: dict, event: str) -> dict:
    at = state["at"]
    if at in TABLE["outcomes"]:
        if event != TABLE["reopen"]["event"]:
            raise InvalidEvent(f"{at!r} is an outcome; only {TABLE['reopen']['event']!r} applies")
        step = {"from": at, "event": event, "to": TABLE["start"],
                "why": TABLE["reopen"]["why"], "cite": TABLE["reopen"]["cite"]}
        return {"at": TABLE["start"], "proposed": None, "trail": [*state["trail"], step]}
    rule = TABLE["states"][at]["on"].get(event)
    if rule is None:
        raise InvalidEvent(f"{event!r} does not answer {at!r}; expected one of {allowed(state)}")
    to = state["proposed"] if rule["to"] == "$proposed" else rule["to"]
    proposed = rule.get("proposed", state["proposed"] if to in TABLE["states"] else None)
    step = {"from": at, "event": event, "to": to, "why": rule["why"], "cite": rule["cite"]}
    return {"at": to, "proposed": proposed, "trail": [*state["trail"], step]}


def run(events: list[str]) -> dict:
    state = initial()
    for event in events:
        state = reduce(state, event)
    return state


def table_markdown() -> str:
    """The state table exactly as SKILL.md must show it."""
    rows = ["| State | Question | Event → next |", "|---|---|---|"]
    for name, node in TABLE["states"].items():
        moves = []
        for event, rule in node["on"].items():
            to = "the proposed status" if rule["to"] == "$proposed" else rule["to"]
            to = f"`{to}`" if to in TABLE["states"] else f"**{to}**"
            moves.append(f"`{event}` → {to}")
        rows.append(f"| `{name}` | {node['question']} | {'. '.join(moves)} |")
    return "\n".join(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("events", nargs="*", help="events in order, starting from the first state")
    parser.add_argument("--json", action="store_true", help="print the final state as JSON")
    parser.add_argument("--table", action="store_true", help="print the state table as SKILL.md shows it")
    args = parser.parse_args()
    if args.table:
        print(table_markdown())
        return 0
    try:
        state = run(args.events)
    except InvalidEvent as error:
        print(f"invalid: {error}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps({**state, "status": status(state), "next": allowed(state)}, indent=2))
        return 0
    for step in state["trail"]:
        cite = f" ({step['cite']})" if step["cite"] else ""
        print(f"{step['from']} --{step['event']}--> {step['to']}: {step['why']}{cite}")
    print(f"status: {status(state)}")
    if state["at"] in TABLE["states"]:
        print(f"next: {TABLE['states'][state['at']]['question']} {allowed(state)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
