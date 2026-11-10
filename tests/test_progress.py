import json
import tempfile
import unittest
from pathlib import Path

from progress import load_progress, save_progress


class ProgressTests(unittest.TestCase):
    def test_missing_progress_starts_empty(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            self.assertEqual(load_progress(Path(directory) / "progress.json"), set())

    def test_save_and_load_progress(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "progress.json"
            save_progress(path, {1, 3})
            self.assertEqual(load_progress(path), {1, 3})

    def test_invalid_step_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "progress.json"
            path.write_text(json.dumps({"completed_steps": [8]}), encoding="utf-8")
            with self.assertRaises(ValueError):
                load_progress(path)

    def test_corrupt_progress_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "progress.json"
            path.write_text("{", encoding="utf-8")
            with self.assertRaises(ValueError):
                load_progress(path)


if __name__ == "__main__":
    unittest.main()
