# Final Demo Checklist

## Before Demo

Run these commands from the project folder:

```powershell
.\.venv\Scripts\Activate.ps1
python init_db.py
python -m unittest discover -s tests
flask --app app run --debug
```

Open:

```text
http://127.0.0.1:5000/
```

## Demo Steps

1. Show GitHub repository link.
2. Show project structure in VS Code.
3. Open `schema.sql` and explain the five tables.
4. Open `app/ai_agent.py` and explain AI agent v1.
5. Open the running app.
6. Search `wifi not connecting`.
7. Point out confidence score, matched terms, and escalation note.
8. Save the recommendation as an incident.
9. Open Incidents and then Details.
10. Add feedback as Helpful.
11. Open AI Activity dashboard.
12. Edit the incident status to Resolved.
13. Open Knowledge Base.
14. Add or edit one knowledge base solution.
15. Mention tests passed with `python -m unittest discover -s tests`.

## Short Speaking Script

For our final project, we completed the IT Incident Knowledge Assistant. It is a Flask and SQLite application that helps users search for common IT issues and receive troubleshooting recommendations. The app includes CRUD for incidents and knowledge base entries, an AI agent v1 that ranks solutions with confidence scores, feedback tracking, automated tests, and final documentation.
