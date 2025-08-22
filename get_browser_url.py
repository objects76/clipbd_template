#!/usr/bin/env python3
"""
Get URL from current active browser window on Ubuntu.
"""

import subprocess
import time
import pyperclip
import re
from typing import Optional

def get_current_url_via_clipboard() -> str|None:
    """Get URL by copying from address bar using Ctrl+L, Ctrl+C."""
    try:
        # Save current clipboard content
        original_clipboard = pyperclip.paste()

        # Focus on address bar and copy URL
        subprocess.run(['xdotool', 'key', 'ctrl+l'], check=True)  # Focus address bar
        time.sleep(0.1)  # Small delay
        subprocess.run(['xdotool', 'key', 'ctrl+c'], check=True)  # Copy URL
        time.sleep(0.1)  # Small delay

        # Get the copied URL
        url = pyperclip.paste().strip()

        # Restore original clipboard
        pyperclip.copy(original_clipboard)

        # Validate URL format
        if url.startswith(('http://', 'https://', 'ftp://')):
            return url
        else:
            return None

    except Exception as e:
        print(f"Clipboard method failed: {e}")
        return None

def get_current_url_via_xclip() -> str|None:
    """Alternative method using xclip directly."""
    try:
        # Save current clipboard
        try:
            original = subprocess.check_output(['xclip', '-selection', 'clipboard', '-o'],
                                             stderr=subprocess.DEVNULL).decode('utf-8')
        except:
            original = ""

        # Focus address bar and copy
        subprocess.run(['xdotool', 'key', 'ctrl+l'], check=True)
        time.sleep(0.1)
        subprocess.run(['xdotool', 'key', 'ctrl+c'], check=True)
        time.sleep(0.2)

        # Get URL from clipboard
        url = subprocess.check_output(['xclip', '-selection', 'clipboard', '-o']).decode('utf-8').strip()

        # Restore clipboard
        if original:
            subprocess.run(['xclip', '-selection', 'clipboard'],
                         input=original.encode('utf-8'), check=True)

        if url.startswith(('http://', 'https://', 'ftp://')):
            return url
        return None

    except Exception as e:
        print(f"xclip method failed: {e}")
        return None

def get_browser_window_title() -> str|None:
    """Get the title of the active window to identify browser."""
    try:
        result = subprocess.check_output(['xdotool', 'getactivewindow', 'getwindowname'],
                                       stderr=subprocess.DEVNULL)
        return result.decode('utf-8').strip()
    except:
        return None

def is_browser_active() -> bool:
    """Check if current active window is a browser."""
    title = get_browser_window_title()
    if not title:
        return False

    browser_indicators = [
        'Mozilla Firefox', 'Google Chrome', 'Chromium', 'Safari',
        'Edge', 'Opera', 'Brave', 'Vivaldi', 'Firefox'
    ]

    return any(browser in title for browser in browser_indicators)

def get_current_browser_url() -> str|None:
    """
    Main function to get URL from active browser window.

    Returns:
        str: Current browser URL or None if failed
    """
    # Check if a browser is active
    if not is_browser_active():
        print("No browser window appears to be active")
        return None

    return get_current_url_via_clipboard()

import time
def test():
    """Test the URL extraction."""
    print("🔍 Getting URL from active browser window...")
    print("Make sure a browser window is active and focused.")

    the_url = None
    while True:
        window_title = get_browser_window_title()

        if is_browser_active():
            url = get_current_browser_url()
            if url and url != the_url:
                print(f"Active window: {window_title}")
                print(f"📍 Current URL: {url}")
                the_url = url
        time.sleep(1)

if __name__ == '__main__':
    test()