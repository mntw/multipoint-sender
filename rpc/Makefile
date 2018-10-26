all:
	proto
proto:
	python -m grpc_tools.protoc -I./ --python_out=. --grpc_python_out=. multisend.proto
clean:
	rm *.pyc


