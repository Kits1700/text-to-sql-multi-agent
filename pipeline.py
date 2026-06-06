"""
pipeline.py — runs the full query from question to result.

Tries 3 times with the local model.
If all 3 fail, gives Claude one final shot.
If that also fails, logs it and returns the error.
"""

import os
import logging
from dotenv import load_dotenv

from schema_reader import get_schema
from router_agent import router_agent
from generator_agent import generator_agent
from sql_executor import run_sql

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

DATABASE_PATHS = {
    "department_management": "databases/department_management.sqlite",
    "concert_singer":        "databases/concert_singer.sqlite",
}

# Attempts 1-3 use the local model, attempt 4 uses Claude
ATTEMPT_PROVIDERS = ["ollama", "ollama", "ollama", "claude"]


def _run_attempt(question, schema, db_path, attempt_num, previous_error, previous_sql, provider):
    log.info("Attempt %d — %s", attempt_num, provider)
    sql    = generator_agent(question, schema, previous_error, previous_sql, provider=provider)
    result = run_sql(sql, db_path)

    if not result["success"]:
        log.warning("Attempt %d failed: %s", attempt_num, result["error"])

    rec = {
        "attempt":  attempt_num,
        "provider": provider,
        "sql":      sql,
        "success":  result["success"],
        "error":    result["error"],
    }
    if result["success"]:
        rec["columns"] = result["columns"]
        rec["data"]    = result["data"]

    return rec


def run_query(question: str) -> dict:
    db_name = router_agent(question, DATABASE_PATHS, provider="ollama")
    db_path = DATABASE_PATHS[db_name]
    schema  = get_schema(db_path)

    attempts      = []
    previous_error = None
    previous_sql   = None

    for attempt_num, provider in enumerate(ATTEMPT_PROVIDERS, start=1):
        rec = _run_attempt(question, schema, db_path, attempt_num, previous_error, previous_sql, provider)
        attempts.append(rec)

        if rec["success"]:
            return {
                "question":    question,
                "database":    db_name,
                "attempts":    attempts,
                "success":     True,
                "columns":     rec["columns"],
                "data":        rec["data"],
                "final_error": None,
            }

        previous_error = rec["error"]
        previous_sql   = rec["sql"]

    log.error("All attempts failed for: %r — %s", question, previous_error)

    return {
        "question":    question,
        "database":    db_name,
        "attempts":    attempts,
        "success":     False,
        "columns":     [],
        "data":        [],
        "final_error": previous_error,
    }
