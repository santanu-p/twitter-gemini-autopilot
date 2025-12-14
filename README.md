# twitter-gemini-autopilot

Small utilities to automate interactions between Twitter and a large language model (Google Gemini or other LLMs) for content generation, posting, and automated replies.

## Project overview
This repo contains lightweight helpers and CLI scripts to:
- Generate tweet content and threads using LLM prompts with Google Gemini 2.5 Flash.
- Find trending topics via real-time Google Search integration.
- Post tweets and replies via Twitter API wrappers.
- Provide small maintenance/fix scripts (e.g., `fix.py`) and an orchestrator (`main.py`) for experimentation.
- Include a startup script (`start.py`) for automatic Python 3.13 compatibility fixes.

Repository layout
- main.py — primary orchestration / entrypoint for Twitter automation (uses Gemini and Google Search).
- start.py — startup script that fixes Python 3.13 compatibility and launches main.py.
- fix.py — helper script(s) for quick fixes or utilities.
- requirements.txt — Python dependencies.
- LICENSE — MIT license.

## Quick start

1. Clone
   ```bash
   git clone https://github.com/santanu-p/twitter-gemini-autopilot.git
   cd twitter-gemini-autopilot
   ```

2. Create and activate a virtual environment
   - Windows:
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     python -m venv venv
     source venv/bin/activate
     ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Configure credentials (environment variables recommended)
   - TWITTER_API_KEY
   - TWITTER_API_SECRET
   - TWITTER_ACCESS_TOKEN
   - TWITTER_ACCESS_SECRET
   - TWITTER_BEARER_TOKEN
   - GEMINI_API_KEY (for Google Gemini 2.5 Flash)

You can use a .env loader in your code (python-dotenv) or your CI/secrets manager.

## Usage examples
- Run the automation tool (recommended):
  ```bash
  python start.py
  ```

- Inspect and run the orchestrator directly:
  ```bash
  python main.py --help
  # The tool runs autonomously, posting up to 5 tweets per day based on trending topics
  ```

- Run a helper/fix script:
  ```bash
  python fix.py
  ```

Adjust flags and behavior by reading the docstrings or CLI help inside the scripts.

## Development notes
- Keep secrets out of the repo. Use environment variables or a secrets manager.
- Start small: separate prompt templates, posting logic, and retry/error handling before scaling.
- Add tests for prompt outputs and API interactions if you plan to automate at scale.
- Note: start.py automatically handles Python 3.13 compatibility (e.g., missing imghdr module).

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
```bash
git remote add origin https://github.com/santanu-p/twitter-gemini-autopilot.git
git branch -M main
git add .
git commit -m "chore(docs): update README and add MIT license"
git push -u origin main
```
