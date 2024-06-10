import os
import json
import grpc
from concurrent import futures
from openai import OpenAI
import Open_servce_pb2
import Open_servce_pb2_grpc

# Initialize OpenAI client
openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class AnalyzerServicer(Open_servce_pb2_grpc.AnalyzerServicer):
    def AnalyzeContract(self, request, context):
        try:
            # Deserialize the JSON request
            code_features = json.loads(request.features_json)

            # Create a detailed prompt
            prompt_sections = {
                "Possible Overflow Statements": code_features.get('possible_overflow_statements', []),
                "Possible Underflow Statements": code_features.get('possible_underflow_statements', []),
                "Possible Reentrancy Statements": code_features.get('possible_reentrancy_statements', []),
                "Possible Authority Vulnerabilities": code_features.get('possible_authority_vulnerabilities', []),
                "Possible Signature Vulnerabilities": code_features.get('possible_signature_vulnerabilities', []),
                "Possible Frozen Account Vulnerabilities": code_features.get('possible_frozen_account_vulnerabilities', []),
                "Structs": code_features.get('structs', []),
                "Static Variables": code_features.get('static_variables', []),
                "Enums": code_features.get('enums', []),
            }

            prompt = "Analyze the following Rust smart contract code for vulnerabilities and generate a JSON report with snippets of vulnerable code and their fixes:\n\n"
            for title, items in prompt_sections.items():
                if items:
                    prompt += f"{title}:\n" + \
                        "\n".join(f"- {item}" for item in items) + "\n"

            prompt += ("\nGenerate a JSON with an array 'snippets' where each 'snippet' is a JSON object "
                       "with attributes 'code' containing the vulnerable code formatted correctly with the spacing corrected, 'fixes' "
                       "containing the code snippet with fixes for the vulnerability, and 'description' "
                       "containing the description for each vulnerability. Your response should be only the JSON you generate.")

            # Make the OpenAI API call
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant for smart contract code vulnerability detection."},
                    {"role": "user", "content": prompt}
                ]
            )

            result = response.choices[0].message.content
            result = result.strip('```json').strip().strip('```')

            return Open_servce_pb2.AnalyzeResponse(vulnerabilities_json=result)
        except Exception as e:
            error_msg = f"An error occurred: {e}"
            print(error_msg)
            return Open_servce_pb2.AnalyzeResponse(vulnerabilities_json=json.dumps({"error": error_msg}))


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

