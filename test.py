import requests
import json

base_url = "https://gpt-oss-20b-api-hosting.vercel.app"  # Updated with your URL
chat_url = f"{base_url}/chat"

# Optional: Set your API key here if authentication is enabled
API_KEY = None  # Replace with your API key if needed: "your-api-key-here"

def test_api(test_name, payload, expected_status=200):
    print(f"\n{'='*20} {test_name} {'='*20}")
    try:
        headers = {"Content-Type": "application/json"}
        if API_KEY:
            headers["Authorization"] = f"Bearer {API_KEY}"
        
        response = requests.post(chat_url, json=payload, headers=headers, timeout=30)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == expected_status
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
        },
        "expected_status": 400
    }
]

# Add authentication tests if API_KEY is set
if API_KEY:
    tests.append({
        "name": "Auth Test - Valid API Key",
        "payload": {
            "messages": [
                {"role": "user", "content": "Test with valid API key"}
            ]
        },
        "expected_status": 200
    })

# Test for rate limiting (if enabled)
def test_rate_limiting():
    """Test rate limiting by making multiple requests quickly"""
    print(f"\n{'='*20} Rate Limiting Test {'='*20}")
    print("Making 15 rapid requests to test rate limiting...")
    
    rate_limited = False
    for i in range(15):
        try:
            headers = {"Content-Type": "application/json"}
            if API_KEY:
                headers["Authorization"] = f"Bearer {API_KEY}"
            
            payload = {
                "messages": [{"role": "user", "content": f"Test {i+1}"}]
            }
            
            response = requests.post(chat_url, json=payload, headers=headers, timeout=30)
            print(f"Request {i+1}: Status {response.status_code}")
            
            if response.status_code == 429:
                rate_limited = True
                print(f"✅ Rate limiting triggered at request {i+1}")
                break
                
        except Exception as e:
            print(f"❌ Error on request {i+1}: {e}")
            break
    
    if not rate_limited:
        print("ℹ️ Rate limiting not triggered (may be disabled or limit not reached)")
    
    return True  # Always return true as this is informational

# Test health check endpoint
def test_health_check():
    print(f"\n{'='*20} Health Check {'='*20}")
    try:
        response = requests.get(f"{base_url}/", timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

# Run all tests
print(f"Testing API at: {chat_url}")
successful_tests = 0

# Test health check first
if test_health_check():
    print("✅ Health check passed")
else:
    print("❌ Health check failed")

for test in tests:
    expected_status = test.get("expected_status", 200)
    success = test_api(test["name"], test["payload"], expected_status)
    if success:
        successful_tests += 1

# Test rate limiting
print(f"\n{'='*60}")
test_rate_limiting()

print(f"\n{'='*60}")
print(f"Results: {successful_tests}/{len(tests)} tests passed")