import grpc
import multisend_pb2 as pb2
import multisend_pb2_grpc as pb2_grpc
from multiprocessing.dummy import Pool as ThreadPool

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
    def close(self):
        self.channel.close()

msg = {
        'socket' : False,
        'sndr_address' : 'localhost:8880',
        'list' : ['localhost:8881', 'localhost:8882', 'localhost:8883'],
        }
msgs = [msg] * 4
msgs[0]['list'] = ['localhost:8881']
msgs[1] = {
        'socket' : True,
        'sndr_address' : 'localhost:8881',
        'list' : ['localhost:8882'],
}
msgs[2] = {
        'socket' : True,
        'sndr_address' : 'localhost:8882',
        'list' : ['localhost:8883'],
}
msgs[3] = {
        'socket' : True,
        'sndr_address' : 'localhost:8883',
        'list' : [],
}

#obj = Client('localhost', 50051, msg)
#obj.StartSender()

objs = [
    Client('localhost', 50052, msgs[1]),
    Client('localhost', 50053, msgs[2]),
    Client('localhost', 50054, msgs[3]),
    Client('localhost', 50051, msgs[0])
]



pool = ThreadPool(processes = len(objs))
results = pool.map(lambda x : x.StartSender(), objs)
pool.close()
pool.join()

map(lambda x : x.close(), objs)

