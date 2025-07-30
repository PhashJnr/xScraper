#!/usr/bin/env python3
"""
Twitter Monitor using RSS Feeds
Simple and reliable alternative to API/web scraping
"""

import logging
import json
import os
import time
import requests
import feedparser
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Set
from config import USERS_TO_MONITOR, LOG_FILE

logger = logging.getLogger(__name__)

class TwitterRSSMonitor:
    def __init__(self):
        self.seen_tweets_file = 'seen_tweets_rss.json'
        self.seen_tweet_ids = self.load_seen_tweets()
        
    def load_seen_tweets(self) -> Set[str]:
        """Load previously seen tweet IDs from file"""
        try:
            if os.path.exists(self.seen_tweets_file):
                with open(self.seen_tweets_file, 'r') as f:
                    data = json.load(f)
                    return set(data.get('seen_tweets', []))
            return set()
        except Exception as e:
            logger.error(f"Error loading seen tweets: {e}")
            return set()
    
    def save_seen_tweets(self):
        """Save seen tweet IDs to file"""
        try:
            data = {
                'seen_tweets': list(self.seen_tweet_ids),
                'last_updated': datetime.now().isoformat()
            }
            with open(self.seen_tweets_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving seen tweets: {e}")
    
    def get_user_tweets(self, username: str) -> List[Dict]:
        """Get recent tweets from RSS feed"""
        try:
            # Try different RSS feed URLs
            rss_urls = [
                f"https://nitter.net/{username}/rss",
                f"https://nitter.1d4.us/{username}/rss",
                f"https://nitter.kavin.rocks/{username}/rss",
                f"https://nitter.unixfox.eu/{username}/rss"
            ]
            
            tweets = []
            one_hour_ago = datetime.now(timezone.utc) - timedelta(hours=1)
            
            for rss_url in rss_urls:
                try:
                    logger.info(f"Trying RSS feed: {rss_url}")
                    
                    # Parse RSS feed
                    feed = feedparser.parse(rss_url)
                    
                    if feed.entries:
                        logger.info(f"Found {len(feed.entries)} entries in RSS feed")
                        
                        for entry in feed.entries[:10]:  # Check first 10 entries
                            try:
                                tweet_data = self.parse_rss_entry(entry, username)
                                
                                if tweet_data and tweet_data['created_at'] >= one_hour_ago:
                                    # Check if it's an original tweet
                                    if self.is_original_tweet(entry):
                                        tweets.append(tweet_data)
                                        
                            except Exception as e:
                                logger.debug(f"Error parsing RSS entry: {e}")
                                continue
                        
                        # If we got tweets from this feed, stop trying others
                        if tweets:
                            break
                            
                except Exception as e:
                    logger.debug(f"Error with RSS feed {rss_url}: {e}")
                    continue
            
            logger.info(f"Found {len(tweets)} original tweets from @{username} in the last hour")
            return tweets
            
        except Exception as e:
            logger.error(f"Error getting tweets for {username}: {e}")
            return []
    
    def parse_rss_entry(self, entry, username: str) -> Dict:
        """Parse RSS entry into tweet data"""
        try:
            # Extract tweet ID from link
            link = entry.get('link', '')
            tweet_id = link.split('/status/')[-1].split('?')[0] if '/status/' in link else None
            
            if not tweet_id:
                return None
            
            # Get tweet text
            tweet_text = entry.get('title', '')
            
            # Get timestamp
            published = entry.get('published_parsed')
            if published:
                created_at = datetime(*published[:6], tzinfo=timezone.utc)
            else:
                created_at = datetime.now(timezone.utc)
            
            return {
                'id': tweet_id,
                'text': tweet_text,
                'created_at': created_at,
                'username': username,
                'type': 'original'
            }
            
        except Exception as e:
            logger.debug(f"Error parsing RSS entry: {e}")
            return None
    
    def is_original_tweet(self, entry) -> bool:
        """Check if RSS entry is an original tweet"""
        try:
            # Check for retweet indicators in title
            title = entry.get('title', '').lower()
            
            # Common retweet/quote indicators
            retweet_indicators = ['rt @', 'retweet', 'quote tweet']
            for indicator in retweet_indicators:
                if indicator in title:
                    return False
            
            return True
            
        except Exception as e:
            logger.debug(f"Error checking tweet type: {e}")
            return True  # Assume original if we can't determine
    
    def check_new_tweets(self) -> List[Dict]:
        """Check for new tweets from all monitored users"""
        new_tweets = []
        
        for username in USERS_TO_MONITOR:
            logger.info(f"Checking tweets for @{username}")
            tweets = self.get_user_tweets(username)
            
            for tweet in tweets:
                if tweet['id'] not in self.seen_tweet_ids:
                    new_tweets.append(tweet)
                    self.seen_tweet_ids.add(tweet['id'])
                    logger.info(f"New tweet found from @{username}: {tweet['text'][:50]}...")
            
            # Add delay between users
            if len(USERS_TO_MONITOR) > 1:
                time.sleep(2)
        
        # Save updated seen tweets
        if new_tweets:
            self.save_seen_tweets()
        
        return new_tweets
    
    def format_tweet_url(self, username: str, tweet_id: str) -> str:
        """Generate tweet URL"""
        return f"https://twitter.com/{username}/status/{tweet_id}"
    
    def format_created_at(self, created_at) -> str:
        """Format tweet creation time"""
        if created_at:
            return created_at.strftime("%Y-%m-%d %H:%M:%S UTC")
        return "Unknown time" 