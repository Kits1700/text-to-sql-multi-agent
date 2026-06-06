"""
app.py — the web server.

GET  /       serves the UI
POST /query  runs the pipeline and returns JSON
"""

from flask import Flask, render_template, request, jsonify
from pipeline import run_query

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/query", methods=["POST"])
def query():
    data     = request.get_json()
    question = data.get("question", "").strip()

    if not question:
        return jsonify({"error": "Please enter a question."}), 400

    return jsonify(run_query(question))


if __name__ == "__main__":
    app.run(debug=True, port=5001)
