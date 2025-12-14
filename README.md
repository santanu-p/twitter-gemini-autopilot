# twitter-gemini-autopilot

Small utilities to automate interactions between Twitter and Google Gemini (LLM) for tasks like content generation, posting, and automated replies.

## Features
- Generate tweet content using Gemini prompts.
- Post tweets and replies via Twitter API helpers.
- Small CLI scripts: `main.py` (orchestrator) and `fix.py` (helper/fixes).
- Minimal, easy-to-adapt code for experimentation and automation.

## Prerequisites
- Python 3.8+
- pip
- Twitter API credentials (API key, API secret, access token, access token secret) or Twitter developer access.
- Google Gemini API credentials or other LLM access (if applicable).
- `requirements.txt` included for dependencies.

## Quick setup
1. Create and activate a virtual environment:
   - Windows: python -m venv venv && venv\Scripts\activate
   - macOS/Linux: python -m venv venv && source venv/bin/activate
2. Install dependencies:
   pip install -r requirements.txt
3. Configure environment variables (example):
   - TWITTER_API_KEY, TWITTER_API_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET
   - GEMINI_API_KEY (or other LLM token)

## Usage
- Inspect `main.py` and `fix.py` for entry points and configuration.
- Example run:
  python main.py --help
- Run with environment variables set or via a .env loader in your environment.

## Development notes
- Keep secrets out of the repo. Use environment variables or a secrets manager.
- Modularize prompts and posting logic before scaling to higher volume.

## Commit & push to GitHub

Option A — you already created a remote:
git remote add origin https://github.com/santanu-p/twitter-gemini-autopilot.git
git branch -M main
git add .
git commit -m "chore: update README"
git push -u origin main

Option B — using GitHub CLI (recommended if installed):
gh repo create santanu-p/twitter-gemini-autopilot --public --source=. --remote=origin --push

Option C — create repo via API with a PAT (replace $TOKEN):
curl -H "Authorization: token $TOKEN" -d '{"name":"twitter-gemini-autopilot"}' https://api.github.com/user/repos
git remote add origin https://github.com/<you>/twitter-gemini-autopilot.git
git branch -M main
git add README.md
git commit -m "docs: update README for project"
git push -u origin main

## License
This project is released under the MIT License — see the accompanying LICENSE file for details.

## Contributing
Open issues or PRs. Keep changes small and documented.
