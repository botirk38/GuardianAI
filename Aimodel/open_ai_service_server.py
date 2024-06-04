from openai import OpenAI, ChatCompletion
import grpc
from concurrent import futures
import Open_servce_pb2
import Open_servce_pb2_grpc
import os

openai = OpenAI()
class OpenAIServiceServicer(Open_servce_pb2_grpc.OpenAIServiceServicer):
    def AnalyzeCode(self, request, context):
        try:
            prompt = f"Find vulnerabilities in the following Rust smart contract code and generate a report:\n\n{request.code}"
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant. smart contract code vulnerability detection."},
                    {"role": "user", "content": prompt}
                ]
            )
            result = response.choices[0].message.content
            return Open_servce_pb2.AnalyzeCodeResponse(vulnerabilities=result)
        
        except Exception as e:
            print(f"An error occurred: {e}")
            return Open_servce_pb2.AnalyzeCodeResponse(vulnerabilities="Error occurred during analysis")
        
        

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    Open_servce_pb2_grpc.add_OpenAIServiceServicer_to_server(OpenAIServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()