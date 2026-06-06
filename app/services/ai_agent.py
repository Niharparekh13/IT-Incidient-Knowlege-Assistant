import re

from .ollama_client import enhance_recommendation, generate_general_guidance, get_settings


STOP_WORDS = {
    "a",
    "an",
    "and",
    "are",
    "can",
    "for",
    "from",
    "have",
    "how",
    "i",
    "in",
    "is",
    "it",
    "my",
    "not",
    "of",
    "on",
    "or",
    "problem",
    "issue",
    "the",
    "to",
    "working",
    "with",
}

CATEGORY_HINTS = {
    "login and account access": {
        "account",
        "auth",
        "authentication",
        "locked",
        "login",
        "mfa",
        "password",
        "reset",
        "signin",
    },
    "network and wi-fi": {
        "connect",
        "internet",
        "network",
        "router",
        "wifi",
        "wi-fi",
        "wireless",
    },
    "software installation": {
        "admin",
        "install",
        "installer",
        "permission",
        "software",
        "update",
    },
    "email and communication": {
        "email",
        "mail",
        "message",
        "outlook",
        "sync",
        "teams",
    },
    "device and hardware": {
        "device",
        "display",
        "hardware",
        "laptop",
        "printer",
        "screen",
    },
}

ESCALATION_TERMS = {
    "breach",
    "critical",
    "everyone",
    "outage",
    "security",
    "urgent",
}


def recommend_solutions(db, issue, category_id=None, limit=5):
    """Return ranked knowledge base matches with a simple AI-style confidence score."""
    issue_tokens = tokenize(issue)
    entries = fetch_knowledge_entries(db, category_id)
    ranked = []

    for entry in entries:
        title_tokens = tokenize(entry["title"])
        symptom_tokens = tokenize(entry["symptoms"])
        resolution_tokens = tokenize(entry["resolution_steps"])
        category_tokens = tokenize(entry["category_name"])
        hint_tokens = CATEGORY_HINTS.get(entry["category_name"].lower(), set())

        title_matches = issue_tokens & title_tokens
        symptom_matches = issue_tokens & symptom_tokens
        resolution_matches = issue_tokens & resolution_tokens
        category_matches = issue_tokens & (category_tokens | hint_tokens)
        matched_terms = sorted(
            title_matches | symptom_matches | resolution_matches | category_matches
        )

        score = (
            len(title_matches) * 3.0
            + len(symptom_matches) * 2.5
            + len(resolution_matches) * 1.2
            + len(category_matches) * 1.8
        )

        if category_id and str(entry["category_id"]) == str(category_id):
            score += 1.0

        phrase_bonus = phrase_score(issue, entry)
        score += phrase_bonus

        if score <= 0:
            continue

        confidence = confidence_from_score(score, len(issue_tokens))
        if confidence < 0.4:
            continue

        recommendation = dict(entry)
        recommendation["confidence_score"] = confidence
        recommendation["confidence_percent"] = int(round(confidence * 100))
        recommendation["matched_terms"] = ", ".join(matched_terms[:8])
        recommendation["ai_summary"] = build_recommendation_text(
            issue,
            entry,
            confidence,
            matched_terms,
        )
        recommendation["ai_provider"] = "Local scoring agent"
        recommendation["saved_ai_summary"] = (
            f"{recommendation['ai_provider']}: {recommendation['ai_summary']}"
        )
        ranked.append(recommendation)

    ranked.sort(
        key=lambda item: (
            item["confidence_score"],
            item["escalation_required"],
            item["title"].lower(),
        ),
        reverse=True,
    )
    recommendations = ranked[:limit]
    enhance_with_ollama(issue, recommendations)
    return recommendations


def enhance_with_ollama(issue, recommendations):
    max_enhancements = get_settings()["max_enhancements"]
    for recommendation in recommendations[:max_enhancements]:
        llm_response = enhance_recommendation(issue, recommendation)
        if not llm_response:
            continue

        recommendation["ai_summary"] = llm_response["text"]
        recommendation["ai_provider"] = llm_response["provider"]
        recommendation["saved_ai_summary"] = (
            f"{llm_response['provider']}: {llm_response['text']}"
        )


def build_escalation_message(issue, has_matches):
    issue_tokens = tokenize(issue)
    if issue_tokens & ESCALATION_TERMS:
        return "The issue includes urgent or security-related language, so escalation should be considered."
    if not has_matches:
        return "No strong knowledge base match was found, so the issue should be saved for team review."
    return "Review the suggested steps first, then escalate if the issue continues."


def build_general_ai_guidance(issue):
    llm_response = generate_general_guidance(issue)
    if llm_response:
        return {
            "provider": llm_response["provider"],
            "text": llm_response["text"],
            "saved_text": f"{llm_response['provider']}: {llm_response['text']}",
        }

    text = (
        "No matching knowledge base solution was found. Try basic troubleshooting: "
        "restart the device, check related settings or cables, confirm the device is updated, "
        "test with another app or device if possible, and save an incident if the issue continues."
    )
    return {
        "provider": "Local fallback guidance",
        "text": text,
        "saved_text": f"Local fallback guidance: {text}",
    }


def fetch_knowledge_entries(db, category_id=None):
    params = []
    where_clause = ""

    if category_id:
        where_clause = "WHERE kb.category_id = ?"
        params.append(category_id)

    return db.execute(
        f"""
        SELECT kb.*, c.name AS category_name
        FROM knowledge_base kb
        JOIN categories c ON c.id = kb.category_id
        {where_clause}
        ORDER BY c.name, kb.title
        """,
        params,
    ).fetchall()


def tokenize(text):
    normalized = text.lower().replace("wi-fi", "wifi")
    return {
        token
        for token in re.findall(r"[a-z0-9]+", normalized)
        if len(token) > 2 and token not in STOP_WORDS
    }


def phrase_score(issue, entry):
    issue_text = issue.lower().replace("wi-fi", "wifi")
    score = 0.0
    for field, weight in (
        ("title", 2.0),
        ("symptoms", 1.5),
        ("resolution_steps", 0.5),
    ):
        value = entry[field].lower().replace("wi-fi", "wifi")
        for token in tokenize(issue_text):
            if token in value:
                score += weight / 3
    return min(score, 3.0)


def confidence_from_score(score, token_count):
    if token_count <= 0:
        return 0.0
    normalized = score / max(token_count * 3.5, 1)
    return min(0.97, max(0.35, normalized))


def build_recommendation_text(issue, entry, confidence, matched_terms):
    percent = int(round(confidence * 100))
    terms = ", ".join(matched_terms[:5]) if matched_terms else "general issue language"
    escalation = " Escalation may be needed." if entry["escalation_required"] else ""
    return (
        f"AI v1 matched this issue to '{entry['title']}' with {percent}% confidence "
        f"using terms like {terms}.{escalation}"
    )
