from flask import Flask, request, jsonify

import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.layers import Input
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

app = Flask(__name__)


max_sequence_length = 250
code_input = Input(shape=(max_sequence_length,), name='code_input')
tokenizer = Tokenizer(num_words=10000, oov_token="<OOV>")
loaded_model = tf.keras.models.load_model('AI Hackathon')
vulnerability_labels = []
@app.route('/predict', methods=['POST'])
def predict():
    user_input = request.form['code']
    preprocessed_data = preprocessing(user_input)
    postprocessed_data = postprocessing(preprocessed_data)
    return jsonify({'predictions':postprocessed_data})
    
if __name__ == "__main__":
    app.run(debug=True)

testing_input = [
    """use solana_program::{program::invoke_signed, instruction::Instruction, account_info::AccountInfo};

pub fn test_unsafe_cpi_without_check(instruction: &Instruction, accounts: &[AccountInfo], signers_seeds: &[&[&[u8]]]) {
    // Test: Executes a CPI without checking the result, risking silent failures
    let _ = invoke_signed(instruction, accounts, signers_seeds);
}
""",
"""use solana_program::{program::invoke_signed, instruction::Instruction, account_info::AccountInfo, entrypoint::ProgramResult};

pub fn test_safe_cpi_with_check(instruction: &Instruction, accounts: &[AccountInfo], signers_seeds: &[&[&[u8]]]) -> ProgramResult {
    // Test: Properly checks the result of the CPI to handle potential errors
    invoke_signed(instruction, accounts, signers_seeds)?;
    Ok(())
}
""",
"""pub fn test_unsafe_instruction_data_handling(data: &[u8]) {
    // Test: Processes instruction data without ensuring it's of expected length
    let _command = data[0];
}
""",
"""use solana_program::{entrypoint::ProgramResult, program_error::ProgramError};

pub fn test_safe_instruction_data_handling(data: &[u8]) -> ProgramResult {
    // Test: Validates the instruction data length before processing
    if data.len() < 1 {
        return Err(ProgramError::InvalidInstructionData);
    }
    let _command = data[0];
    Ok(())
}
""",
"""use solana_program::{account_info::AccountInfo, pubkey::Pubkey};

pub fn test_unsafe_account_ownership_verification(account: &AccountInfo, owner: &Pubkey) {
    // Test: Assumes account ownership matches without verification
    let _is_owned_by = account.owner == owner;
}
""",
"""use solana_program::{account_info::AccountInfo, pubkey::Pubkey, entrypoint::ProgramResult, program_error::ProgramError};

pub fn test_safe_account_ownership_verification(account: &AccountInfo, owner: &Pubkey) -> ProgramResult {
    // Test: Verifies account ownership against the provided owner pubkey
    if account.owner != owner {
        return Err(ProgramError::IllegalOwner);
    }
    Ok(())
}
""",
"""use solana_program::account_info::AccountInfo;

pub fn test_unsafe_signature_presence_check(account: &AccountInfo) {
    // Test: Executes critical action without verifying if the account provided a signature
    let _is_signer = account.is_signer;
}
""",
"""use solana_program::{account_info::AccountInfo, entrypoint::ProgramResult, program_error::ProgramError};

pub fn test_safe_signature_presence_check(account: &AccountInfo) -> ProgramResult {
    // Test: Ensures the account has signed the transaction before proceeding
    if !account.is_signer {
        return Err(ProgramError::MissingRequiredSignature);
    }
    Ok(())
}
""",
"""use solana_program::account_info::AccountInfo;

pub fn test_unsafe_lamport_adjustment(account: &AccountInfo) {
    // Test: Adjusts lamports without any checks for underflow or account state
    **account.lamports.borrow_mut() -= 500; // Risks underflow and state inconsistency
}
""",
"""use solana_program::{account_info::AccountInfo, entrypoint::ProgramResult, program_error::ProgramError};

pub fn test_safe_lamport_adjustment(account: &AccountInfo) -> ProgramResult {
    // Test: Carefully adjusts lamports with checks to prevent underflow
    let lamports = **account.lamports.borrow();
    if lamports < 500 {
        return Err(ProgramError::InsufficientFunds);
    }
    **account.lamports.borrow_mut() -= 500;
    Ok(())
}
"""
]

def preprocessing(user_input):
    tokenized_input = tokenizer.texts_to_sequences(user_input)
    padd_sequence = pad_sequences(tokenized_input,maxlen=max_sequence_length, padding='post')
    predictions = loaded_model.predict(padd_sequence)
    return predictions

def postprocessing(predictions_prob):
    for i in range(predictions_prob):
        vulnerability_labels[i] = predictions_prob[i]
    return vulnerability_labels
