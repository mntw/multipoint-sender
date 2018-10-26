import grpc, 
import multisend_pb2 as pb2
import multisend_pb2_grpc as pb2_grpc

class Client():
    def __init__ (self, grpcIP, grpcPort, sender_params, rcvrs_params):
        self.channel =  grpc.insecure_channel('%s:%d' % (grpcIP, grpcPort))
        self.stub = pb2_grpc.ApiStub(self.channel)
        self.rcvrs_params  = rcvrs_params
        self.sender_params = sender_params
    def StartSender(self):
        res = self.stub.StartSender(self.sender_params)
        print (res)
        self.AddReceivers()
    def SendFile(self, path, recursive=True):
        res = self.stub.SendFile(pb2.Path(path=path, recursive=recursive))
        for i in res:
            print i
    def AddReceivers(self):
        res = self.stub.AddReceivers(pb2.ReceiverList(receivers=self.rcvrs_params))
        for i in res:
            print i
    def Shutdown(self):
        res = self.stub.Shutdown(pb2.Void())
    def close():
        self.channel.close()

def makeReceiver(peer_id, host):
    hostPort = host + ':8849'
    return {
        'id': peer_id,
        'ssh': {'host': host},
        'rcvr_address': hostPort,
        'args': {
            'bin_path': './mts',
            'df': './'
        }
    }

rmdt_params = [makeReceiver(2, '192.168.0.1')]
obj = Client('192.168.0.2', 3205, pb2.Parameters(), rmdt_params)
obj.StartSender()
obj.SendFile(path='./1G')
obj.Shutdown()
