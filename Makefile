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
grpc-mp:
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
	tmux send-keys "./multisend.py -sf ./300M -fs 300 -st -H localhost:8883 --grpc 50051" C-m
	tmux split-window -v -p 50
	tmux send-keys "python rpc/rpc.py" C-m
	tmux attach -t "run"
grpc-chain:
	fallocate -l 300M 300M
	tmux new -s "run" -d
	tmux split-window -h -p 50
	tmux send-keys "./multisend.py -s -p 8881 -fs 300 -st -df ./300M-8881 --grpc 50052" C-m
	tmux split-window -v -p 50
	tmux send-keys "./multisend.py -s -p 8882 -fs 300 -st -df ./300M-8882 --grpc 50053" C-m
	tmux select-pane -t 0
	tmux split-window -v -p 50
	tmux send-keys "./multisend.py -s -p 8883 -fs 300 -st -df ./300M-8883 --grpc 50054" C-m
	tmux select-pane -t 0
	sleep 2
	tmux send-keys "./multisend.py -sf ./300M -fs 300 -st -H localhost:0 --grpc 50051 " C-m
	tmux split-window -v -p 50
	tmux send-keys "python rpc/rpc.py" C-m
	tmux attach -t "run"
binary: binary_clean compose binary_clean_after

compose:
	mkdir -p bin
	python2.7 -m PyInstaller ./multisend.py --hidden-import=pkg_resources --onefile --distpath bin
binary_clean:
	rm -rf *.spec build *.pyc dist __pycache__ bin 2> /dev/null
binary_clean_after:
	rm -rf *.spec *.pyc build dist __pycache__ 2> /dev/null
proto:
	python -m grpc_tools.protoc -I./ --python_out=. --grpc_python_out=. multisend.proto
proto-clean:
	rm *.pyc
chain_bin:
	fallocate -l 300M 300M
	tmux new -s "run" -d
	tmux split-window -h -p 50
	tmux send-keys "bin/multisend -s -p 8881 -fs 300 -st -H localhost:8882 -df ./300M-8881" C-m
	tmux split-window -v -p 50
	tmux send-keys "bin/multisend -s -p 8882 -fs 300 -st -H localhost:8883 -df ./300M-8882" C-m
	tmux select-pane -t 0
	tmux split-window -v -p 50
	tmux send-keys "bin/multisend -s -p 8883 -fs 300 -st -df ./300M-8883" C-m
	tmux select-pane -t 0
	sleep 2
	tmux send-keys "bin/multisend -sf ./300M -fs 300 -st -H localhost:8881" C-m
	tmux attach -t "run"
grpc-chain-bin:
	fallocate -l 300M 300M
	tmux new -s "run" -d
	tmux split-window -h -p 50
	tmux send-keys "bin/multisend -s -p 8881 -fs 300 -st -df ./300M-8881 --grpc 50052" C-m
	tmux split-window -v -p 50
	tmux send-keys "bin/multisend -s -p 8882 -fs 300 -st -df ./300M-8882 --grpc 50053" C-m
	tmux select-pane -t 0
	tmux split-window -v -p 50
	tmux send-keys "bin/multisend -s -p 8883 -fs 300 -st -df ./300M-8883 --grpc 50054" C-m
	tmux select-pane -t 0
	sleep 2
	tmux send-keys "bin/multisend -sf ./300M -fs 300 -st -H localhost:0 --grpc 50051 " C-m
	tmux split-window -v -p 50
	tmux send-keys "python rpc/rpc.py" C-m
	tmux attach -t "run"
