import os
import requests
from flask import Flask, jsonify, render_template, request
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

BHARATCODE_URL = "https://bharatcode.ai/api/model/v1/chat/completions"
MODEL_NAME = "qwen-3.8-27b"


def ask_bharatcode(prompt):
    api_key = os.getenv("BHARATCODE_API_KEY")
    if not api_key:
        raise RuntimeError(
            "BharatCode API key is missing. Add it to your .env file."
        )

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are PrepPilot AI, a supportive placement preparation "
                    "coach for Indian engineering students. Be accurate, clear, "
                    "beginner-friendly, and constructive. Do not claim that an "
                    "answer is correct unless it is justified."
                ),
            },
            {"role": "user", "content": prompt},
        ],
    }

    response = requests.post(
        BHARATCODE_URL, headers=headers, json=payload, timeout=90
    )
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"]


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/practice", methods=["POST"])
def practice():
    data = request.get_json(silent=True) or {}
    mode = data.get("mode", "question")
    topic = (data.get("topic") or "Java").strip()
    difficulty = (data.get("difficulty") or "Beginner").strip()

    if mode == "question":
        prompt = (
            f"Create ONE {difficulty.lower()}-level placement interview question "
            f"about {topic}. Give the question first, then a short hint. "
            "Do not reveal the answer yet. Format it clearly."
        )
    elif mode == "evaluate":
        question = (data.get("question") or "").strip()
        answer = (data.get("answer") or "").strip()
        if not question or not answer:
            return jsonify({"error": "Enter both the question and your answer."}), 400

        prompt = (
            "Evaluate this student's placement interview answer. "
            "Be supportive but honest. Give: (1) score out of 10, "
            "(2) what is correct, (3) what is missing or incorrect, "
            "(4) an improved sample answer, and (5) one follow-up question.\n\n"
            f"Topic: {topic}\nQuestion: {question}\nStudent answer: {answer}"
        )
    else:
        return jsonify({"error": "Unsupported practice mode."}), 400

    try:
        result = ask_bharatcode(prompt)
        return jsonify({"result": result})
    except requests.exceptions.HTTPError as exc:
        status = exc.response.status_code if exc.response is not None else 502
        return jsonify({
            "error": f"BharatCode API returned HTTP {status}. Check API access, key, and model availability."
        }), 502
    except requests.exceptions.Timeout:
        return jsonify({"error": "The AI request timed out. Please try again."}), 504
    except requests.exceptions.RequestException:
        return jsonify({"error": "Could not connect to BharatCode. Check your internet connection."}), 502
    except (KeyError, IndexError, TypeError, ValueError):
        return jsonify({"error": "The AI response format was unexpected. Please try again."}), 502
    except RuntimeError as exc:
        return jsonify({"error": str(exc)}), 500


if __name__ == "__main__":
    app.run(debug=True)
