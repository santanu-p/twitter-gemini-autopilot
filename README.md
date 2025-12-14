# twitter-gemini-autopilot

Small utilities to automate interactions between Twitter and a large language model (Google Gemini or other LLMs) for content generation, posting, and automated replies.

## Project overview
This repo contains lightweight helpers and CLI scripts to:
- Generate tweet content and threads using LLM prompts.
- Post tweets and replies via Twitter API wrappers.
- Provide small maintenance/fix scripts (e.g., `fix.py`) and an orchestrator (`main.py`) for experimentation.

Repository layout
- main.py — primary orchestration / entrypoint (CLI or script).
- fix.py — helper script(s) for quick fixes or utilities.
- requirements.txt — Python dependencies.
- LICENSE — MIT license.

## Quick start

1. Clone
   git clone https://github.com/santanu-p/twitter-gemini-autopilot.git
   cd twitter-gemini-autopilot

2. Create and activate a virtual environment
   - Windows:
     python -m venv venv
     venv\Scripts\activate
   - macOS/Linux:
     python -m venv venv
     source venv/bin/activate

3. Install dependencies
   pip install -r requirements.txt

4. Configure credentials (environment variables recommended)
   - TWITTER_API_KEY
   - TWITTER_API_SECRET
   - TWITTER_ACCESS_TOKEN
   - TWITTER_ACCESS_SECRET
   - GEMINI_API_KEY (or other LLM API key)

You can use a .env loader in your code (python-dotenv) or your CI/secrets manager.

## Usage examples
- Inspect and run the orchestrator:
  python main.py --help
  python main.py --generate --post    # example flags — see main.py for exact CLI

- Run a helper/fix script:
  python fix.py

Adjust flags and behavior by reading the docstrings or CLI help inside the scripts.

## Development notes
- Keep secrets out of the repo. Use environment variables or a secrets manager.
- Start small: separate prompt templates, posting logic, and retry/error handling before scaling.
- Add tests for prompt outputs and API interactions if you plan to automate at scale.

## Logging & error handling
- Add structured logging (json/logfmt) for production runs.
- Implement rate-limit handling and backoff for Twitter/LLM APIs.

## Contributing
- Open issues or PRs.
- Use feature branches, keep commits small and focused, and include tests for behavior changes.

## License
This project is released under the MIT License — see LICENSE.

## Push to your GitHub repo
(Using the repo you shared)
git remote add origin https://github.com/santanu-p/twitter-gemini-autopilot.git
git branch -M main
git add .
git commit -m "chore: update README"
git push -u origin main
