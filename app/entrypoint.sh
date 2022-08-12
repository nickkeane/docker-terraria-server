#!/bin/sh

pipe=/tmp/tmod.out
players=/tmp/tmod.players.out

function shutdown() {
  # Post Shutdown Message and Shutdown Server Safely
  [ -n "$TMOD_SHUTDOWN_MSG" ] && tmod-send-cmd "say $TMOD_SHUTDOWN_MSG"
  tmod-send-cmd "exit"
  tmuxPid=$(pgrep tmux)
  tmodPid=$(pgrep --parent $tmuxPid Main)
  while [ -e /proc/$tmodPid ]; do
    sleep .5
  done
  rm $pipe
}

#server="/opt/terraria/tModLoaderServer.bin.x86_64" # TODO: Old, use tMod sh script instead
server="/opt/terraria/start-tModLoaderServer.sh"

if [ "$1" = "setup" ]; then
  $server
else
  # Enable Signal Traps
  trap shutdown SIGTERM SIGINT

  # Schedule Autosave Task
  #saveMsg='Autosave - $(date +"%Y-%m-%d %T")'
  #if [ ! -z "$TMOD_AUTOSAVE_INTERVAL" ] && ! crontab -l | grep -q "Autosave"; then
  #  (crontab -l 2>/dev/null; echo "$TMOD_AUTOSAVE_INTERVAL echo \"$saveMsg\" > $pipe && tmod-send-cmd save") | crontab -
  #fi

  # TODO: Schedule World Backup Task

  # Fire up Server
  mkfifo $pipe
  tmux new-session -d "$server -config serverconfig.txt | tee $pipe $players" &
#  sleep 2 && tmod-send-cmd "y"
#  sleep 2 && tmod-send-cmd "f"
  sleep 60 && /usr/sbin/crond -d 8 &
  cat $pipe &

  wait ${!}
fi