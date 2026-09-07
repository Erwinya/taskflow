#!/usr/bin/env python3
"""Load a task-flow JSON file, validate depends_on, and compute run order."""
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict, deque
from pathlib import Path
from typing import Any


def load_flow(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(data, dict):
        raise ValueError("flow root must be a JSON object")
    tasks = data.get("tasks")
    if not isinstance(tasks, dict) or not tasks:
        raise ValueError("flow.tasks must be a non-empty object")
    for name, spec in tasks.items():
        if not isinstance(spec, dict):
            raise ValueError(f"task '{name}' must be an object")
        deps = spec.get("depends_on", [])
        if not isinstance(deps, list):
            raise ValueError(f"task '{name}'.depends_on must be an array")
        for dep in deps:
            if dep not in tasks:
                raise ValueError(f"task '{name}' depends on unknown task '{dep}'")
    return data


def topo_sort(tasks: dict[str, dict[str, Any]]) -> list[str]:
    indegree = {name: 0 for name in tasks}
    graph: dict[str, list[str]] = defaultdict(list)
    for name, spec in tasks.items():
        for dep in spec.get("depends_on", []):
            graph[dep].append(name)
            indegree[name] += 1

    q = deque([n for n, d in indegree.items() if d == 0])
    order: list[str] = []
    while q:
        n = q.popleft()
        order.append(n)
        for nxt in graph[n]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                q.append(nxt)
    if len(order) != len(tasks):
        raise ValueError("cycle detected in task dependencies")
    return order


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Order tasks in a dependency-aware flow")
    parser.add_argument("--file", required=True, help="Flow JSON file")
    args = parser.parse_args(argv)

    path = Path(args.file)
    if not path.is_file():
        print(f"error: file not found: {path}", file=sys.stderr)
        return 2

    try:
        flow = load_flow(path)
        order = topo_sort(flow["tasks"])
    except (OSError, json.JSONDecodeError, ValueError) as ex:
        print(f"error: {ex}", file=sys.stderr)
        return 2

    print(f"ok tasks={len(order)} file={path}")
    print("order: " + " -> ".join(order))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
