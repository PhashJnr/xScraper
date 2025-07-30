#!/usr/bin/env python3
"""
Countdown Timer Module
Provides a visual countdown timer for monitoring intervals
"""

import time
import sys
from datetime import datetime, timedelta

def show_countdown(minutes, message="Next check in"):
    """
    Display a countdown timer for the specified number of minutes
    
    Args:
        minutes (int): Number of minutes to countdown
        message (str): Message to display before countdown
    """
    try:
        total_seconds = minutes * 60
        start_time = datetime.now()
        end_time = start_time + timedelta(minutes=minutes)
        
        print(f"\n{message}: {end_time.strftime('%H:%M:%S')}")
        print("=" * 50)
        
        while total_seconds > 0:
            # Calculate remaining time
            remaining = timedelta(seconds=total_seconds)
            hours, remainder = divmod(remaining.seconds, 3600)
            minutes_remaining, seconds = divmod(remainder, 60)
            
            # Format time display
            if hours > 0:
                time_str = f"{hours:02d}:{minutes_remaining:02d}:{seconds:02d}"
            else:
                time_str = f"{minutes_remaining:02d}:{seconds:02d}"
            
            # Display countdown
            print(f"\r⏰ Countdown: {time_str} remaining...", end="", flush=True)
            
            # Sleep for 1 second
            time.sleep(1)
            total_seconds -= 1
            
            # Check for keyboard interrupt
            if total_seconds % 60 == 0:  # Every minute
                try:
                    # Non-blocking check for keyboard interrupt
                    pass
                except KeyboardInterrupt:
                    print("\n\n⏹️ Countdown interrupted by user")
                    return False
        
        print(f"\n✅ Countdown complete! Next check at {datetime.now().strftime('%H:%M:%S')}")
        return True
        
    except KeyboardInterrupt:
        print("\n\n⏹️ Countdown interrupted by user")
        return False
    except Exception as e:
        print(f"\n❌ Error in countdown: {e}")
        return False

def show_simple_countdown(seconds, message="Waiting"):
    """
    Display a simple countdown for the specified number of seconds
    
    Args:
        seconds (int): Number of seconds to countdown
        message (str): Message to display
    """
    try:
        print(f"\n{message}...")
        
        for i in range(seconds, 0, -1):
            print(f"\r⏰ {message}: {i} seconds...", end="", flush=True)
            time.sleep(1)
            
            # Check for keyboard interrupt
            if i % 10 == 0:  # Every 10 seconds
                try:
                    pass
                except KeyboardInterrupt:
                    print("\n\n⏹️ Countdown interrupted by user")
                    return False
        
        print(f"\n✅ {message} complete!")
        return True
        
    except KeyboardInterrupt:
        print("\n\n⏹️ Countdown interrupted by user")
        return False
    except Exception as e:
        print(f"\n❌ Error in countdown: {e}")
        return False

def format_time_remaining(seconds):
    """
    Format remaining time in a human-readable format
    
    Args:
        seconds (int): Number of seconds remaining
        
    Returns:
        str: Formatted time string
    """
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        minutes = seconds // 60
        remaining_seconds = seconds % 60
        return f"{minutes}m {remaining_seconds}s"
    else:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return f"{hours}h {minutes}m"

if __name__ == "__main__":
    # Test the countdown timer
    print("Testing countdown timer...")
    show_countdown(1, "Test countdown") 