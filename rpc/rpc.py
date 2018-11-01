import grpc
import multisend_pb2 as pb2
import multisend_pb2_grpc as pb2_grpc

class Client():
    def __init__ (self, grpcIP, grpcPort, params):
        self.channel =  grpc.insecure_channel('%s:%d' % (grpcIP, grpcPort))
        self.stub = pb2_grpc.ApiStub(self.channel)
        self.params = params
    def StartSender(self):
        params = pb2.Parameters(**self.params)
        res = self.stub.StartSender(params)
        print (res)
    def Shutdown(self):
        res = self.stub.Shutdown(pb2.Void())
    def close():
        self.channel.close()

msg = {
        'socket' : True,
        'sndr_address' : 'localhost:505050',
        'list' : ['localhost:1','localhost:2','localhost:3','localhost:4','localhost:5'],
        }

obj = Client('localhost', 50051, msg)
obj.StartSender()
