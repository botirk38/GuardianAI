from openai import OpenAI
import grpc
from concurrent import futures
import Open_servce_pb2
import Open_servce_pb2_grpc

# Initialize OpenAI client
openai = OpenAI()


class AnalyzerServicer(Open_servce_pb2_grpc.AnalyzerServicer):
    def AnalyzeContract(self, request, context):
        try:
            prompt = f"Find vulnerabilities in the following Rust smart contract code and generate a report:\n\n{request.features_json}"
            response = openai.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant. smart contract code vulnerability detection."},
                    {"role": "user", "content": prompt}
                ]
            )
            result = response.choices[0].message.content
            return Open_servce_pb2.AnalyzeResponse(vulnerabilities_json=result)
        except Exception as e:
            error_msg = f"An error occured {e}"
            return Open_servce_pb2.AnalyzeResponse(vulnerabilities_json=error_msg)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    Open_servce_pb2_grpc.add_AnalyzerServicer_to_server(
        AnalyzerServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started")
    server.wait_for_termination()


if __name__ == '__main__':
    serve()

