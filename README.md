# taskflow

Tiny dependency-aware task runner (DAG) with built-in actions such as `echo`, `add`, and `sleep_ms`.

## Status

Project scaffolding is in place. Flow loading, topo-sort, builtins, and sample flows will land in follow-up commits.

## Goals

- Load a JSON flow of named tasks and `depends_on` edges
- Detect missing dependencies and cycles
- Run tasks in topological order
- Emit a clear text or JSON result report

## Requirements

- Python 3.10+
- Standard library only

## License

MIT
