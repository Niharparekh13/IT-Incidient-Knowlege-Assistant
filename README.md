# IT Incident Knowledge Assistant

Week 2 project skeleton for a Flask and SQLite web application.

## Week 2 Goals

- Set up a Flask application with organized routes, templates, and static files.
- Create a SQLite database schema for incident categories, knowledge base solutions, and user-submitted incidents.
- Seed the database with sample IT troubleshooting data.
- Show a basic working flow where a user enters an issue and the app returns possible fixes from the knowledge base.

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

## Demo Flow

1. Open the home page.
2. Type an issue such as `wifi not connecting` or `account locked`.
3. Submit the issue and show matching troubleshooting steps.
4. Open the incidents page to show stored user-submitted incidents.
5. Open the add knowledge page to show how the team can add future solutions.

## GitHub Setup Later

After the local project works, create a GitHub repository and push these files:

```powershell
git init
git add .
git commit -m "Add week 2 Flask project skeleton"
git branch -M main
git remote add origin YOUR_GITHUB_REPO_URL
git push -u origin main
```
