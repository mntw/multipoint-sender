# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import multisend_pb2 as multisend__pb2


class ApiStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.StartSender = channel.unary_unary(
        '/proto.Api/StartSender',
        request_serializer=multisend__pb2.Parameters.SerializeToString,
        response_deserializer=multisend__pb2.Status.FromString,
        )
    self.SendFile = channel.unary_stream(
        '/proto.Api/SendFile',
        request_serializer=multisend__pb2.Path.SerializeToString,
        response_deserializer=multisend__pb2.Status.FromString,
        )
    self.AddReceivers = channel.unary_stream(
        '/proto.Api/AddReceivers',
        request_serializer=multisend__pb2.ReceiverList.SerializeToString,
        response_deserializer=multisend__pb2.ReceiverReply.FromString,
        )
    self.Shutdown = channel.unary_unary(
        '/proto.Api/Shutdown',
        request_serializer=multisend__pb2.Void.SerializeToString,
        response_deserializer=multisend__pb2.Void.FromString,
        )


class ApiServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def StartSender(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def SendFile(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def AddReceivers(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def Shutdown(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_ApiServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'StartSender': grpc.unary_unary_rpc_method_handler(
          servicer.StartSender,
          request_deserializer=multisend__pb2.Parameters.FromString,
          response_serializer=multisend__pb2.Status.SerializeToString,
      ),
      'SendFile': grpc.unary_stream_rpc_method_handler(
          servicer.SendFile,
          request_deserializer=multisend__pb2.Path.FromString,
          response_serializer=multisend__pb2.Status.SerializeToString,
      ),
      'AddReceivers': grpc.unary_stream_rpc_method_handler(
          servicer.AddReceivers,
          request_deserializer=multisend__pb2.ReceiverList.FromString,
          response_serializer=multisend__pb2.ReceiverReply.SerializeToString,
      ),
      'Shutdown': grpc.unary_unary_rpc_method_handler(
          servicer.Shutdown,
          request_deserializer=multisend__pb2.Void.FromString,
          response_serializer=multisend__pb2.Void.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'proto.Api', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
