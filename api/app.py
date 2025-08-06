import os
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()  # Load HF_TOKEN from .env if available

app = Flask(__name__)

API_URL = "https://router.huggingface.co/v1/chat/completions"
HF_TOKEN = os.environ.get("HF_TOKEN")

if not HF_TOKEN:
    raise RuntimeError("HF_TOKEN is not set in environment.")

HEADERS = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

DEFAULT_MODEL = "openai/gpt-oss-20b:fireworks-ai"

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()

        if "messages" not in data:
            return jsonify({"error": "Missing 'messages' in request body"}), 400

        payload = {
            "model": data.get("model", DEFAULT_MODEL),
            "messages": data["messages"]
        }

        response = requests.post(API_URL, headers=HEADERS, json=payload)
        response.raise_for_status()
        result = response.json()

        return jsonify({
            "reply": result["choices"][0]["message"]["content"]
        })

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Request to Hugging Face failed: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
