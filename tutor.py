import asyncio
import os
import re
from contextlib import AsyncExitStack
from dataclasses import dataclass
from pathlib import Path

from agent_framework import Agent, AgentSession, tool
from agent_framework.foundry import FoundryChatClient
from azure.identity import AzureCliCredential
from dotenv import load_dotenv

from progress import TOTAL_STEPS, load_progress, save_progress

PROJECT_DIR = Path(__file__).resolve().parent
GUIDE_PATHS = {
    "ai": PROJECT_DIR / "AI-Agent-Learning-Guide.md",
    "python": PROJECT_DIR / "PYTHON-Learning-Guide.md",
}
PROGRESS_PATHS = {
    "ai": PROJECT_DIR / ".learning-progress.json",
    "python": PROJECT_DIR / ".python-learning-progress.json",
}


@dataclass(slots=True)
class ConsultationBudget:
    remaining: int = 1


@dataclass(slots=True)
class TutorPair:
    ai_agent: Agent
    python_agent: Agent
    ai_session: AgentSession
    python_session: AgentSession
    consultation_budget: ConsultationBudget


async def consult_peer(
    question: str,
    peer: Agent,
    session: AgentSession | None,
    peer_name: str,
    budget: ConsultationBudget,
) -> str:
    if session is None:
        raise RuntimeError(f"The {peer_name} tutor session is not initialized.")
    if budget.remaining <= 0:
        return (
            "A tutor has already been consulted for this reply. "
            "Continue with the information already available."
        )

    budget.remaining -= 1
    response = await peer.run(question, session=session)
    return f"Consultation from the {peer_name} tutor:\n{response.text}"


def read_guide(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError as error:
        raise FileNotFoundError(f"Learning guide not found at {path}.") from error


def get_topics(guide: str) -> list[str]:
    return re.findall(r"^## (\d+\. .+)$", guide, flags=re.MULTILINE)


def create_agents(ai_guide: str, python_guide: str) -> TutorPair:
    load_dotenv(PROJECT_DIR / ".env")
    load_dotenv(PROJECT_DIR.parent / "foundry_agent" / ".env")

    endpoint = os.getenv("FOUNDRY_PROJECT_ENDPOINT")
    model = os.getenv("FOUNDRY_MODEL")
    if not endpoint or not model:
        raise ValueError(
            "Set FOUNDRY_PROJECT_ENDPOINT and FOUNDRY_MODEL in the companion's "
            f"{PROJECT_DIR / '.env'}, the existing Foundry agent's "
            f"{PROJECT_DIR.parent / 'foundry_agent' / '.env'}, or your environment."
        )

    budget = ConsultationBudget()
    python_agent: Agent
    ai_agent: Agent
    python_session = None
    ai_session = None

    @tool
    async def consult_python_tutor(question: str) -> str:
        """Ask the Python tutor about Python syntax or programming basics."""
        return await consult_peer(question, python_agent, python_session, "Python")

    @tool
    async def consult_ai_tutor(question: str) -> str:
        """Ask the AI tutor about Microsoft Agent Framework concepts."""
        return await consult_peer(question, ai_agent, ai_session, "AI")

    ai_agent = Agent(
        client=FoundryChatClient(
            project_endpoint=endpoint,
            model=model,
            credential=AzureCliCredential(),
        ),
        name="AILearningTutor",
        instructions=f"""You are the AI and Microsoft Agent Framework tutor for a beginner.
Use the guide below as the source for framework-specific facts. Do not invent API
details, current package versions, or features. If it does not answer a framework
question, say so and point to a relevant official Microsoft Learn link in the guide.
Explain unfamiliar terms simply and teach one idea at a time. Offer small examples,
exercises, and kind, specific feedback. Clearly label teaching examples as examples.
You may consult the Python tutor when Python syntax or a programming-language concept
is central to the user's question. Use its result as supporting context, not as proof
of Microsoft framework behavior. When answering a consultation from the Python tutor,
do not ask the Python tutor to consult you again.

AI learning guide:
{ai_guide}""",
        tools=[consult_python_tutor],
    )
    python_agent = Agent(
        client=FoundryChatClient(
            project_endpoint=endpoint,
            model=model,
            credential=AzureCliCredential(),
        ),
        name="PythonLearningTutor",
        instructions=f"""You are a patient Python tutor for someone who is new to Python
and may also be new to programming. Explain from first principles, define unfamiliar
terms, and use short examples. Use the Python learning guide below and its official
Python documentation links as factual references. Do not invent Python syntax or
library behavior. If the guide does not settle a detail, say so and direct the learner
to the relevant official Python documentation. The official Python Tutorial assumes
basic programming knowledge; do not assume the learner already has it.
Offer small exercises and give specific, kind feedback. Clearly label teaching
examples as examples. You may consult the AI tutor for a Microsoft Agent Framework
connection, then explain the Python parts in simple terms. When answering a
consultation from the AI tutor, do not ask the AI tutor to consult you again.

Python learning guide:
{python_guide}""",
        tools=[consult_ai_tutor],
    )

    ai_session = ai_agent.create_session()
    python_session = python_agent.create_session()
    return TutorPair(
        ai_agent=ai_agent,
        python_agent=python_agent,
        ai_session=ai_session,
        python_session=python_session,
        consultation_budget=budget,
    )


def show_progress(
    subject: str, completed_steps: set[int], topics: list[str]
) -> None:
    print(f"{subject.upper()} learning progress:")
    for topic in topics:
        step = int(topic.split(".", maxsplit=1)[0])
        status = "done" if step in completed_steps else "not yet"
        print(f"  {topic} - {status}")
    print(f"{len(completed_steps)} of {len(topics)} steps complete.")


def handle_command(
    text: str,
    current_subject: str,
    completed_steps: dict[str, set[int]],
    topics: dict[str, list[str]],
) -> str:
    parts = text.split()
    command = parts[0].lower()
    arguments = parts[1:]

    if command == "/help":
        print(
            "Commands: /ai, /python, /topics [ai|python], "
            "/progress [ai|python], /done [ai|python] <step>, /help, /exit"
        )
    elif command in {"/ai", "/python"}:
        current_subject = command[1:]
        print(f"Switched to the {current_subject.upper()} tutor.")
    elif command == "/topics":
        subject = arguments[0].lower() if arguments else current_subject
        if subject not in topics:
            print("Choose a topic set with /topics ai or /topics python.")
            return current_subject
        for topic in topics[subject]:
            print(f"  {topic}")
    elif command == "/progress":
        subjects = arguments or list(topics)
        for subject in subjects:
            subject = subject.lower()
            if subject not in topics:
                print("Choose /progress ai or /progress python.")
                continue
            show_progress(subject, completed_steps[subject], topics[subject])
    elif command == "/done":
        subject = current_subject
        step_text = ""
        if len(arguments) == 1:
            step_text = arguments[0]
        elif len(arguments) == 2:
            subject, step_text = arguments[0].lower(), arguments[1]

        if subject not in topics:
            print("Use /done [ai|python] followed by a step number.")
            return current_subject
        try:
            step = int(step_text)
        except ValueError:
            print("Use /done [ai|python] followed by a step number.")
            return current_subject

        if not 1 <= step <= len(topics[subject]):
            print(f"Choose a step number from 1 to {len(topics[subject])}.")
            return current_subject

        completed_steps[subject].add(step)
        save_progress(PROGRESS_PATHS[subject], completed_steps[subject])
        print(f"Marked {subject.upper()} step {step} complete.")
    else:
        print("Unknown command. Type /help to see available commands.")
    return current_subject


async def main() -> None:
    guides = {subject: read_guide(path) for subject, path in GUIDE_PATHS.items()}
    topics = {subject: get_topics(guide) for subject, guide in guides.items()}
    for subject, subject_topics in topics.items():
        if len(subject_topics) != TOTAL_STEPS:
            raise ValueError(
                f"Expected {TOTAL_STEPS} numbered {subject} topics in "
                f"{GUIDE_PATHS[subject]}, found {len(subject_topics)}."
            )

    completed_steps = {
        subject: load_progress(PROGRESS_PATHS[subject]) for subject in guides
    }
    print("Learning Companion - choose /ai or /python, then ask a question.")
    print("The tutors can consult each other when a topic overlaps.")
    print("Type /help for commands; type /exit to quit.")

    tutors: TutorPair | None = None
    current_subject = "ai"
    async with AsyncExitStack() as stack:
        while True:
            try:
                user_input = input("\nYou: ").strip()
            except EOFError:
                print()
                break

            if not user_input:
                continue
            if user_input.lower() in {"/exit", "exit", "quit"}:
                break
            if user_input.startswith("/"):
                current_subject = handle_command(
                    user_input, current_subject, completed_steps, topics
                )
                continue

            if tutors is None:
                tutors = create_agents(guides["ai"], guides["python"])
                await stack.enter_async_context(tutors.ai_agent)
                await stack.enter_async_context(tutors.python_agent)

            tutors.consultation_budget.remaining = 1
            if current_subject == "ai":
                tutor = tutors.ai_agent
                session = tutors.ai_session
            else:
                tutor = tutors.python_agent
                session = tutors.python_session

            response = await tutor.run(user_input, session=session)
            print(f"\n{current_subject.upper()} tutor: {response.text}")


if __name__ == "__main__":
    asyncio.run(main())
