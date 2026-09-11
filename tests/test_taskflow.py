import json
import tempfile
import unittest
from pathlib import Path

import taskflow


class TaskflowValidationTests(unittest.TestCase):
    def test_missing_dependency_raises(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "flow.json"
            path.write_text(
                json.dumps(
                    {
                        "tasks": {
                            "work": {
                                "action": "echo",
                                "depends_on": ["missing"],
                                "config": {"message": "x"},
                            }
                        }
                    }
                ),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "unknown task"):
                taskflow.load_flow(path)

    def test_cycle_raises(self) -> None:
        tasks = {
            "a": {"action": "echo", "depends_on": ["b"], "config": {"message": "a"}},
            "b": {"action": "echo", "depends_on": ["a"], "config": {"message": "b"}},
        }
        with self.assertRaisesRegex(ValueError, "cycle detected"):
            taskflow.topo_sort(tasks)

    def test_happy_path_order(self) -> None:
        tasks = {
            "prep": {"action": "echo", "config": {"message": "prep"}},
            "work": {"action": "add", "depends_on": ["prep"], "config": {"a": 1, "b": 2}},
        }
        self.assertEqual(taskflow.topo_sort(tasks), ["prep", "work"])


if __name__ == "__main__":
    unittest.main()
