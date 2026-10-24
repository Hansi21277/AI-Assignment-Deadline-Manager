# AI Assignment & Deadline Manager

A **local, tool-using AI agent** that manages academic assignments and creates deadline-aware study plans. The core LLM runs through **Ollama**; no paid cloud LLM API is required.

## Requirements
- Python 3.11+ (tested interactively by the project group on Windows with Python 3.14 launcher; confirm package compatibility on your machine)
- Ollama with `qwen2.5:3b` downloaded
- Internet only for initial software/model downloads

## Quick start (Windows PowerShell)
```powershell
ollama pull qwen2.5:3b
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe agent.py
```
Open a terminal **inside the folder containing `agent.py` and `requirements.txt`**. If `ollama` is not recognized, install Ollama and restart the terminal. If Ollama is not running, launch its Windows app. Check with `ollama list`.

macOS/Linux:
```bash
ollama pull qwen2.5:3b
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python agent.py
```

## Three example prompts
1. `Add a Database Systems assignment due on 2026-10-28 with high priority and estimated work of 5 hours.`
2. `Check my deadlines for the next 7 days, calculate my workload for 7 days, and generate a study plan with 2 hours per day.`
3. `Mark my Database Systems assignment as completed, then show me all completed assignments.`

Dates in these examples are for the **2026-10-24 demonstration**; replace them with future dates when re-running later.

## Agent architecture
`Student prompt -> Ollama chat (qwen2.5:3b) -> tool-call decision -> Python tool -> JSON result -> Ollama follow-up -> response`. A single request can trigger multiple tools. The agent sends tool schemas to the model, executes returned calls, appends structured tool results to the conversation, and repeats for up to 10 rounds. Tool calls/results print to the console and are logged in `agent.log`.

## Available tools
| Tool | Purpose |
|---|---|
| `add_assignment` | Validate and save title, deadline, priority, hours |
| `list_assignments` | Retrieve all, pending, or completed tasks |
| `check_deadlines` | Find pending tasks due within a chosen window (including overdue) |
| `update_status` | Set pending/completed by assignment ID |
| `calculate_workload` | Count tasks and sum estimated hours in a deadline window |
| `create_study_plan` | Allocate daily hours using earliest-deadline-first scheduling |

## Data and logging
- `assignments.json`: created at runtime; local persistent single-user assignment store.
- `agent.log`: created at runtime; tool activity and exceptions.
- In-session `messages`: conversation history resets when the process exits.
- No automatic reminders or calendar integration.

## Run unit tests
```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```
The provided tests cover deterministic tool behavior; manual end-to-end traces are needed to verify the local LLM's tool selection.

## Demonstrated manual results (2026-10-24)
- Added Database Systems due 2026-10-28, high priority, 5 hours; tool returned `ok: true`.
- Retrieved the pending assignment.
- Corrected 7-day multi-step request called `check_deadlines(days=7)`, `calculate_workload(days=7)`, and `create_study_plan(days=7,daily_hours=2)`; allocated 2h, 2h, 1h on October 24–26.
- Invalid date `2026-15-50` returned `ok: false` and a month validation error.
- Updated assignment ID 1 to completed and retrieved it with `list_assignments(status="completed")`.

## Known limitations
Tool selection can vary across model runs (an earlier prompt produced `check_deadlines(days=1)` despite asking about seven days). Study sessions are computed, not booked. Work hours are estimates; the planner is greedy and does not account for existing appointments, breaks, or actual progress. JSON storage is not concurrency-safe. Logging may contain assignment text, so do not commit runtime data or logs.

## Group contribution record — fill in before submission
| Member | Actual code changes | Test/documentation work | Commit links |
|---|---|---|---|
| Student 1: [NAME / ID] | [VERIFY AND FILL] | [VERIFY AND FILL] | [LINKS] |
| Student 2: [NAME / ID] | [VERIFY AND FILL] | [VERIFY AND FILL] | [LINKS] |

Each student must genuinely review, modify, test and commit work under their own account. Do not claim work not performed.

## AI coding assistant disclosure
A ChatGPT-generated starter implementation and submission drafting assistance were used. The group must disclose this, explain human review/modifications, and verify all claims against the final code and demo. Do not submit the starter unchanged as original student work.

## Submission contents
Source files, README, `report/Technical_Report.pdf`, `demo/Demo_Script.md`, and a **group-recorded** 3–5-minute demo video. The video must be recorded separately and placed in `demo/` before the final Git push.
