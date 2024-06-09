from openai import OpenAI, ChatCompletion
import grpc
from concurrent import futures
import Open_servce_pb2
import Open_servce_pb2_grpc
import os

# Initialize OpenAI client
openai = OpenAI()
class AnalyzerServicer(Open_servce_pb2_grpc.AnalyzerServicer):
    # Define the AnalyzeCode method, which takes a request containing Rust smart contract code
    def AnalyzeContract(self, request, context):
        try: 
            prompt = f"Find vulnerabilities in the following Rust smart contract code and generate a report:\n\n{request.features_json}"
            # Make the OpenAI API call
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant. smart contract code vulnerability detection."},
                    {"role": "user", "content": prompt}
                ]
            )
            # Extract the result from the response
            print("response")
            result = response.choices[0].message.content
            print(f"Result: {result}")
            return Open_servce_pb2.AnalyzeResponse(vulnerabilities_json=result)
        
        except Exception as e:
            print(f"An error occurred: {e}")
            return Open_servce_pb2.AnalyzeResponse(vulnerabilities_json="Error occurred during analysis")
        
        

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    Open_servce_pb2_grpc.add_AnalyzerServicer_to_server(AnalyzerServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()