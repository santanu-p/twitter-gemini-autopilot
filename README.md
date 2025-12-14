# Twitter Gemini Autopilot

A sophisticated automation tool that leverages Google Gemini AI and real-time Google Search to generate and post engaging Twitter content based on trending topics. The system autonomously discovers trending topics across technology, business, entertainment, science, and breaking news, then creates informative tweets using the latest available information.

## Features

- **Real-time Trend Discovery**: Uses Google Search integration to find the most trending topics across multiple categories
- **AI-Powered Content Generation**: Leverages Google Gemini 2.5 Flash for creating engaging, accurate tweets
- **Automated Posting**: Scheduled posting system with configurable limits (up to 5 tweets per day)
- **Python 3.13+ Compatibility**: Automatic compatibility fixes for modern Python versions
- **Rate Limit Handling**: Built-in error handling and retry mechanisms for API interactions
- **Environment-Based Configuration**: Secure credential management using environment variables

## Project Structure

- `main.py` — Core automation orchestrator and entry point
- `start.py` — Startup script with Python 3.13 compatibility fixes
- `fix.py` — Standalone compatibility fix utility
- `requirements.txt` — Python dependencies
- `Procfile` — Heroku deployment configuration
- `runtime.txt` — Python runtime specification for deployment
- `LICENSE` — MIT license

## Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/santanu-p/twitter-gemini-autopilot.git
   cd twitter-gemini-autopilot
   ```

2. **Set up virtual environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**

   Create a `.env` file in the project root:

   ```env
   # Twitter API v2 Credentials (get from https://developer.twitter.com)
   TWITTER_API_KEY=your_api_key_here
   TWITTER_API_SECRET=your_api_secret_here
   TWITTER_ACCESS_TOKEN=your_access_token_here
   TWITTER_ACCESS_SECRET=your_access_secret_here
   TWITTER_BEARER_TOKEN=your_bearer_token_here

   # Google Gemini API Key (get from https://makersuite.google.com/app/apikey)
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

5. **Run the automation**
   ```bash
   python start.py
   ```

### API Setup

#### Twitter API
1. Visit [Twitter Developer Portal](https://developer.twitter.com)
2. Create a new app or use existing one
3. Generate API v2 credentials (API Key, API Secret, Access Token, Access Secret, Bearer Token)
4. Ensure your app has write permissions for posting tweets

#### Google Gemini API
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the key to your environment variables

## Usage

### Basic Operation

The tool runs autonomously once started:

- **Daily Topic Refresh**: Updates trending topics every day at 6:00 AM
- **Scheduled Posting**: Posts every 3 hours (configurable)
- **Daily Limit**: Maximum 5 posts per day
- **Real-time Search**: Uses Google Search for current, accurate information

### Manual Control

```bash
# View help
python main.py --help

# Run compatibility fix only
python fix.py

# Start with automatic fixes
python start.py
```

### Configuration Options

Edit the `Config` class in `main.py` to customize:

- `POSTS_PER_DAY`: Maximum tweets per day (default: 5)
- `POST_INTERVAL_HOURS`: Hours between posts (default: 3)

## Deployment

### Heroku

1. **Create Heroku app**
   ```bash
   heroku create your-app-name
   ```

2. **Set environment variables**
   ```bash
   heroku config:set TWITTER_API_KEY=your_key
   heroku config:set TWITTER_API_SECRET=your_secret
   heroku config:set TWITTER_ACCESS_TOKEN=your_token
   heroku config:set TWITTER_ACCESS_SECRET=your_secret
   heroku config:set TWITTER_BEARER_TOKEN=your_bearer
   heroku config:set GEMINI_API_KEY=your_gemini_key
   ```

3. **Deploy**
   ```bash
   git push heroku main
   ```

The `Procfile` and `runtime.txt` are pre-configured for Heroku deployment.

## Development

### Prerequisites

- Python 3.8+
- Twitter Developer Account with API v2 access
- Google Gemini API key

### Testing

The tool includes basic error handling and logging. For production use:

- Monitor API rate limits
- Test with dummy credentials first
- Validate tweet content before full automation

### Security Best Practices

- Never commit `.env` files or API keys
- Use environment variables or secret managers
- Rotate API keys regularly
- Monitor account activity for unauthorized access

## Troubleshooting

### Common Issues

**Python 3.13 Compatibility**
- The `start.py` script automatically handles this
- If issues persist, run `python fix.py` manually

**API Rate Limits**
- Twitter: 300 posts per 3 hours for v2 API
- Gemini: 60 requests per minute
- Built-in delays prevent hitting limits

**Missing Dependencies**
```bash
pip install --upgrade -r requirements.txt
```

**Environment Variables Not Loading**
- Ensure `.env` file exists in project root
- Check variable names match exactly
- Restart the application after changes

### Logs and Debugging

The application provides detailed console output:
- ✓ Success indicators
- ✗ Error messages with details
- Progress tracking for daily limits

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Keep commits focused and descriptive
- Add tests for new features
- Update documentation for API changes
- Follow PEP 8 style guidelines

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This tool is for educational and legitimate automation purposes. Users are responsible for complying with Twitter's Terms of Service and API usage policies. Automated posting should not violate platform rules or spam guidelines.
