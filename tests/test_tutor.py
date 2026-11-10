import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock, patch

from agent_framework import Agent, AgentSession

from tutor import (
    GUIDE_PATHS,
    ConsultationBudget,
    consult_peer,
    get_topics,
    handle_command,
    read_guide,
)


class TutorTests(unittest.TestCase):
    def test_guides_are_in_the_project(self) -> None:
        project_dir = Path(__file__).resolve().parent.parent
        for guide_path in GUIDE_PATHS.values():
            with self.subTest(guide_path=guide_path):
                self.assertEqual(guide_path.parent, project_dir)
                self.assertTrue(guide_path.is_file())

    def test_both_guides_have_seven_topics(self) -> None:
        for guide_path in GUIDE_PATHS.values():
            with self.subTest(guide_path=guide_path):
                self.assertEqual(len(get_topics(read_guide(guide_path))), 7)

    def test_python_guide_notes_tutorial_prerequisite(self) -> None:
        guide = read_guide(GUIDE_PATHS["python"])
        self.assertIn("new to programming", guide)
        self.assertIn("https://docs.python.org/3/tutorial/", guide)

    def test_subject_switch_changes_current_tutor(self) -> None:
        topics = {"ai": ["1. First"], "python": ["1. First"]}
        progress = {"ai": set(), "python": set()}
        self.assertEqual(handle_command("/python", "ai", progress, topics), "python")

    def test_done_command_saves_the_selected_subject(self) -> None:
        topics = {"ai": ["1. First"], "python": ["1. First"]}
        progress = {"ai": set(), "python": set()}

        with tempfile.TemporaryDirectory() as directory:
            ai_path = Path(directory) / "ai.json"
            python_path = Path(directory) / "python.json"
            with patch(
                "tutor.PROGRESS_PATHS",
                {"ai": ai_path, "python": python_path},
            ):
                handle_command("/done python 1", "ai", progress, topics)

            self.assertEqual(progress["python"], {1})
            self.assertEqual(progress["ai"], set())
            self.assertEqual(
                json.loads(python_path.read_text(encoding="utf-8")),
                {"completed_steps": [1]},
            )


class ConsultationTests(unittest.IsolatedAsyncioTestCase):
    async def test_only_one_peer_consultation_is_allowed_per_reply(self) -> None:
        peer = Mock(spec=Agent)
        peer.run = AsyncMock(return_value=SimpleNamespace(text="A helpful answer."))
        budget = ConsultationBudget()
        session = AgentSession()

        answer = await consult_peer("Explain this.", peer, session, "Python", budget)
        second_answer = await consult_peer(
            "Ask again.", peer, session, "Python", budget
        )

        self.assertIn("A helpful answer.", answer)
        self.assertIn("already been consulted", second_answer)
        peer.run.assert_awaited_once()


if __name__ == "__main__":
    unittest.main()
