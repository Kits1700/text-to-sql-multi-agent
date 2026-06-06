"""
generator_agent.py — writes a SQL query for the user's question.

Supports two models:
  - ollama  (local, used for attempts 1-3)
  - claude  (fallback, used for attempt 4)
"""

import os
import requests
import anthropic

OLLAMA_MODEL = "qwen2.5:1.5b"
OLLAMA_URL   = "http://localhost:11434/api/generate"


def generator_agent(question, schema, previous_error=None, previous_sql=None, provider="ollama"):
    prompt = _build_prompt(question, schema, previous_error, previous_sql)
    return _call_claude(prompt) if provider == "claude" else _call_ollama(prompt)


def _build_prompt(question, schema, previous_error, previous_sql):
    prompt = f"""You are a SQL expert. Write a SQLite query that answers the question below.

Rules:
- Return only the raw SQL, no explanation
- Use the exact table and column names from the schema

Schema:
{schema}

Question: {question}"""

    if previous_error:
        prompt += f"""

Your last query:
{previous_sql}

Failed with this error:
{previous_error}

Fix it and return the corrected SQL."""

    return prompt


def _call_ollama(prompt):
    res = requests.post(OLLAMA_URL, json={
        "model":  OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "temperature": 0
    }, timeout=60)
    res.raise_for_status()
    text = res.json()["response"].strip()

    # Strip markdown code fences if the model adds them
    if text.startswith("```"):
        text = "\n".join(
            line for line in text.splitlines()
            if not line.startswith("```")
        ).strip()

    return text


def _call_claude(prompt):
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    res = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}]
    )
    return res.content[0].text.strip()
