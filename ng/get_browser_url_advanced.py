#!/usr/bin/env python3
"""
Advanced browser URL extraction with browser-specific methods.
"""

import subprocess
import json
import os
import sqlite3
import time
from pathlib import Path
from typing import Optional, Dict, List

def get_chrome_current_url() -> Optional[str]:
    """Get current URL from Chrome using remote debugging."""
    try:
        # Check if Chrome debug port is accessible
        result = subprocess.run([
            'curl', '-s', 'http://localhost:9222/json/tabs'
        ], capture_output=True, text=True, timeout=2)
        
        if result.returncode == 0:
            tabs = json.loads(result.stdout)
            # Find active tab
            for tab in tabs:
                if tab.get('active', False):
                    return tab.get('url')
    except Exception as e:
        print(f"Chrome remote debugging failed: {e}")
    
    return None

def get_firefox_current_url() -> Optional[str]:
    """Get current URL from Firefox using places database (last visited)."""
    try:
        # Firefox profile directory
        firefox_dir = Path.home() / '.mozilla' / 'firefox'
        if not firefox_dir.exists():
            return None
        
        # Find default profile
        profiles = list(firefox_dir.glob('*.default*'))
        if not profiles:
            return None
        
        places_db = profiles[0] / 'places.sqlite'
        if not places_db.exists():
            return None
        
        # Copy database to avoid locking issues
        temp_db = '/tmp/places_temp.sqlite'
        subprocess.run(['cp', str(places_db), temp_db], check=True)
        
        # Query recent URLs
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT url FROM moz_places 
            WHERE last_visit_date IS NOT NULL 
            ORDER BY last_visit_date DESC 
            LIMIT 1
        """)
        
        result = cursor.fetchone()
        conn.close()
        
        # Clean up
        os.remove(temp_db)
        
        return result[0] if result else None
        
    except Exception as e:
        print(f"Firefox database method failed: {e}")
        return None

def get_active_window_info() -> Dict[str, str]:
    """Get detailed info about active window."""
    try:
        # Get window ID
        window_id = subprocess.check_output(
            ['xdotool', 'getactivewindow'], stderr=subprocess.DEVNULL
        ).decode().strip()
        
        # Get window name
        window_name = subprocess.check_output(
            ['xdotool', 'getwindowname', window_id], stderr=subprocess.DEVNULL
        ).decode().strip()
        
        # Get process name
        pid = subprocess.check_output(
            ['xdotool', 'getwindowpid', window_id], stderr=subprocess.DEVNULL
        ).decode().strip()
        
        process_name = subprocess.check_output(
            ['ps', '-p', pid, '-o', 'comm='], stderr=subprocess.DEVNULL
        ).decode().strip()
        
        return {
            'window_id': window_id,
            'window_name': window_name,
            'pid': pid,
            'process_name': process_name
        }
        
    except Exception as e:
        print(f"Failed to get window info: {e}")
        return {}

def detect_browser_type() -> Optional[str]:
    """Detect which browser is currently active."""
    info = get_active_window_info()
    process_name = info.get('process_name', '').lower()
    window_name = info.get('window_name', '').lower()
    
    if 'firefox' in process_name or 'firefox' in window_name:
        return 'firefox'
    elif 'chrome' in process_name or 'chromium' in process_name:
        return 'chrome'
    elif 'brave' in process_name:
        return 'brave'
    elif 'opera' in process_name:
        return 'opera'
    elif 'edge' in process_name:
        return 'edge'
    
    return None

def get_url_browser_specific() -> Optional[str]:
    """Try browser-specific methods to get current URL."""
    browser = detect_browser_type()
    print(f"Detected browser: {browser}")
    
    if browser == 'chrome':
        return get_chrome_current_url()
    elif browser == 'firefox':
        return get_firefox_current_url()
    
    return None

def get_current_browser_url_advanced() -> Optional[str]:
    """
    Advanced method combining multiple approaches.
    
    Returns:
        str: Current browser URL or None if failed
    """
    # Method 1: Try browser-specific methods
    url = get_url_browser_specific()
    if url:
        return url
    
    # Method 2: Fallback to clipboard method
    from get_browser_url import get_current_browser_url
    return get_current_browser_url()

def test_advanced():
    """Test the advanced URL extraction."""
    print("🔍 Advanced Browser URL Detection")
    print("=" * 40)
    
    # Show window info
    info = get_active_window_info()
    print(f"Active window: {info.get('window_name', 'Unknown')}")
    print(f"Process: {info.get('process_name', 'Unknown')}")
    
    # Detect browser
    browser = detect_browser_type()
    print(f"Browser type: {browser}")
    
    # Try to get URL
    url = get_current_browser_url_advanced()
    if url:
        print(f"📍 Current URL: {url}")
    else:
        print("❌ Failed to extract URL")

if __name__ == '__main__':
    test_advanced()