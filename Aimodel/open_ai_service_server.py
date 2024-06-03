import grpc
from concurrent import futures
import Open_servce_pb2
import Open_servce_pb2_grpc

class OpenAIServiceServicer(Open_servce_pb2_grpc.OpenAIServiceServicer):
    def AnalyzeCode(self, request, context):
        result = request.code + " has 0 vulnerabilities"
        return Open_servce_pb2.AnalyzeCodeResponse(vulnerabilities=result)
        

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    Open_servce_pb2_grpc.add_OpenAIServiceServicer_to_server(OpenAIServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()