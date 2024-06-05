from transformers import AutoTokenizer, AutoModel
import torch

def load_model():
    tokenizer = AutoTokenizer.from_pretrained("microsoft/codebert-base")
    model = AutoModel.from_pretrained("microsoft/codebert-base")
    return tokenizer, model
# Import necessary libraries from the Hugging Face `transformers` package and PyTorch

def prepare_input(tokenizer, code_snippet):
    return tokenizer(code_snippet, return_tensors="pt", max_length=512, truncation=True, padding="max_length")

def get_embeddings(model, inputs):
    with torch.no_grad(): 
        outputs = model(**inputs)
        return outputs.last_hidden_state

def main():

    tokenizer, model = load_model()
    code_snippet = """function withdraw() public { 
        uint amount = balances[msg.sender]; 
        require(msg.sender.call.value(amount)()); 
        balances[msg.sender] = 0; 
    }"""
    inputs = prepare_input(tokenizer, code_snippet)
    embeddings = get_embeddings(model, inputs)
    print(embeddings)


if __name__ == "__main__":
    main()
