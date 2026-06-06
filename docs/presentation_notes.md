# Final Presentation Notes

## Slide 1: Project Title

IT Incident Knowledge Assistant

Team members: Dhruv Patel, Ruchitaben Patel, Nihar Parekh

## Slide 2: Problem

Many users face repeated IT problems such as login errors, Wi-Fi issues, password resets, software installation problems, and email syncing issues. These problems slow down users and create repeated work for IT support teams.

## Slide 3: Proposed Solution

Our app gives users a web interface where they can enter an IT issue and receive troubleshooting steps from a knowledge base. If the issue needs tracking, the user can save it as an incident.

## Slide 4: Technology Stack

- Python for backend logic
- Flask for routes and pages
- SQLite for database storage
- HTML/CSS for frontend
- GitHub for version control
- AI agent v1 for recommendation ranking
- Ollama/Llama for optional local LLM-generated responses

## Slide 5: Architecture

Browser -> Flask routes -> AI agent v1 -> SQLite database -> templates and results

Main database tables:

- categories
- knowledge_base
- incidents
- ai_recommendations
- feedback

## Slide 6: Week 2 and Week 3 Progress

Week 2 created the Flask skeleton, schema, seed data, and GitHub repo.

Week 3 added core CRUD and a working user flow for incident management and knowledge base management.

## Slide 7: AI Agent v1

The AI agent compares the user's issue against stored knowledge base entries. It ranks possible solutions using matched keywords, category hints, and issue wording. It then displays a confidence score, matched terms, and escalation guidance. If Ollama is running locally, the app sends the user issue and the matched knowledge base entry to a Llama model to generate a clearer troubleshooting response. If Ollama is unavailable, the app falls back to the local scoring agent.

## Slide 8: Testing and Refinement

We added automated tests using Python unittest. The tests check route loading, AI recommendations, incident CRUD, knowledge base CRUD, and feedback.

## Slide 9: Demo

Demo sequence:

1. Search for an issue.
2. Review the AI provider and recommendation.
3. Save it as an incident.
4. Open incident details.
5. Add feedback.
6. Show AI Activity.
7. Edit incident status.
8. Show knowledge base management.

## Slide 10: Conclusion

The project meets the planned six-week scope. It is not a full enterprise helpdesk system, but it successfully demonstrates a working Flask application with a database, CRUD operations, AI-style recommendations, feedback, testing, GitHub version control, and final demo materials.
