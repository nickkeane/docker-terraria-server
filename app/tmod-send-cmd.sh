#!/bin/sh

# Check for existance of world
ls /opt/terraria-home/ModLoader/Worlds/*.wld >/dev/null || exit

# Send command to server
tmux send-keys "$1" Enter
