# IT Incident Knowledge Assistant

Final project report for COET-295 Emerging Technologies.

## Team Members

- Dhruv Patel
- Ruchitaben Patel
- Nihar Parekh

## Project Summary

The IT Incident Knowledge Assistant is a Flask web application that helps users find troubleshooting steps for common IT problems. Users can search for issues such as login failures, Wi-Fi problems, password resets, software installation errors, and email syncing issues. The system uses a SQLite knowledge base and an AI-style recommendation layer to suggest likely solutions before an issue is escalated.

## Problem Statement

Students, employees, and IT support teams often face repeated technical issues. Many of these issues are common, but users do not always know the correct troubleshooting steps. IT support staff may also spend time answering the same questions repeatedly. This project reduces repetitive troubleshooting work by giving users quick guidance and saving unresolved issues as incidents.

## Proposed Solution

The application provides a searchable IT knowledge base, incident tracking, and an AI recommendation flow. A user enters an issue, the app compares the issue against stored solutions, and the system returns ranked troubleshooting recommendations with confidence scores. If the user wants to track the issue, they can save it as an incident. Team members can manage the knowledge base and update incident statuses.

## Technology Stack

- Python: backend application logic
- Flask: web framework, routing, request handling, and templates
- SQLite: local database for categories, solutions, incidents, AI recommendations, and feedback
- HTML/CSS: user interface
- Git and GitHub: version control and collaboration
- AI agent v1: local keyword and confidence scoring for recommendation ranking
- Ollama/Llama: optional local LLM response generation when Ollama is running

## Scope

In scope:

- Simple web interface for entering IT issues
- Knowledge base for common problems and troubleshooting steps
- Incident CRUD operations
- Knowledge base CRUD operations
- AI recommendation v1 with confidence scores
- Feedback capture for AI recommendations
- Basic testing and final demo documentation

Out of scope:

- Enterprise helpdesk replacement
- Live chat with IT agents
- Real ServiceNow, Jira, or ticketing integration
- Automatic system repair
- Production authentication
- Sensitive personal data handling

## Architecture Sketch

```text
User Browser
    |
    v
Flask Web App
    |
    +--> Routes and Templates
    |
    +--> AI Agent v1
    |       |
    |       +--> Keyword scoring
    |       +--> Confidence calculation
    |       +--> Escalation hint
    |
    v
SQLite Database
    |
    +--> categories
    +--> knowledge_base
    +--> incidents
    +--> ai_recommendations
    +--> feedback
```

## MVC Project Organization

The final Flask code is organized using an MVC-style structure:

- Models in `app/models/`: database query and CRUD logic
- Views in `app/views/`: HTML templates and CSS
- Controllers in `app/controllers/`: Flask routes and request handling
- Services in `app/services/`: AI agent and Ollama integration

## Weekly Completion

Week 1: Proposal, architecture, technology plan, scope, and task breakdown were completed.

Week 2: Flask project skeleton, database schema, seed data, and GitHub repository were completed.

Week 3: Core CRUD and working user flow were added for incidents and knowledge base entries.

Week 4: AI agent v1 was added. The app now ranks knowledge base solutions, shows confidence scores, records AI recommendations, provides escalation guidance, and optionally uses Ollama with a local Llama model to generate clearer troubleshooting responses.

Week 5: Testing and refinement were added. The project includes a unittest suite that checks app routes, AI recommendations, incident CRUD, knowledge CRUD, and feedback flow.

Week 6: Final delivery materials were prepared, including this final report, presentation notes, and a demo checklist.

## Final Features

- Search IT issue and receive AI-ranked recommendations
- Optional Ollama/Llama generated troubleshooting text
- View confidence score and matched terms
- Save a recommendation as an incident
- View incident details and AI recommendation history
- Add helpful or not helpful feedback
- Create, read, update, and delete incidents
- Create, read, update, and delete knowledge base solutions
- View AI recommendation activity dashboard

## Database Tables

- `categories`: stores issue categories
- `knowledge_base`: stores known issues, symptoms, troubleshooting steps, and escalation flags
- `incidents`: stores user-submitted issues and statuses
- `ai_recommendations`: stores saved recommendation text and confidence scores
- `feedback`: stores user feedback about AI recommendation usefulness

## Testing

Run tests with:

```powershell
python -m unittest discover -s tests
```

The tests verify:

- Main pages load successfully
- AI agent returns relevant recommendations
- Ollama prompt generation includes the user issue and knowledge base match
- Search to incident to feedback flow works
- Knowledge base CRUD works
- Incident update and delete flow works

## GitHub Repository

```text
https://github.com/Niharparekh13/IT-Incidient-Knowlege-Assistant
```

## Final Demo Flow

1. Open the home page.
2. Search for `wifi not connecting`.
3. Show the AI provider, confidence score, and matched recommendation.
4. Save the recommendation as an incident.
5. Open the incident details page.
6. Add feedback saying the recommendation was helpful.
7. Open the AI Activity dashboard.
8. Show incident CRUD by editing the incident status.
9. Show knowledge base CRUD by adding or editing a troubleshooting entry.
