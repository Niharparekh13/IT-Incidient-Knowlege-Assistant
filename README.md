# IT Incident Knowledge Assistant

Final Flask and SQLite prototype for an IT incident troubleshooting application.

## Completed Milestones

### Week 2

- Set up a Flask application with organized routes, templates, and static files.
- Created a SQLite database schema for incident categories, knowledge base solutions, and user-submitted incidents.
- Seeded the database with sample IT troubleshooting data.
- Built a basic flow where a user enters an issue and the app returns possible fixes from the knowledge base.

### Week 3

- Added core CRUD for knowledge base solutions.
- Added core CRUD for user-submitted incidents.
- Added manual incident creation, incident editing, status updates, and delete actions.
- Added a knowledge base management page with edit and delete controls.
- Improved the working user flow from issue search to saved incident to incident status update.

### Week 4

- Added AI agent v1 for local recommendation ranking.
- Added confidence scores, matched terms, and escalation guidance.
- Stored AI recommendations when incidents are created from search results.
- Added an AI Activity dashboard.

### Week 5

- Added feedback capture for AI recommendations.
- Added automated tests using Python `unittest`.
- Refined incident deletion and knowledge deletion so related AI records stay consistent.

### Week 6

- Added final report, presentation notes, and demo checklist in the `docs/` folder.
- Prepared a final demo flow covering search, AI, CRUD, feedback, and tests.

## Project Structure

```text
app/
  __init__.py
  ai_agent.py
  db.py
  routes.py
  static/
    styles.css
  templates/
    base.html
    index.html
    results.html
    incidents.html
    incident_detail.html
    incident_form.html
    ai_dashboard.html
    knowledge.html
    knowledge_form.html
docs/
  final_report.md
  presentation_notes.md
  demo_checklist.md
tests/
  test_app.py
schema.sql
seed.sql
init_db.py
requirements.txt
```

## Local Setup

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Initialize the database:

```powershell
python init_db.py
```

Run the app:

```powershell
flask --app app run --debug
```

Open the local URL shown in the terminal, usually:

```text
http://127.0.0.1:5000
```

Run tests:

```powershell
python -m unittest discover -s tests
```

## Final Demo Flow

1. Open the home page.
2. Type an issue such as `wifi not connecting` or `account locked`.
3. Submit the issue and show AI-ranked troubleshooting recommendations.
4. Point out the confidence score, matched terms, and escalation guidance.
5. Save one matching result as an incident.
6. Open the incident details page and show the stored AI recommendation.
7. Add helpful or not helpful feedback.
8. Open the AI Activity page.
9. Edit the saved incident status, notes, or matched solution.
10. Open the Knowledge Base page, add a new solution, edit it, and delete it if needed.

## Final Documentation

- `docs/final_report.md`
- `docs/presentation_notes.md`
- `docs/demo_checklist.md`

## GitHub

Repository:

```text
https://github.com/Niharparekh13/IT-Incidient-Knowlege-Assistant
```
