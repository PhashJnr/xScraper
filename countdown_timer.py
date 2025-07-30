#!/usr/bin/env python3
"""
Countdown timer utility for terminal display
"""

import time
import sys
import threading
from datetime import datetime, timedelta

class CountdownTimer:
    def __init__(self, minutes):
        self.minutes = minutes
        self.seconds = minutes * 60
        self.running = False
        self._stop_event = threading.Event()
    
    def start(self):
        """Start the countdown timer with live display"""
        self.running = True
        self._stop_event.clear()
        
        print(f"\n⏰ Next check in {self.minutes} minutes...")
        print("=" * 50)
        
        remaining = self.seconds
        while remaining > 0 and not self._stop_event.is_set():
            minutes_left = remaining // 60
            seconds_left = remaining % 60
            
            # Clear line and show countdown
            sys.stdout.write(f"\r🕐 Next check in: {minutes_left:02d}:{seconds_left:02d}")
            sys.stdout.flush()
            
            time.sleep(1)
            remaining -= 1
        
        if not self._stop_event.is_set():
            print(f"\n✅ Time's up! Starting next check...")
        else:
            print(f"\n⏹️ Countdown stopped.")
    
    def stop(self):
        """Stop the countdown timer"""
        self.running = False
        self._stop_event.set()
    
    def get_remaining_time(self):
        """Get remaining time in seconds"""
        return max(0, self.seconds)

def format_time(seconds):
    """Format seconds into MM:SS"""
    minutes = seconds // 60
    secs = seconds % 60
    return f"{minutes:02d}:{secs:02d}"

def show_countdown(minutes, message="Next check"):
    """Show a countdown timer for specified minutes"""
    timer = CountdownTimer(minutes)
    
    try:
        timer.start()
    except KeyboardInterrupt:
        print(f"\n⏹️ Countdown interrupted by user")
        timer.stop()
        return False
    
    return True 