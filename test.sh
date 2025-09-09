#!/bin/bash

# Basic rofi menu with initial selection
options="Option 1\nOption 2\nOption 3\nOption 4"

selected=$(echo -e "$options" | rofi -dmenu \
    -selected-row 2 \
    -lines 4 \
    -no-fixed-num-lines \
    -hover-select -me-select-entry '' -me-accept-entry MousePrimary \
    -auto-select \
    -kb-accept-entry "Return,space" \
    -theme-str 'window {width: 300px;} listview {scrollbar: false;} inputbar {enabled: false;}')

echo "You selected: $selected"