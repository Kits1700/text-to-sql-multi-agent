"""
test_script.py — runs all 10 evaluation test cases and optionally saves a markdown report.

Usage:
    python test_script.py              # prints to console
    python test_script.py --save-log   # also writes evaluation_log.md
"""

import sys
from pipeline import run_query

TEST_CASES = [
    (1,  "EN", "How many heads of departments are older than 56?"),
    (2,  "CS", "Kolik vedoucích oddělení je starších než 56 let?"),
    (3,  "EN", "List the creation year, name, and budget of each department."),
    (4,  "CS", "Vypiš rok založení, název a rozpočet každého oddělení."),
    (5,  "EN", "Show the name and head ID of the heads who are managing a department."),
    (6,  "CS", "Ukaž jméno a ID vedoucího (head ID) u těch vedoucích, kteří aktuálně řídí nějaké oddělení."),
    (7,  "EN", "What is the total capacity of all stadiums combined?"),
    (8,  "CS", "Jaká je celková kapacita všech stadionů dohromady?"),
    (9,  "EN", "Show the names of singers and the themes of concerts they sang in."),
    (10, "CS", "Ukaž jména zpěváků a témata koncertů, na kterých zpívali."),
]

PROVIDER_LABEL = {
    "ollama": "Local (Ollama)",
    "claude": "Claude API",
}


def run_tests():
    passed  = 0
    failed  = 0
    results = []   # collected for the markdown log

    for num, lang, question in TEST_CASES:
        divider = "-" * 60
        print(f"\n{divider}")
        print(f"Test {num} [{lang}]")
        print(f"Question : {question}")

        result = run_query(question)

        print(f"Database : {result['database']}")
        print(f"Attempts :")

        for a in result["attempts"]:
            label    = PROVIDER_LABEL.get(a["provider"], a["provider"])
            outcome  = "OK  " if a["success"] else "FAIL"
            print(f"  [{a['attempt']}] {label} — {outcome}")
            print(f"       SQL   : {a['sql']}")
            if not a["success"]:
                print(f"       Error : {a['error']}")

        if result["success"]:
            print(f"Result   : {result['columns']}")
            for row in result["data"]:
                print(f"           {list(row)}")
            passed += 1
        else:
            print(f"Result   : FAILED after {len(result['attempts'])} attempts")
            print(f"           Last error: {result['final_error']}")
            failed += 1

        results.append((num, lang, question, result))

    print(f"\n{'=' * 60}")
    print(f"Summary : {passed} passed / {failed} failed out of {len(TEST_CASES)} tests")
    print(f"{'=' * 60}")

    return results, passed, failed


def save_markdown_log(results, passed, failed):
    lines = []
    lines.append("# Evaluation Log\n")
    lines.append(f"**{passed} passed / {failed} failed out of {len(TEST_CASES)} tests**\n")

    for num, lang, question, result in results:
        status = "PASS" if result["success"] else "FAIL"
        lines.append(f"---\n")
        lines.append(f"## Test {num} [{lang}] — {status}\n")
        lines.append(f"**Question:** {question}  \n")
        lines.append(f"**Database:** {result['database']}  \n\n")
        lines.append(f"### Attempts\n")

        for a in result["attempts"]:
            label   = PROVIDER_LABEL.get(a["provider"], a["provider"])
            outcome = "✓ OK" if a["success"] else "✗ FAIL"
            lines.append(f"**Attempt {a['attempt']} — {label} — {outcome}**\n")
            lines.append(f"```sql\n{a['sql']}\n```\n")
            if not a["success"] and a["error"]:
                lines.append(f"> Error: `{a['error']}`\n\n")

        if result["success"]:
            lines.append(f"### Result\n")
            lines.append(f"Columns: {result['columns']}  \n")
            for row in result["data"]:
                lines.append(f"- {list(row)}\n")
        else:
            lines.append(f"### Result\n")
            lines.append(f"Failed after {len(result['attempts'])} attempts.  \n")
            lines.append(f"> Last error: `{result['final_error']}`\n")

        lines.append("\n")

    path = "evaluation_log.md"
    with open(path, "w", encoding="utf-8") as f:
        f.writelines(lines)

    print(f"\nLog saved to {path}")


if __name__ == "__main__":
    results, passed, failed = run_tests()

    if "--save-log" in sys.argv:
        save_markdown_log(results, passed, failed)
