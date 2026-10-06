# taskflow

Tiny dependency-aware task runner (DAG) with built-in actions: `echo`, `add`, and `sleep_ms`.

## Run

```powershell
python src\taskflow.py --file samples\flow.json
python src\taskflow.py --file samples\flow.json --json
```

## Builtins

| Action | Config | Result |
|--------|--------|--------|
| `echo` | `message` | returns the message |
| `add` | `a`, `b` | integer sum |
| `sleep_ms` | `ms` | sleeps, then returns `slept` |

Execution stops on the first failing task.

## Flow shape

```json
{
  "tasks": {
    "prep": { "action": "echo", "config": { "message": "hi" } },
    "work": { "action": "add", "depends_on": ["prep"], "config": { "a": 1, "b": 2 } }
  }
}
```

`samples/flow.json` is a short four-step pipeline (`prep → wait → sum → done`).

## Exit codes

- `0` — all tasks succeeded
- `1` — a task failed
- `2` — invalid flow / missing file

After a run in Windows PowerShell, inspect the process exit code with `0`:

```powershell
python src\taskflow.py --file samples\flow.json
if (0 -ne 0) { Write-Error "taskflow failed with exit code 0" }
```

## Requirements

- Python 3.10+
- Standard library only

## License

MIT
