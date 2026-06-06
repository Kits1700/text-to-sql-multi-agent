"""
router_agent.py — picks which database the question is about.

Reads the schema of every available database and asks the model
to choose the best match. Supports ollama (local) and claude.
"""

import os
import requests
import anthropic
from schema_reader import get_schema

OLLAMA_MODEL = "qwen2.5:1.5b"
OLLAMA_URL   = "http://localhost:11434/api/generate"


def router_agent(question, database_paths, provider="ollama"):
    # Build a combined description of all databases
    all_schemas = ""
    for db_name, db_path in database_paths.items():
        all_schemas += f"=== {db_name} ===\n{get_schema(db_path)}\n"

    valid_names = list(database_paths.keys())

    prompt = f"""You are a routing assistant. Pick which database can answer the question.

Available databases:
{all_schemas}

Rules:
- Reply with only the database name, nothing else
- Must be one of: {valid_names}

Question: {question}"""

    chosen = _call_claude(prompt) if provider == "claude" else _call_ollama(prompt)
    chosen = chosen.strip().rstrip(".")

    # Fall back to the first database if the model returns something unexpected
    return chosen if chosen in database_paths else valid_names[0]


def _call_ollama(prompt):
    res = requests.post(OLLAMA_URL, json={
        "model":  OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
    }, timeout=30)
    res.raise_for_status()
    return res.json()["response"].strip()


def _call_claude(prompt):
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    res = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=50,
        messages=[{"role": "user", "content": prompt}]
    )
    return res.content[0].text.strip()
