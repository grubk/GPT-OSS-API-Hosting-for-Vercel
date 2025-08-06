import os
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

load_dotenv()  # Load HF_TOKEN from .env if available

app = Flask(__name__)

# Environment variables
API_URL = "https://router.huggingface.co/v1/chat/completions"
HF_TOKEN = os.environ.get("HF_TOKEN")
API_KEY = os.environ.get("API_KEY")  # Optional API key for authentication
ENABLE_RATE_LIMITING = os.environ.get("ENABLE_RATE_LIMITING", "false").lower() == "true"

if not HF_TOKEN:
    raise RuntimeError("HF_TOKEN is not set in environment.")

# Initialize rate limiter (conditionally)
limiter = None
if ENABLE_RATE_LIMITING:
    limiter = Limiter(
        key_func=get_remote_address,
        app=app,
        default_limits=[],  # No default limits, we'll apply per route
        storage_uri="memory://",
    )

HEADERS = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

'''
Note: If you would like to use a different inference provider, you can set it here.
Here are the ones available on Hugging Face:
- openai/gpt-oss-20b:fireworks-ai
- openai/gpt-oss-20b:groq
- openai/gpt-oss-20b:hyperbolic
- openai/gpt-oss-20b:nscale
- openai/gpt-oss-20b:hf-inference
'''
DEFAULT_MODEL = "openai/gpt-oss-20b:fireworks-ai"

def conditional_rate_limit(rate_limit_string):
    """Decorator that conditionally applies rate limiting"""
    def decorator(f):
        if ENABLE_RATE_LIMITING and limiter:
            return limiter.limit(rate_limit_string)(f)
        return f
    return decorator

def require_api_key():
    """Check if API key is required and validate it"""
    if not API_KEY:
        return None  # No API key required if not set
    
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return jsonify({"error": "Missing Authorization header"}), 401
    
    if not auth_header.startswith("Bearer "):
        return jsonify({"error": "Invalid Authorization header format. Use 'Bearer <your-api-key>'"}), 401
    
    provided_key = auth_header[7:]  # Remove "Bearer " prefix
    if provided_key != API_KEY:
        return jsonify({"error": "Invalid API key"}), 401
    
    return None  # Valid authentication

@app.route("/", methods=["GET"])
def health_check():
    """Public health check endpoint"""
    return jsonify({
        "status": "healthy",
        "message": "GPT-OSS-20B API is running",
        "authentication": "required" if API_KEY else "not required",
        "rate_limiting": "enabled" if ENABLE_RATE_LIMITING else "disabled"
    })

@app.route("/chat", methods=["POST"])
@conditional_rate_limit("10 per minute")
def chat():
    # Check authentication
    auth_error = require_api_key()
    if auth_error:
        return auth_error
    
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
