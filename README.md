# taskflow

Tiny dependency-aware task runner (DAG) with built-in actions: `echo`, `add`, and `sleep_ms`.

## Status

Flow loading, dependency ordering, cycle detection, and builtin execution are in place.  
JSON result reports and richer samples will land in follow-up commits.

## Run

```powershell
python src\taskflow.py --file samples\flow.json
```

## Builtins

| Action | Config | Result |
|--------|--------|--------|
| `echo` | `message` | prints/returns the message |
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

## Requirements

- Python 3.10+
- Standard library only

## License

MIT
