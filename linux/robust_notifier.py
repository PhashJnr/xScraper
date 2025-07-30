#!/usr/bin/env python3
"""
Robust Telegram notification system with connection pooling and retry logic
"""

import logging
import asyncio
import threading
import time
import httpx
from telegram import Bot
from telegram.error import TelegramError, NetworkError, RetryAfter
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

logger = logging.getLogger(__name__)

class RobustTelegramNotifier:
    def __init__(self):
        self.bot = Bot(token=TELEGRAM_BOT_TOKEN)
        self.chat_id = TELEGRAM_CHAT_ID
        self._notification_lock = threading.Lock()
        self._last_notification_time = 0
        self._connection_pool = None
        
    async def send_notification_with_retry(self, message, max_retries=3):
        """Send notification with retry logic"""
        for attempt in range(max_retries):
            try:
                # Test the bot connection first
                bot_info = await self.bot.get_me()
                logger.info(f"Bot connection test successful: {bot_info.first_name}")
                
                # Send the message
                await self.bot.send_message(
                    chat_id=self.chat_id,
                    text=message,
                    parse_mode='HTML'
                )
                return True  # Success
                
            except RetryAfter as e:
                wait_time = e.retry_after
                logger.warning(f"Rate limited, waiting {wait_time} seconds")
                await asyncio.sleep(wait_time)
                continue
                
            except NetworkError as e:
                logger.warning(f"Network error (attempt {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    await asyncio.sleep(2 ** attempt)  # Exponential backoff
                    continue
                else:
                    logger.error(f"Failed to send notification after {max_retries} attempts")
                    return False
                    
            except Exception as e:
                logger.error(f"Unexpected error sending notification: {e}")
                if attempt < max_retries - 1:
                    await asyncio.sleep(2 ** attempt)
                    continue
                return False
        
        return False
    
    def send_notification_sync(self, message):
        """Synchronous wrapper with robust error handling"""
        try:
            # Rate limiting
            current_time = time.time()
            with self._notification_lock:
                if current_time - self._last_notification_time < 2:
                    time.sleep(2)
                self._last_notification_time = current_time
            
            # Use threading with better error handling
            def send_in_thread():
                try:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    try:
                        success = loop.run_until_complete(self.send_notification_with_retry(message))
                        if success:
                            logger.info("Notification sent successfully")
                        else:
                            logger.error("Failed to send notification")
                    finally:
                        loop.close()
                except Exception as e:
                    logger.error(f"Error in thread notification: {e}")
            
            # Run in separate thread
            thread = threading.Thread(target=send_in_thread)
            thread.daemon = True
            thread.start()
            thread.join(timeout=20)  # Longer timeout
            
        except Exception as e:
            logger.error(f"Error in sync notification: {e}")
    
    async def send_document_with_retry(self, file_path, caption="", max_retries=3):
        """Send document with retry logic"""
        for attempt in range(max_retries):
            try:
                # Test the bot connection first
                bot_info = await self.bot.get_me()
                logger.info(f"Bot connection test successful: {bot_info.first_name}")
                
                # Send the document
                with open(file_path, 'rb') as file:
                    await self.bot.send_document(
                        chat_id=self.chat_id,
                        document=file,
                        caption=caption,
                        parse_mode='HTML'
                    )
                return True  # Success
                
            except RetryAfter as e:
                wait_time = e.retry_after
                logger.warning(f"Rate limited, waiting {wait_time} seconds")
                await asyncio.sleep(wait_time)
                continue
                
            except NetworkError as e:
                logger.warning(f"Network error (attempt {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    await asyncio.sleep(2 ** attempt)  # Exponential backoff
                    continue
                else:
                    logger.error(f"Failed to send document after {max_retries} attempts")
                    return False
                    
            except Exception as e:
                logger.error(f"Unexpected error sending document: {e}")
                if attempt < max_retries - 1:
                    await asyncio.sleep(2 ** attempt)
                    continue
                return False
        
        return False
    
    def send_document(self, file_path, caption=""):
        """Synchronous wrapper for sending documents with robust error handling"""
        try:
            # Rate limiting
            current_time = time.time()
            with self._notification_lock:
                if current_time - self._last_notification_time < 2:
                    time.sleep(2)
                self._last_notification_time = current_time
            
            # Use threading with better error handling
            def send_in_thread():
                try:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    try:
                        success = loop.run_until_complete(self.send_document_with_retry(file_path, caption))
                        if success:
                            logger.info("Document sent successfully")
                        else:
                            logger.error("Failed to send document")
                    finally:
                        loop.close()
                except Exception as e:
                    logger.error(f"Error in thread document send: {e}")
            
            # Run in separate thread
            thread = threading.Thread(target=send_in_thread)
            thread.daemon = True
            thread.start()
            thread.join(timeout=30)  # Longer timeout for file uploads
            
            return True  # Assume success if no exception
            
        except Exception as e:
            logger.error(f"Error in sync document send: {e}")
            return False

    def format_tweet_message(self, username, tweet_text, tweet_url, created_at, tweet_type="original"):
        """Format tweet information for Telegram message"""
        type_emoji = '📝'
        type_text = 'Original Tweet'
        
        message = f"""
🔔 <b>New {type_text} from @{username}</b>

{type_emoji} <b>Content:</b>
{tweet_text}

🔗 <a href="{tweet_url}">View Tweet</a>
⏰ {created_at}

#TwitterMonitor
        """.strip()
        return message 