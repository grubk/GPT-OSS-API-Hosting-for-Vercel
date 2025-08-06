import requests
import json

base_url = "your-deployed-url"  # Replace with your actual URL
chat_url = f"{base_url}/chat"

def test_api(test_name, payload):
    print(f"\n{'='*20} {test_name} {'='*20}")
    try:
        response = requests.post(chat_url, json=payload, timeout=30)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

tests = [
    {
        "name": "Simple Question",
        "payload": {
            "messages": [
                {"role": "user", "content": "What is the capital of France?"}
            ]
        }
    },
    {
        "name": "Conversation Context",
        "payload": {
            "messages": [
                {"role": "user", "content": "Hello, my name is John"},
                {"role": "assistant", "content": "Hello John! Nice to meet you."},
                {"role": "user", "content": "What's my name?"}
            ]
        }
    },
    {
        "name": "Custom Model",
        "payload": {
            "messages": [
                {"role": "user", "content": "Tell me a short joke"}
            ],
            "model": "openai/gpt-oss-20b:fireworks-ai"
        }
    },
    {
        "name": "Error Test - Missing Messages",
        "payload": {
            "model": "openai/gpt-oss-20b:fireworks-ai"
        }
    }
]

# Run all tests
print(f"Testing API at: {chat_url}")
successful_tests = 0

for test in tests:
    success = test_api(test["name"], test["payload"])
    if success:
        successful_tests += 1

print(f"\n{'='*60}")
print(f"Results: {successful_tests}/{len(tests)} tests passed")