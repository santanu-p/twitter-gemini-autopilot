#!/usr/bin/env python3
"""
Single-run version for GitHub Actions
Runs once per execution, posts one tweet
"""

import os
from google import genai
from google.genai import types
import tweepy
from datetime import datetime
import json

# ============================================
# CONFIGURATION
# ============================================

class Config:
    # Twitter API credentials (from GitHub Secrets)
    TWITTER_API_KEY = os.getenv('TWITTER_API_KEY')
    TWITTER_API_SECRET = os.getenv('TWITTER_API_SECRET')
    TWITTER_ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
    TWITTER_ACCESS_SECRET = os.getenv('TWITTER_ACCESS_SECRET')
    TWITTER_BEARER_TOKEN = os.getenv('TWITTER_BEARER_TOKEN')
    
    # Gemini API key
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# ============================================
# GEMINI AI HANDLER
# ============================================

class GeminiHandler:
    def __init__(self, api_key):
        self.client = genai.Client(api_key=api_key)
        self.model = 'gemini-2.0-flash-exp'
        
        # Configure Google Search grounding tool
        self.grounding_tool = types.Tool(
            google_search=types.GoogleSearch()
        )
        print("✓ Gemini API initialized with Google Search")
    
    def find_trending_topic(self):
        """Find one trending topic using real-time Google Search"""
        prompt = """Search the web and find ONE highly trending topic RIGHT NOW (today) that would make an engaging Twitter post.

        Focus on a topic that is:
        1. Currently trending TODAY
        2. Newsworthy and timely
        3. Has high engagement potential
        4. Suitable for professional Twitter posts
        
        Return ONLY the topic as plain text, nothing else. Make it specific and timely."""
        
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
            
            topic = response.text.strip()
            print(f"✓ Found trending topic: {topic}")
            return topic
            
        except Exception as e:
            print(f"✗ Error finding topic: {e}")
            return "Latest developments in AI technology"
    
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
            
            print(f"✓ Generated tweet: {tweet}")
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
# MAIN EXECUTION
# ============================================

def main():
    print("="*60)
    print(f"Twitter AI Bot - Single Run")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    config = Config()
    
    # Validate API keys
    if not config.GEMINI_API_KEY:
        print("✗ GEMINI_API_KEY not found!")
        return
    if not config.TWITTER_API_KEY:
        print("✗ Twitter API keys not found!")
        return
    
    try:
        # Initialize handlers
        gemini = GeminiHandler(config.GEMINI_API_KEY)
        twitter = TwitterHandler(
            config.TWITTER_API_KEY,
            config.TWITTER_API_SECRET,
            config.TWITTER_ACCESS_TOKEN,
            config.TWITTER_ACCESS_SECRET,
            config.TWITTER_BEARER_TOKEN
        )
        
        # Find trending topic
        topic = gemini.find_trending_topic()
        print(f"\n📍 Topic: {topic}\n")
        
        # Generate tweet
        tweet = gemini.generate_tweet(topic)
        
        if tweet:
            # Post to Twitter
            if twitter.post_tweet(tweet):
                print("\n✓ Success! Tweet posted.")
            else:
                print("\n✗ Failed to post tweet.")
        else:
            print("\n✗ Failed to generate tweet.")
            
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()