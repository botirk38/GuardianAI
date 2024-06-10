from openai import OpenAI
import grpc
from concurrent import futures
import Open_servce_pb2
import Open_servce_pb2_grpc
import json

# Initialize OpenAI client
openai = OpenAI()


class AnalyzerServicer(Open_servce_pb2_grpc.AnalyzerServicer):
    def AnalyzeContract(self, request, context):
        try:
            # Deserialize the JSON request
            code_features = json.loads(request.features_json)

            # Create a detailed prompt
            prompt = "Analyze the following Rust smart contract code for vulnerabilities and generate a JSON report with snippets of vulnerable code and their fixes:\n\n"

            def add_section(title, items):
                if items:
                    prompt_section = f"{title}:\n"
                    for item in items:
                        prompt_section += f"- {item}\n"
                    return prompt_section
                return ""

            prompt += add_section("Possible Overflow Statements",
                                  code_features.get('possible_overflow_statements', []))
            prompt += add_section("Possible Underflow Statements",
                                  code_features.get('possible_underflow_statements', []))
            prompt += add_section("Possible Reentrancy Statements",
                                  code_features.get('possible_reentrancy_statements', []))
            prompt += add_section("Possible Authority Vulnerabilities",
                                  code_features.get('possible_authority_vulnerabilities', []))
            prompt += add_section("Possible Signature Vulnerabilities",
                                  code_features.get('possible_signature_vulnerabilities', []))
            prompt += add_section("Possible Frozen Account Vulnerabilities",
                                  code_features.get('possible_frozen_account_vulnerabilities', []))
            prompt += add_section("Structs", code_features.get('structs', []))
            prompt += add_section("Static Variables",
                                  code_features.get('static_variables', []))
            prompt += add_section("Enums", code_features.get('enums', []))

            prompt += "\nGenerate a JSON with 'snippets' containing vulnerable code , 'fixes' containing suggested fixes for each vulnerability , and 'description' containing the description for each vulnerability."
            prompt += "Your response should be only the json you generate."

            # Make the OpenAI API call
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant. smart contract code vulnerability detection."},
                    {"role": "user", "content": prompt}
                ]
            )
            result = response.choices[0].message.content

            return Open_servce_pb2.AnalyzeResponse(vulnerabilities_json=result)
        except Exception as e:
            error_msg = f"An error occurred: {e}"
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

