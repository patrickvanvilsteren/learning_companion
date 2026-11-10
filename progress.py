import json
from pathlib import Path

TOTAL_STEPS = 7


def load_progress(path: Path) -> set[int]:
    try:
        content = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return set()

    try:
        data = json.loads(content)
    except json.JSONDecodeError as error:
        raise ValueError(f"Progress file is not valid JSON: {path}") from error

    if not isinstance(data, dict):
        raise ValueError("Progress file must contain a JSON object.")

    completed_steps = data.get("completed_steps")
    if not isinstance(completed_steps, list):
        raise ValueError("Progress file must contain a completed_steps list.")

    if any(type(step) is not int or not 1 <= step <= TOTAL_STEPS for step in completed_steps):
        raise ValueError(f"Completed steps must be integers from 1 to {TOTAL_STEPS}.")

    return set(completed_steps)


def save_progress(path: Path, completed_steps: set[int]) -> None:
    if any(type(step) is not int or not 1 <= step <= TOTAL_STEPS for step in completed_steps):
        raise ValueError(f"Completed steps must be integers from 1 to {TOTAL_STEPS}.")

    path.write_text(
        json.dumps({"completed_steps": sorted(completed_steps)}, indent=2) + "\n",
        encoding="utf-8",
    )
