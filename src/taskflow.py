#!/usr/bin/env python3
"""Load a task-flow JSON file and validate depends_on references."""
from __future__ import annotations

import argparse
import json
import sys
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


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate a task-flow JSON file")
    parser.add_argument("--file", required=True, help="Flow JSON file")
    args = parser.parse_args(argv)

    path = Path(args.file)
    if not path.is_file():
        print(f"error: file not found: {path}", file=sys.stderr)
        return 2

    try:
        flow = load_flow(path)
    except (OSError, json.JSONDecodeError, ValueError) as ex:
        print(f"error: {ex}", file=sys.stderr)
        return 2

    tasks = flow["tasks"]
    print(f"ok tasks={len(tasks)} file={path}")
    for name, spec in tasks.items():
        deps = spec.get("depends_on", [])
        dep_txt = ",".join(deps) if deps else "-"
        print(f"  {name} depends_on=[{dep_txt}]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
