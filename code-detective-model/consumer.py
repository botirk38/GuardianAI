from aiokafka import AIOKafkaConsumer
import json
import openai  # Ensure you have your OpenAI API key configured
from websocket_server import send_message


def detect_vulnerabilities(code_features):
    try:
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

        return result
    except Exception as e:
        error_msg = f"An error occurred: {e}"
        print(error_msg)
        return error_msg


async def consume():
    consumer = AIOKafkaConsumer(
        'code-analysis-requests',
        bootstrap_servers='localhost:9092',
        group_id="analysis-group"
    )
    await consumer.start()
    print("Consumer started")
    try:
        async for msg in consumer:
            request = json.loads(msg.value.decode('utf-8'))
            print(request)
            analysis_request = request.get("code_features", "")
            request_id = request.get("request_id", "")
            if analysis_request and request_id:
                vulnerabilities = detect_vulnerabilities(analysis_request)
                response_message = json.dumps(
                    {"request_id": request_id, "vulnerabilities": vulnerabilities})
                await send_message(request_id, response_message)
    finally:
        await consumer.stop()

