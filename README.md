# taskflow

Tiny dependency-aware task runner (DAG) with built-in actions such as `echo`, `add`, and `sleep_ms`.

## Status

Flow loading, `depends_on` validation, topological ordering, and cycle detection are in place.  
Builtin execution and result reports will land in follow-up commits.

## Run (current)

```powershell
python src\taskflow.py --file samples\flow.json
```

Prints a valid run order, or exits with an error if a dependency is missing or a cycle exists.

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
