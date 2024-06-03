import sys
sys.path.insert(0, '../')
import grpc
import Open_servce_pb2
import Open_servce_pb2_grpc

def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = Open_servce_pb2_grpc.OpenAIServiceStub(channel)
    request = Open_servce_pb2.AnalyzeCodeRequest(code="Your test code here")
    response = stub.AnalyzeCode(request)
    print(response)

if __name__ == '__main__':
    run()