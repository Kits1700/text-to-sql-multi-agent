# Multilingual Multi-Agent Text-to-SQL

Bilingual (English + Czech) Text-to-SQL pipeline using a multi-agent loop.

---

## How to run

**1. Install Python**

Download and install Python 3.10 or newer from https://python.org/downloads

To check it's installed, open a terminal and run:
```bash
python3 --version
```

**2. Install an editor**

Download VS Code from https://code.visualstudio.com and install the Python extension from the Extensions panel.

**3. Install Ollama**

Download Ollama from https://ollama.com and follow the installer for your OS. Ollama lets you run AI models locally on your machine.

On macOS, open the Ollama app after installing, it runs as a background service in your menu bar.
Once Ollama is running, pull the model used by this project:
```bash
ollama pull qwen2.5:1.5b
```

This downloads a small (1.5 billion parameter) language model. You can confirm it downloaded with:
```bash
ollama list
```

**4. Get a Claude API key**

Go to https://console.anthropic.com, create an account, and generate an API key.

This is only used on attempt 4 if the local model fails 3 times in a row, the system automatically falls back to Claude.

Copy the `.env.example` file and fill in your key:
```bash
cp .env.example .env
```
Then open `.env` and replace `your-key-here` with your actual key.

**5. Install project dependencies**
```bash
pip install -r requirements.txt
```

**6. Start the web app**
```bash
python app.py
```
Open `http://localhost:5001` in your browser.

**7. Or run the evaluation test suite**
```bash
python test_script.py              # prints results to console
python test_script.py --save-log   # also saves evaluation_log.md
```

---

## How it works

```
[Question]
    │
    ▼
Router Agent       figures out which database the question is about
    │
    ▼
Generator Agent  ◄──────────────────────────────────────┐
    │                                                    │
    │  writes SQL                                   failed SQL
    ▼                                               + error msg
SQL Executor                                            │
    │                                                   │
  pass? ── no ─────────────────────────────────────────┘
    │
   yes
    │
    ▼
Return results


```

Attempts 1, 2, 3 → local Ollama model (qwen2.5:1.5b)
Attempt 4 → Claude API (automatic fallback if all 3 local attempts fail)

---

## Files

| File | What it does |
|---|---|
| `app.py` | Web server |
| `pipeline.py` | Runs the agent loop |
| `router_agent.py` | Picks the right database |
| `generator_agent.py` | Writes the SQL query |
| `sql_executor.py` | Runs the SQL, catches errors |
| `schema_reader.py` | Reads table structure from the database |
| `test_script.py` | Runs all 10 test cases |
| `databases/` | The two SQLite databases |
| `templates/index.html` | Web UI |

---

## How Czech queries work

Both the local model and Claude understand Czech. The prompt tells the model to always write SQL using the English table and column names from the schema, regardless of what language the question is in. The databases are never touched or translated.

```
Input  → "Kolik vedoucích oddělení je starších než 56 let?"
Output → SELECT COUNT(*) FROM head WHERE age > 56
```

---

## Schema discovery

No table or column names are hardcoded anywhere in the prompts. `schema_reader.py` reads the structure directly from each SQLite file at runtime, so adding a new database requires no code changes.
