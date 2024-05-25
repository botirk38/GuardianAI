from transformers import AutoTokenizer, AutoModel
import torch

def load_model():
    tokenizer = AutoTokenizer.from_pretrained("microsoft/codebert-base")
    model = AutoModel.from_pretrained("microsoft/codebert-base")
    return tokenizer, model
# Import necessary libraries from the Hugging Face `transformers` package and PyTorch

def prepare_input(tokenizer, code_snippet):
    # Tokenize the code snippet using the loaded tokenizer
    # 'return_tensors="pt"' tells the tokenizer to return PyTorch tensors
    # 'max_length=512' ensures that the input is no longer than 512 tokens
    # 'truncation=True' truncates the inputs to max_length if they are longer
    # 'padding="max_length"' pads the sequence to exactly 512 tokens
    return tokenizer(code_snippet, return_tensors="pt", max_length=512, truncation=True, padding="max_length")

def get_embeddings(model, inputs):
    # Disable gradient calculation to save memory and computation since we're only doing inference
    # This passes the tokenized input through the model and obtains the last hidden state (embeddings)
    with torch.no_grad(): 
        outputs = model(**inputs)
        return outputs.last_hidden_state

def main():
    # Initialize the tokenizer and model
    tokenizer, model = load_model()
    
    # Example code snippet that potentially contains a vulnerability
    code_snippet = """function withdraw() public { 
        uint amount = balances[msg.sender]; 
        require(msg.sender.call.value(amount)()); 
        balances[msg.sender] = 0; 
    }"""
    
    # Prepare the input data
    inputs = prepare_input(tokenizer, code_snippet)
    
    # Get the embeddings for the code snippet
    embeddings = get_embeddings(model, inputs)
    
    # Print out the embeddings (tensor) to see the output
    print(embeddings)

# This line checks if this script is being run as the main program and prevents the code from being run if the script is imported as a module
if __name__ == "__main__":
    main()
