# Final submission checklist — complete before LMS upload

- [ ] Replace BOTH student names, IDs, contribution placeholders and commit references in the PDF (regenerate PDF after editing source) and README. **Do not submit placeholders.**
- [ ] Both students have made genuine, identifiable Git commits and can explain the whole system.
- [ ] Confirm `ollama list` shows the locally downloaded model.
- [ ] Run `py -m unittest discover -s tests -v` (or venv Python) and retain output.
- [ ] Verify `agent.log` contains tool-call records and errors are handled.
- [ ] Run an explicit contextual follow-up to verify conversation history.
- [ ] Record a real 3–5 minute demo, including two complete tasks and visible tool traces; place video in `demo/`.
- [ ] Update README for any changes made to code or environment.
- [ ] Confirm `.gitignore` excludes `.venv/`, runtime `assignments.json`, `agent.log`, and `__pycache__/`.
- [ ] Create GitHub repository; push all source, README, PDF and demo; check links in a browser.
- [ ] Submit repository URL in LMS before the deadline.

## GitHub PowerShell commands (after creating empty repository)
```powershell
git init
git add .
git commit -m "Initial academic agent implementation"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/AI-Assignment-Deadline-Manager.git
git push -u origin main
```

Then invite the second student as collaborator. Each student should clone, modify, test and push their own commits; avoid fabricated contribution claims.

## Note
The included PDF is a well-developed draft with unfilled identity/contribution placeholders. The demo script is not a substitute for the actual video. This package is not a fully submitted repository until your group completes these steps.
