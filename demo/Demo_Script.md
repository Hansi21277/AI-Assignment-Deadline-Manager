# 4-minute demo script — AI Assignment & Deadline Manager

**Important:** Record a real screen capture of the running local agent, not simulated output. Rehearse prompts with fresh task names or reset test data deliberately. Make terminal tool calls visible and readable.

## 00:00–00:30 — Introduction (Student 1)
"We developed an AI Assignment & Deadline Manager to help students track deadlines and distribute study time. The agent uses a local Ollama language model, Python tools, and a JSON data store. Unlike a simple chatbot, it calls tools and processes their results to complete tasks."

## 00:30–01:00 — Architecture (Student 2)
Show `agent.py`, `tools.py`, `README.md`, and `ollama list`. "The LLM selects a function, Python validates and executes it, the result is returned to the model, and the loop continues. Six tools are available. Tool calls and results are visible in the terminal and recorded in a log."

## 01:00–01:50 — Task 1: create and retrieve (Student 1)
Prompt: `Add a Database Systems assignment due 2026-10-28, high priority, estimated 5 hours. Then show pending assignments.`
Show `[TOOL CALL] add_assignment`, its result, then `list_assignments`. If re-recording after Oct 28, use a future date. Avoid duplicates by using a new title.

## 01:50–03:05 — Task 2: multi-step request (Student 2)
Prompt: `Check my deadlines for the next 7 days using the deadline checking tool, calculate my workload for 7 days, and create a 7-day study plan with 2 hours per day.`
Show calls to `check_deadlines`, `calculate_workload`, `create_study_plan`, their returned JSON, and the final schedule. Point out that earliest-deadline-first allocates hours before due dates. If a call uses incorrect arguments, retry after improving the prompt and explain the model's limitation.

## 03:05–03:35 — Error handling and update (Student 1)
Prompt: `Add Mathematics due 2026-15-50.` Show rejected date. Then prompt: `Mark assignment ID [ACTUAL ID] completed and list completed assignments.` Show both calls and results. Do not hardcode ID 1 unless it exists.

## 03:35–04:00 — Limitations and conclusion (Both)
"The system runs locally and saves tasks in JSON. It does not create real calendar bookings or send reminders. Tool selection depends on the local model, and conversation history lasts for one run. Our report describes tests, architecture, limitations, and actual individual contributions."

## Recording checklist
- Record at 1080p if possible, readable terminal font, minimal pauses.
- Verify `ollama list` and local model before recording.
- Show at least two complete tasks; one must clearly have multiple tool calls.
- Show a real error and the tool trace; do not edit traces to imply success.
- Save the finished 3–5 minute recording as `demo/Demo_Video.mp4` (or provide a working video link if allowed by your instructor).
