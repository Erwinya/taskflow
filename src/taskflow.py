#!/usr/bin/env python3
"""Run a dependency-aware task flow with built-in actions."""
from __future__ import annotations

import argparse
import json
import sys
import time
from collections import defaultdict, deque
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable


@dataclass
class TaskResult:
    name: str
    ok: bool
    elapsed_ms: float
    output: str | None = None
    error: str | None = None


BUILTINS: dict[str, Callable[[dict[str, Any]], str]] = {
    "echo": lambda cfg: str(cfg.get("message", "")),
    "add": lambda cfg: str(int(cfg.get("a", 0)) + int(cfg.get("b", 0))),
    "sleep_ms": lambda cfg: (time.sleep(float(cfg.get("ms", 0)) / 1000.0) or "slept"),
}


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


def run_flow(flow: dict[str, Any]) -> list[TaskResult]:
    tasks = flow["tasks"]
    order = topo_sort(tasks)
    results: list[TaskResult] = []
    for name in order:
        spec = tasks[name]
        action = spec.get("action")
        if action not in BUILTINS:
            raise ValueError(f"unsupported action '{action}' in task '{name}'")
        started = time.perf_counter()
        try:
            output = BUILTINS[action](spec.get("config", {}) or {})
            elapsed = (time.perf_counter() - started) * 1000.0
            results.append(TaskResult(name, True, round(elapsed, 2), output=output))
        except Exception as ex:  # noqa: BLE001
            elapsed = (time.perf_counter() - started) * 1000.0
            results.append(TaskResult(name, False, round(elapsed, 2), error=str(ex)))
            break
    return results


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run a dependency-aware task flow")
    parser.add_argument("--file", required=True, help="Flow JSON file")
    args = parser.parse_args(argv)

    path = Path(args.file)
    if not path.is_file():
        print(f"error: file not found: {path}", file=sys.stderr)
        return 2

    try:
        flow = load_flow(path)
        results = run_flow(flow)
    except (OSError, json.JSONDecodeError, ValueError) as ex:
        print(f"error: {ex}", file=sys.stderr)
        return 2

    for r in results:
        flag = "OK" if r.ok else "FAIL"
        detail = r.error if r.error else r.output
        print(f"[{flag}] {r.name} {r.elapsed_ms}ms :: {detail}")
    return 0 if results and all(r.ok for r in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
