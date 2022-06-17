#!/bin/bash
cd /home/pi
tmux new-session -d -s test
test=$(tmux list-sessions | grep rpi)
if [ "$SESSIONEXISTS" = "" ];then
	sh scripts/createTmuxTesting.sh
else
        echo "Exitst"
fi
tmux kill-session -t test
