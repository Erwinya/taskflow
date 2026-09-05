# taskflow

Tiny dependency-aware task runner (DAG) with built-in actions such as `echo`, `add`, and `sleep_ms`.

## Status

Flow JSON loading and `depends_on` validation are in place. Topo-sort, builtins, and execution reports will land in follow-up commits.

## Run (current)

```powershell
python src\taskflow.py --file samples\flow.json
```

Validates that every `depends_on` entry refers to a known task name.

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
