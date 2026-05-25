# IT Incident Knowledge Assistant

Week 3 Flask and SQLite prototype for an IT incident troubleshooting application.

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

## Project Structure

```text
app/
  __init__.py
  db.py
  routes.py
  static/
    styles.css
  templates/
    base.html
    index.html
    results.html
    incidents.html
    incident_form.html
    knowledge.html
    knowledge_form.html
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

## Week 3 Demo Flow

1. Open the home page.
2. Type an issue such as `wifi not connecting` or `account locked`.
3. Submit the issue and show matching troubleshooting steps.
4. Save one matching result as an incident.
5. Open the incidents page and edit the saved incident status, notes, or matched solution.
6. Create a manual incident from the New Incident page.
7. Open the Knowledge Base page, add a new solution, edit it, and delete it if needed.

## GitHub

Repository:

```text
https://github.com/Niharparekh13/IT-Incidient-Knowlege-Assistant
```
