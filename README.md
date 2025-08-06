# GPT-OSS-20B API for Vercel deployment

A Flask API for chatting with GPT-OSS-20B model via Hugging Face, made to be deployed on Vercel.

### Prerequisites
1. A Vercel account
2. A Hugging Face account with API token
3. Git repository

### Steps to Deploy

1. **Set up environment variables in Vercel**:
   - Go to your Vercel dashboard
   - Navigate to your project settings
   - Add environment variable: `HF_TOKEN` with your Hugging Face API token

2. **Deploy via Git**:
   - Push your code to a repository
   - Import the repository in Vercel dashboard
   - Vercel will automatically detect the configuration and deploy


### Usage

Send POST requests to `https://your-vercel-app.vercel.app/chat` with the following format:

```
{
  "messages": [
    {"role": "user", "content": "Hello!"}
  ],
  "model": "openai/gpt-oss-20b:fireworks-ai"
}
```

### Environment Variables

- `HF_TOKEN` - Your Hugging Face API token (required)

## Local Development

1. Create a `.env` file with:
   ```
   HF_TOKEN=your_huggingface_token_here
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the app:
   ```
   python api/app.py
   ```

The app will be available at `http://localhost:5000/chat`
