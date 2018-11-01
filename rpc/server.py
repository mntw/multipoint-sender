import grpc
import multisend_pb2 as pb2
import multisend_pb2_grpc as pb2_grpc
from concurrent import futures
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool
import subprocess, time

class ApiServicer(pb2_grpc.ApiServicer):
    def StartSender(self, request, context):
        isSocket = request.socket
        source_address = request.sndr_address
        ReceiverList = request.list
        print(isSocket)
        print(source_address)
        print(ReceiverList)
        return pb2.Status(ok=True)

def Serve():
    print('server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))')
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    print('pb2_grpc.add_ApiServicer_to_server(ApiServicer(), server)')
    pb2_grpc.add_ApiServicer_to_server(ApiServicer(), server)
    print('server.add_insecure_port(\'[::]:50051\')')
    server.add_insecure_port('[::]:%d' % 50051)
    print('server.start()')
    server.start()
    try:
        while True: time.sleep(30)
    except KeyboardInterrupt:
        server.stop(0)


Serve()
