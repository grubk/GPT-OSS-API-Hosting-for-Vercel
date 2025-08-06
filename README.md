# GPT-OSS-20B API

A Flask API for chatting with GPT-OSS-20B model via Hugging Face.

## Deployment on Vercel

### Prerequisites
1. A Vercel account
2. A Hugging Face account with API token
3. Git repository

### Steps to Deploy

1. **Install Vercel CLI** (optional):
   ```bash
   npm i -g vercel
   ```

2. **Set up environment variables in Vercel**:
   - Go to your Vercel dashboard
   - Navigate to your project settings
   - Add environment variable: `HF_TOKEN` with your Hugging Face API token
   - Optional: Add `API_KEY` with a secure random string for API authentication

3. **Deploy via Git**:
   - Push your code to GitHub/GitLab/Bitbucket
   - Import the repository in Vercel dashboard
   - Vercel will automatically detect the configuration and deploy

4. **Deploy via CLI** (alternative):
   ```bash
   vercel --prod
   ```

### Usage

Send POST requests to `https://your-vercel-app.vercel.app/chat` with the following format:

**Without Authentication:**
```json
{
  "messages": [
    {"role": "user", "content": "Hello!"}
  ],
  "model": "openai/gpt-oss-20b:fireworks-ai"
}
```

**With Authentication (if API_KEY is set):**
```bash
curl -X POST https://your-vercel-app.vercel.app/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-api-key-here" \
  -d '{
    "messages": [
      {"role": "user", "content": "Hello!"}
    ],
    "model": "openai/gpt-oss-20b:fireworks-ai"
  }'
```

### Files Created for Vercel Deployment

- `vercel.json` - Vercel configuration
- `requirements.txt` - Python dependencies
- Modified `api/app.py` - Flask app with Vercel compatibility

### Environment Variables

- `HF_TOKEN` - Your Hugging Face API token (required)
- `API_KEY` - Optional API key for authentication (if set, all requests must include Authorization header)

## Local Development

1. Create a `.env` file with:
   ```
   HF_TOKEN=your_huggingface_token_here
   API_KEY=your_optional_api_key_here
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the app:
   ```bash
   python api/app.py
   ```

The app will be available at `http://localhost:5000/chat`
