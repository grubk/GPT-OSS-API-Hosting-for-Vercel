# GPT-OSS-20B API for Vercel deployment

‼️Today, OpenAI released an [open-source model](https://huggingface.co/openai/gpt-oss-20b) that is roughly as powerful as gpt-o3. This repo allows you to host this model on Vercel with some security features using Flask API in python.

---

### Features
- Rate limiting
- API-key authentication
- All features of the model accessible via API
- [test.py](https://github.com/grubk/gpt-oss-20b-api-hosting/blob/main/test.py) is included for test cases or to demonstrate usage after you deploy.

---

### Prerequisites
1. A Vercel account
2. A Hugging Face account with API token
3. Git repository

---

### Usage

1. **Clone the repo**

2.  **Set up environment variables in Vercel**:
   - Go to your Vercel dashboard
   - Navigate to your project settings
   - Add environment variables:
      - `HF_TOKEN` with your Hugging Face API token
      - Optional: Add `API_KEY` with a secure random string for API authentication
      - Optional: Add `ENABLE_RATE_LIMITING` set to `true` to enable rate limiting (default: false)

3. **Deploy via Git**:
   - Import the repository in Vercel dashboard
   - Vercel will automatically detect the configuration and deploy

---

### Usage

Send POST requests to `https://your-vercel-app.vercel.app/chat` with the following format:

```json
{
  "messages": [
    {"role": "user", "content": "Hello!"}
  ],
  "model": "openai/gpt-oss-20b:fireworks-ai"
}
```

---

### Files Created for Vercel Deployment

- `vercel.json` - Vercel configuration
- `requirements.txt` - Python dependencies
- Modified `api/app.py` - Flask app with Vercel compatibility

---

### Environment Variables

- `HF_TOKEN` - Your Hugging Face API token (required)
- `API_KEY` - Optional API key for authentication (if set, all requests must include Authorization header)
- `ENABLE_RATE_LIMITING` - Set to `true` to enable rate limiting (default: `false`)

### Rate Limiting

When `ENABLE_RATE_LIMITING=true`, the API applies these limits:
- **10 requests per minute per IP address** for `/chat` endpoint
- Rate limit exceeded returns `429 Too Many Requests`
- No rate limiting on health check endpoint (`/`)

## Local Development

1. Create a `.env` file with:
   ```
   HF_TOKEN=your_huggingface_token_here
   API_KEY=your_optional_api_key_here
   ENABLE_RATE_LIMITING=true
   ```

2. Install dependencies (highly recommended to create a virtual environment):
   ```
   pip install -r requirements.txt
   ```

3. Run the app:
   ```
   python api/app.py
   ```

The app will be available locally at `http://localhost:5000/chat`
