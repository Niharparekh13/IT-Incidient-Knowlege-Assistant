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
4. Open `app/controllers/main_controller.py` and explain Flask routes.
5. Open `app/models/` and explain that database CRUD logic lives there.
6. Open `app/views/templates/` and explain these are the HTML views.
7. Open `app/services/ai_agent.py` and explain AI agent v1.
8. Open `app/services/ollama_client.py` and explain optional Ollama/Llama integration.
9. Open the running app.
10. Search `wifi not connecting`.
11. Point out AI provider, confidence score, matched terms, and escalation note.
12. Save the recommendation as an incident.
13. Open Incidents and then Details.
14. Add feedback as Helpful.
15. Open AI Activity dashboard.
16. Edit the incident status to Resolved.
17. Open Knowledge Base.
18. Add or edit one knowledge base solution.
19. Mention tests passed with `python -m unittest discover -s tests`.

## Optional Ollama Demo

If Ollama is installed, run:

```powershell
ollama pull llama3.2
```

Then keep Ollama running and start Flask. The search results should show:

```text
AI provider: Ollama (llama3.2)
```

If Ollama is not running, the app still works and shows:

```text
AI provider: Local scoring agent
```

## Short Speaking Script

For our final project, we completed the IT Incident Knowledge Assistant. It is a Flask and SQLite application that helps users search for common IT issues and receive troubleshooting recommendations. The app includes CRUD for incidents and knowledge base entries, an AI agent v1 that ranks solutions with confidence scores, optional Ollama/Llama generated responses, feedback tracking, automated tests, and final documentation.
