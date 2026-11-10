# Learning Companion

A small command-line tutor built with the Microsoft Agent Framework Python SDK. It has two focused tutors:

- The AI tutor uses [`AI-Agent-Learning-Guide.md`](./AI-Agent-Learning-Guide.md).
- The Python tutor uses [`PYTHON-Learning-Guide.md`](./PYTHON-Learning-Guide.md), based on links to official Python documentation.

The tutors can consult each other on overlapping questions, such as explaining Python syntax in an agent example. Each answer allows at most one peer consultation to prevent recursive delegation. Neither tutor has tools that modify workspace files or external services; `/done` commands only update local progress files.

## Requirements

- Python 3.10 or later.
- A Microsoft Foundry project endpoint and a deployed model.
- Azure CLI sign-in with access to that project (`az login`).

The app sends your questions and the relevant learning guide to the configured model service. Do not enter confidential information. Model usage may incur charges according to your Foundry deployment; a peer consultation makes an additional model request.

## Set up on Windows

From this directory in PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

The app first reads `learning_companion\.env`, then falls back to the existing `foundry_agent\.env` for `FOUNDRY_PROJECT_ENDPOINT` and `FOUNDRY_MODEL`. Environment variables already set in your shell take precedence. If neither file has the settings, copy `.env.example` to `.env` and fill in the values for your existing Foundry project. Do not share or commit `.env`. No new Azure project or deployment is created. Sign in with `az login`, then start the tutor:

```powershell
python tutor.py
```

If PowerShell blocks virtual-environment activation, run the environment's Python directly instead:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe tutor.py
```

## Commands

- `/ai` — switch to the AI and Microsoft Agent Framework tutor.
- `/python` — switch to the Python tutor.
- `/topics` — show topics for the current tutor; `/topics ai` or `/topics python` selects one.
- `/progress` — show both tutors' progress; `/progress ai` or `/progress python` selects one.
- `/done 1` — mark step 1 for the current tutor complete.
- `/done ai 1` or `/done python 1` — mark a specific tutor's step complete.
- `/help` — show commands.
- `/exit` — quit.

AI and Python progress are stored separately in `.learning-progress.json` and `.python-learning-progress.json`. Conversation sessions last until you exit; marked progress remains for your next run.

The official Python Tutorial notes that it is intended for people who already know basic programming. The Python tutor is instructed to explain from first principles, but you can still ask it to slow down or define a term. For framework concepts and provider-specific details, follow the official links in the learning guides and the [Microsoft Agent Framework documentation](https://learn.microsoft.com/en-us/agent-framework/).
