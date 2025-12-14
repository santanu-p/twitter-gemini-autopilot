# Twitter AI Automation Tool with Gemini 2.0 + Google Search
# Fixed version for google-genai package

from dotenv import load_dotenv
load_dotenv()

import os
import time
from google import genai
from google.genai import types
import tweepy
from datetime import datetime
import json
import schedule

# ============================================
# CONFIGURATION
# ============================================

class Config:
    # Twitter API credentials (X API v2)
    TWITTER_API_KEY = os.getenv('TWITTER_API_KEY')
    TWITTER_API_SECRET = os.getenv('TWITTER_API_SECRET')
    TWITTER_ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
    TWITTER_ACCESS_SECRET = os.getenv('TWITTER_ACCESS_SECRET')
    TWITTER_BEARER_TOKEN = os.getenv('TWITTER_BEARER_TOKEN')
    
    # Gemini API key
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    
    # Settings
    POSTS_PER_DAY = 5
    POST_INTERVAL_HOURS = 3

# ============================================
# GEMINI AI HANDLER
# ============================================

class GeminiHandler:
    def __init__(self, api_key):
        self.client = genai.Client(api_key=api_key)
        self.model = 'gemini-2.5-flash'
        
        # Configure Google Search grounding tool
        self.grounding_tool = types.Tool(
            google_search=types.GoogleSearch()
        )
        print("✓ Gemini API initialized with Google Search")
    
    def find_trending_topics(self):
        """Find top 5 trending topics using real-time Google Search"""
        prompt = """Search the web and find the top 5 MOST trending topics RIGHT NOW (today) across:
        - Technology & AI
        - Business & Economy
        - Entertainment & Pop Culture
        - Science & Innovation
        - Breaking News
        
        Focus on topics that are:
        1. Currently trending TODAY
        2. Have high engagement potential
        3. Are newsworthy and timely
        4. Suitable for professional Twitter posts
        
        Return ONLY a JSON array with 5 topics in this exact format:
        ["topic1", "topic2", "topic3", "topic4", "topic5"]
        
        Make each topic specific and timely (e.g., "OpenAI's new GPT-5 announcement" instead of just "AI")."""
        
        try:
            config = types.GenerateContentConfig(
                tools=[self.grounding_tool],
                temperature=0.7
            )
            
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=config
            )
            
            text = response.text.strip()
            # Remove markdown code blocks if present
            text = text.replace('```json', '').replace('```', '').strip()
            topics = json.loads(text)
            
            print(f"✓ Found trending topics (with Google Search):")
            for i, topic in enumerate(topics, 1):
                print(f"  {i}. {topic}")
            
            return topics
        except Exception as e:
            print(f"✗ Error finding topics: {e}")
            print(f"Response text (for debugging): {response.text if 'response' in locals() else 'No response'}")
            # Fallback topics
            return [
                "Latest AI developments", 
                "Tech industry news", 
                "Space exploration updates",
                "Cryptocurrency trends", 
                "Healthcare innovation"
            ]
    
    def generate_tweet(self, topic):
        """Generate an engaging tweet for a topic using Google Search for accuracy"""
        prompt = f"""Search the web for current information about: {topic}

        Then create an engaging, accurate Twitter post based on the LATEST information you find.

        Requirements:
        - Maximum 280 characters
        - Use CURRENT, ACCURATE information from your search
        - Informative and interesting
        - Include 2-3 relevant hashtags
        - Professional yet conversational tone
        - Make it timely and newsworthy
        - No emojis unless very appropriate
        
        Return ONLY the tweet text, nothing else. No explanations."""
        
        try:
            config = types.GenerateContentConfig(
                tools=[self.grounding_tool],
                temperature=0.8
            )
            
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=config
            )
            
            tweet = response.text.strip()
            # Remove quotes if AI added them
            tweet = tweet.strip('"').strip("'")
            
            # Ensure it's under 280 characters
            if len(tweet) > 280:
                tweet = tweet[:277] + "..."
            
            print(f"✓ Generated tweet: {tweet[:80]}{'...' if len(tweet) > 80 else ''}")
            return tweet
        except Exception as e:
            print(f"✗ Error generating tweet: {e}")
            return None

# ============================================
# TWITTER HANDLER
# ============================================

class TwitterHandler:
    def __init__(self, api_key, api_secret, access_token, access_secret, bearer_token):
        # Initialize Twitter API v2 client
        self.client = tweepy.Client(
            bearer_token=bearer_token,
            consumer_key=api_key,
            consumer_secret=api_secret,
            access_token=access_token,
            access_token_secret=access_secret
        )
        print("✓ Twitter API initialized")
    
    def post_tweet(self, text):
        """Post a tweet to Twitter"""
        try:
            response = self.client.create_tweet(text=text)
            print(f"✓ Tweet posted successfully! ID: {response.data['id']}")
            return True
        except Exception as e:
            print(f"✗ Error posting tweet: {e}")
            return False

# ============================================
# AUTOMATION ORCHESTRATOR
# ============================================

class TwitterAutomation:
    def __init__(self):
        self.config = Config()
        
        # Validate API keys
        if not self.config.GEMINI_API_KEY:
            raise ValueError("❌ GEMINI_API_KEY not found in .env file!")
        if not self.config.TWITTER_API_KEY:
            raise ValueError("❌ Twitter API keys not found in .env file!")
        
        self.gemini = GeminiHandler(self.config.GEMINI_API_KEY)
        self.twitter = TwitterHandler(
            self.config.TWITTER_API_KEY,
            self.config.TWITTER_API_SECRET,
            self.config.TWITTER_ACCESS_TOKEN,
            self.config.TWITTER_ACCESS_SECRET,
            self.config.TWITTER_BEARER_TOKEN
        )
        self.daily_topics = []
        self.posts_today = 0
    
    def refresh_daily_topics(self):
        """Get new trending topics for the day"""
        print(f"\n{'='*50}")
        print(f"Refreshing daily topics - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*50}")
        self.daily_topics = self.gemini.find_trending_topics()
        self.posts_today = 0
    
    def create_and_post(self):
        """Create and post a tweet"""
        if self.posts_today >= self.config.POSTS_PER_DAY:
            print("✓ Daily post limit reached. Waiting for next day...")
            return
        
        if not self.daily_topics:
            self.refresh_daily_topics()
        
        # Get next topic
        topic = self.daily_topics[self.posts_today % len(self.daily_topics)]
        
        print(f"\n{'='*50}")
        print(f"Creating post {self.posts_today + 1}/{self.config.POSTS_PER_DAY}")
        print(f"Topic: {topic}")
        print(f"{'='*50}")
        
        # Generate tweet
        tweet = self.gemini.generate_tweet(topic)
        
        if tweet:
            # Post to Twitter
            if self.twitter.post_tweet(tweet):
                self.posts_today += 1
                print(f"✓ Progress: {self.posts_today}/{self.config.POSTS_PER_DAY} posts today")
    
    def run(self):
        """Main execution loop"""
        print("""
╔════════════════════════════════════════════════╗
║   Twitter AI Automation Tool                   ║
║   Powered by Gemini 2.5 Flash + Google Search  ║
╚════════════════════════════════════════════════╝
        """)
        
        # Initial setup
        self.refresh_daily_topics()
        
        # Schedule jobs
        schedule.every().day.at("06:00").do(self.refresh_daily_topics)
        schedule.every(self.config.POST_INTERVAL_HOURS).hours.do(self.create_and_post)
        
        # Run first post immediately
        self.create_and_post()
        
        print(f"\n✓ Automation started!")
        print(f"✓ Will post every {self.config.POST_INTERVAL_HOURS} hours")
        print(f"✓ Daily limit: {self.config.POSTS_PER_DAY} posts")
        print(f"✓ Press Ctrl+C to stop\n")
        
        # Keep running
        while True:
            schedule.run_pending()
            time.sleep(60)

# ============================================
# MAIN ENTRY POINT
# ============================================

if __name__ == "__main__":
    try:
        automation = TwitterAutomation()
        automation.run()
    except KeyboardInterrupt:
        print("\n\n✓ Automation stopped by user")
    except Exception as e:
        print(f"\n✗ Fatal error: {e}")
        import traceback
        traceback.print_exc()