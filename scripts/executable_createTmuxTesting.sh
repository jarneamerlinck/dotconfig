cd /home/pi
tmux new-session -d -s rpi \; \
	send-keys 'clear'  C-m \; \
	rename-window -t 0 Main \; \
	new-window -n Overview \; \
	split-window -v -p 30 \; \
	select-pane -t 0 \; \
	split-window -v -p 25 \; \
	select-pane -t 0 \; \
	send-keys 'top' C-m \; \
	split-window -h -p 25 \; \
	select-window -t 1 \; \
	select-pane -t 2 \; \
	send-keys 'ls -ia' C-m \; \
	select-pane -t 3 \; \
	split-pane -h -p 50 \; \
	select-pane -t 3 \; \
	send-keys 'echo "wip"' C-m \; \
	select-pane -t 4 \; \
	send-keys 'echo "wip2"' C-m \; \
	select-pane -t 1 \; \
	send-keys 'clear' C-m \; \
	send-keys 'who | grep -v "tmux"' C-m \; \
	select-pane -t 0 \;


