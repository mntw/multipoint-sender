all: tmux

chain:
	fallocate -l 300M 300M
	tmux new -s "run" -d
	tmux split-window -h -p 50
	tmux send-keys "./multisend.py -s -p 8881 -fs 300 -st -H localhost:8882 -df ./300M-8881" C-m
	tmux split-window -v -p 50
	tmux send-keys "./multisend.py -s -p 8882 -fs 300 -st -H localhost:8883 -df ./300M-8882" C-m
	tmux select-pane -t 0
	tmux split-window -v -p 50
	tmux send-keys "./multisend.py -s -p 8883 -fs 300 -st -df ./300M-8883" C-m
	tmux select-pane -t 0
	sleep 2
	tmux send-keys "./multisend.py -sf ./300M -fs 300 -st -H localhost:8881" C-m
	tmux attach -t "run"
mp:
	fallocate -l 300M 300M
	tmux new -s "run" -d
	tmux split-window -h -p 50
	tmux send-keys "nc -l 8881 | pv -b > 300M-8881" C-m
	tmux split-window -v -p 50
	tmux send-keys "nc -l 8882 | pv -b > 300M-8882" C-m
	tmux select-pane -t 0
	tmux split-window -v -p 50
	tmux send-keys "nc -l 8883 | pv -b > 300M-8883" C-m
	tmux select-pane -t 0
	sleep 2
	tmux send-keys "./multisend.py -sf ./300M -fs 300 -st -H localhost:8881 localhost:8882 localhost:8883" C-m
	tmux attach -t "run"

