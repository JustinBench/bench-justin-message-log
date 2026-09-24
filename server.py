import json
from pathlib import Path
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=[])

MESSAGE_FILE = Path(__file__).parent / "messages.jsonl"

@app.route("/")
def main():
    return render_template("main/index.html")

@app.route("/messages", methods=["GET"])
def get_messages():
    messages = []

    with MESSAGE_FILE.open("r", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                messages.append(json.loads(line))

    return jsonify(messages), 200

@app.route("/messages", methods=["POST"])
def add_message():
    if not request.is_json:
        return jsonify({
            "error": "Content-Type must be application/json"
        }), 400

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": "Request body must contain a JSON object"
        }), 400

    message = data.get("message")

    if not isinstance(message, str) or not message.strip():
        return jsonify({
            "error": "The message field must contain text"
        }), 400

    new_message = {
        "message": message.strip()
    }

    with MESSAGE_FILE.open("a+", encoding="utf-8") as file:
        file.seek(0, 2)

        if file.tell() > 0:
            file.seek(file.tell() - 1)
            last_character = file.read(1)

            if last_character != "\n":
                file.write("\n")

        file.write(json.dumps(new_message) + "\n")

    return "", 201

@app.route("/about_me")
def project_one():
    return render_template("project_one/about_me.html")

@app.route("/zelda")
def project_two():
    return render_template("project_two/zelda.html")

if __name__ == "__main__":
    app.run()