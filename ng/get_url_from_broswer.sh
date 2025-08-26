#!/bin/bash
# Simple shell script to get URL from active browser

# Method 1: Using clipboard
get_url_clipboard() {
    # Save current clipboard
    original=$(xclip -selection clipboard -o 2>/dev/null || echo "")
    
    # Focus address bar and copy URL
    xdotool key ctrl+l
    sleep 0.1
    xdotool key ctrl+c
    sleep 0.2
    
    # Get URL from clipboard
    url=$(xclip -selection clipboard -o 2>/dev/null)
    
    # Restore original clipboard
    if [ -n "$original" ]; then
        echo -n "$original" | xclip -selection clipboard
    fi
    
    # Check if it's a valid URL
    if [[ $url =~ ^https?:// ]]; then
        echo "$url"
        return 0
    else
        return 1
    fi
}

# Method 2: Using window title analysis (less reliable)
get_url_from_title() {
    title=$(xdotool getactivewindow getwindowname 2>/dev/null)
    
    # Extract URL patterns from window title
    if [[ $title =~ https?://[^[:space:]]+ ]]; then
        echo "${BASH_REMATCH[0]}"
        return 0
    fi
    
    return 1
}

# Main function
main() {
    echo "Getting URL from active browser window..."
    
    # Check if browser is active
    title=$(xdotool getactivewindow getwindowname 2>/dev/null)
    if [[ ! $title =~ (Firefox|Chrome|Chromium|Safari|Edge|Opera|Brave) ]]; then
        echo "Warning: Active window doesn't appear to be a browser" >&2
    fi
    
    # Try clipboard method first
    if url=$(get_url_clipboard); then
        echo "URL: $url"
        
        # Optionally copy to a specific clipboard selection
        echo -n "$url" | xclip -selection primary
        echo "URL copied to primary selection"
        
        exit 0
    fi
    
    # Try title method as fallback
    if url=$(get_url_from_title); then
        echo "URL (from title): $url"
        exit 0
    fi
    
    echo "Failed to get URL from browser" >&2
    exit 1
}

# Run main function
main "$@"