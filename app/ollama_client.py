import json
import os
import socket
import urllib.error
import urllib.parse
import urllib.request


DEFAULT_BASE_URL = "http://127.0.0.1:11434"
DEFAULT_MODEL = "llama3.2"
DEFAULT_TIMEOUT_SECONDS = 12
DEFAULT_MAX_ENHANCEMENTS = 1


def enhance_recommendation(issue, entry):
    """Ask a local Ollama model to write a concise troubleshooting response."""
    if not is_enabled():
        return None

    settings = get_settings()
    if not is_service_available(settings["base_url"]):
        return None

    payload = {
        "model": settings["model"],
        "prompt": build_prompt(issue, entry),
        "stream": False,
        "options": {
            "temperature": 0.2,
            "num_predict": 120,
        },
    }

    request = urllib.request.Request(
        f"{settings['base_url']}/api/generate",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=settings["timeout"]) as response:
            data = json.loads(response.read().decode("utf-8"))
    except (OSError, urllib.error.URLError, TimeoutError, json.JSONDecodeError):
        return None

    text = (data.get("response") or "").strip()
    if not text:
        return None

    return {
        "model": settings["model"],
        "provider": f"Ollama ({settings['model']})",
        "text": trim_response(text),
    }


def get_settings():
    return {
        "base_url": os.getenv("OLLAMA_BASE_URL", DEFAULT_BASE_URL).rstrip("/"),
        "model": os.getenv("OLLAMA_MODEL", DEFAULT_MODEL),
        "timeout": parse_float(
            os.getenv("OLLAMA_TIMEOUT_SECONDS"),
            DEFAULT_TIMEOUT_SECONDS,
        ),
        "max_enhancements": parse_int(
            os.getenv("OLLAMA_MAX_ENHANCEMENTS"),
            DEFAULT_MAX_ENHANCEMENTS,
        ),
    }


def is_enabled():
    return os.getenv("OLLAMA_ENABLED", "1").strip().lower() not in {
        "0",
        "false",
        "no",
        "off",
    }


def is_service_available(base_url, timeout=0.2):
    parsed_url = urllib.parse.urlparse(base_url)
    host = parsed_url.hostname
    port = parsed_url.port or (443 if parsed_url.scheme == "https" else 80)

    if not host:
        return False

    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False


def build_prompt(issue, entry):
    escalation_hint = (
        "Mention that escalation may be required."
        if entry["escalation_required"]
        else "Do not recommend escalation unless the steps fail."
    )
    return f"""
You are an IT helpdesk assistant. Use only the knowledge base information below.
Write a clear recommendation for the user's issue in 2 short paragraphs.
Do not invent company policies, phone numbers, private links, or sensitive information.
End with one short next step.

User issue:
{issue}

Knowledge base match:
Category: {entry["category_name"]}
Title: {entry["title"]}
Symptoms/keywords: {entry["symptoms"]}
Troubleshooting steps: {entry["resolution_steps"]}
Escalation rule: {escalation_hint}
""".strip()


def trim_response(text, max_length=900):
    clean = " ".join(text.split())
    if len(clean) <= max_length:
        return clean
    return clean[: max_length - 3].rstrip() + "..."


def parse_float(value, default):
    try:
        return float(value) if value is not None else default
    except ValueError:
        return default


def parse_int(value, default):
    try:
        return int(value) if value is not None else default
    except ValueError:
        return default
