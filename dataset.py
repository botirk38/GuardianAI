code_snippets = [
    """use solana_program::{
        account_info::{AccountInfo, next_account_info},
        entrypoint::ProgramResult,
    };

    pub fn safe_increment_balance(accounts: &[AccountInfo], amount: u64) -> ProgramResult {
        let accounts_iter = &mut accounts.iter();
        let account = next_account_info(accounts_iter)?;
        **account.try_borrow_mut_lamports()? += amount;
        // Missing error handling for overflow
        Ok(())""",
        """use solana_program::{
        account_info::{AccountInfo, next_account_info},
        entrypoint::ProgramResult,
        program_error::ProgramError,
};

pub fn safe_increment_balance(accounts: &[AccountInfo], amount: u64) -> ProgramResult {
    let accounts_iter = &mut accounts.iter();
    let account = next_account_info(accounts_iter)?;
    **account.try_borrow_mut_lamports()? = account.lamports()
        .checked_add(amount)
        .ok_or(ProgramError::InvalidArgument)?;
    Ok(())
}
""",
#unsafe
"""use solana_program::{
    account_info::{AccountInfo, next_account_info},
    entrypoint::ProgramResult,
};

pub fn safe_write_data(accounts: &[AccountInfo], data: &[u8]) -> ProgramResult {
    let accounts_iter = &mut accounts.iter();
    let account = next_account_info(accounts_iter)?;
    account.try_borrow_mut_data()?[..data.len()].copy_from_slice(data);
    // No validation of data length vs account data size
    Ok(())
}
""",
"""use solana_program::{
    account_info::{AccountInfo, next_account_info},
    entrypoint::ProgramResult,
    program_error::ProgramError,
};

pub fn safe_write_data(accounts: &[AccountInfo], data: &[u8]) -> ProgramResult {
    let accounts_iter = &mut accounts.iter();
    let account = next_account_info(accounts_iter)?;
    if data.len() > account.data_len() {
        return Err(ProgramError::AccountDataTooSmall);
    }
    account.try_borrow_mut_data()?[..data.len()].copy_from_slice(data);
    Ok(())
}
""",
#unsafe
"""use solana_program::{program::invoke, account_info::AccountInfo, instruction::Instruction};

pub fn safe_invoke(instruction: &Instruction, accounts: &[AccountInfo]) {
    let _ = invoke(instruction, accounts);
}
""",
"""use solana_program::{program::invoke, account_info::AccountInfo, instruction::Instruction, entrypoint::ProgramResult};

pub fn safe_invoke(instruction: &Instruction, accounts: &[AccountInfo]) -> ProgramResult {
    invoke(instruction, accounts)?;
    Ok(())
}
""",
#unsafe
"""use solana_program::{account_info::AccountInfo, pubkey::Pubkey, program_error::ProgramError};

pub fn safe_account_verification(account: &AccountInfo, expected_owner: &Pubkey) -> bool {
    account.owner == expected_owner
}
""",
"""use solana_program::{account_info::AccountInfo, pubkey::Pubkey, entrypoint::ProgramResult, program_error::ProgramError};

pub fn safe_account_verification(account: &AccountInfo, expected_owner: &Pubkey) -> ProgramResult {
    if account.owner != expected_owner {
        return Err(ProgramError::IllegalOwner);
    }
    Ok(())
}
""",
#unsafe
"""use solana_program::{account_info::AccountInfo, program_error::ProgramError, program_pack::Pack};
use spl_token::state::Account;

pub fn safe_deserialize(account: &AccountInfo) -> Account {
    Account::unpack_unchecked(&account.data.borrow()).unwrap()
}
""",
"""use solana_program::{account_info::AccountInfo, program_error::ProgramError, program_pack::Pack, entrypoint::ProgramResult};
use spl_token::state::Account;

pub fn safe_deserialize(account: &AccountInfo) -> ProgramResult<Account> {
    Account::unpack(&account.data.borrow()).map_err(|_| ProgramError::InvalidAccountData)
}
""",
#unsafe
"""use solana_program::{account_info::AccountInfo, entrypoint::ProgramResult, pubkey::Pubkey, system_instruction, program::invoke};

pub fn unsafe_token_transfer(from: &AccountInfo, to: &AccountInfo, amount: u64) {
    let ix = system_instruction::transfer(from.key, to.key, amount);
    let _ = invoke(&ix, &[from.clone(), to.clone()]);
}
""",
"""use solana_program::{account_info::AccountInfo, entrypoint::ProgramResult, pubkey::Pubkey, system_instruction, program::invoke};

pub fn safe_token_transfer(from: &AccountInfo, to: &AccountInfo, amount: u64) -> ProgramResult {
    let ix = system_instruction::transfer(from.key, to.key, amount);
    invoke(&ix, &[from.clone(), to.clone()])?;
    Ok(())
}
""",
#unsafe
"""use solana_program::{account_info::AccountInfo, entrypoint::ProgramResult};

pub fn safe_signature_check(account: &AccountInfo) {
    let _is_signer = account.is_signer;
}
""",
"""use solana_program::{account_info::AccountInfo, entrypoint::ProgramResult, program_error::ProgramError};

pub fn safe_signature_check(account: &AccountInfo) -> ProgramResult {
    if !account.is_signer {
        return Err(ProgramError::MissingRequiredSignature);
    }
    Ok(())
}
""",
#unsafe
"""use solana_program::{entrypoint::ProgramResult, program_error::ProgramError};

pub fn safe_error_propagation(result: ProgramResult) {
    match result {
        Ok(_) => {},
        Err(_) => {} // Error is ignored, not propagated
    }
}
""",
"""use solana_program::entrypoint::ProgramResult;

pub fn safe_error_propagation(result: ProgramResult) -> ProgramResult {
    match result {
        Ok(_) => Ok(()),
        Err(e) => Err(e), // Properly propagate the error
    }
}
""",
#unsafe
"""use solana_program::{account_info::AccountInfo, program_error::ProgramError, entrypoint::ProgramResult};

pub fn safe_state_update(accounts: &[AccountInfo]) -> ProgramResult {
    let account = &accounts[0];
    account.try_borrow_mut_data()?[0] = 1; // Arbitrary state change
    Ok(())
}
""",
"""use solana_program::{account_info::AccountInfo, program_error::ProgramError, entrypoint::ProgramResult};

pub fn safe_state_update(accounts: &[AccountInfo], validator: &Pubkey) -> ProgramResult {
    let account = &accounts[0];
    if account.owner != validator {
        return Err(ProgramError::IllegalOwner);
    }
    account.try_borrow_mut_data()?[0] = 1; // State change after validation
    Ok(())
}
""",
#unsafe
"""use solana_program::{account_info::AccountInfo, entrypoint::ProgramResult};

pub fn safe_writability_check(account: &AccountInfo) {
    let _ = account.try_borrow_mut_data(); // Attempt to borrow data without checking writability
}
""",
"""use solana_program::{account_info::AccountInfo, entrypoint::ProgramResult, program_error::ProgramError};

pub fn safe_writability_check(account: &AccountInfo) -> ProgramResult {
    if !account.is_writable {
        return Err(ProgramError::ReadOnly);
    }
    let _ = account.try_borrow_mut_data(); // Proceed after check
    Ok(())
}
""",
#unsafe
"""use solana_program::{account_info::AccountInfo, entrypoint::ProgramResult};

pub fn safe_account_size_check(account: &AccountInfo) {
    let _data = account.try_borrow_data().unwrap(); // Direct access without size check
}
""",
"""use solana_program::{account_info::AccountInfo, entrypoint::ProgramResult, program_error::ProgramError};

pub fn safe_account_size_check(account: &AccountInfo) -> ProgramResult {
    let data = account.try_borrow_data()?;
    if data.len() < expected_size {
        return Err(ProgramError::AccountDataTooSmall);
    }
    Ok(())
}
""",
#unsafe
"""use solana_program::{account_info::AccountInfo, sysvar::rent::Rent, entrypoint::ProgramResult};

pub fn safe_account_liveness_check(account: &AccountInfo) {
    let _lamports = account.lamports();
}
""",
"""use solana_program::{account_info::AccountInfo, sysvar::rent::Rent, entrypoint::ProgramResult, program_error::ProgramError};

pub fn safe_account_liveness_check(account: &AccountInfo) -> ProgramResult {
    let rent = Rent::get()?;
    if !rent.is_exempt(account.lamports(), account.data_len()) {
        return Err(ProgramError::AccountNotRentExempt);
    }
    Ok(())
}
""",
"""use solana_program::{
    account_info::{AccountInfo, next_account_info},
    pubkey::Pubkey,
    entrypoint::ProgramResult,
    program_error::ProgramError,
    sysvar::{rent::Rent, Sysvar},
};
use spl_token::instruction::transfer;

pub fn safe_spl_token_transfer(accounts: &[AccountInfo], amount: u64, program_id: &Pubkey) {
    let accounts_iter = &mut accounts.iter();
    let source_account = next_account_info(accounts_iter).unwrap();
    let destination_account = next_account_info(accounts_iter).unwrap();
    let authority_account = next_account_info(accounts_iter).unwrap();

    let transfer_ix = transfer(
        program_id,
        source_account.key,
        destination_account.key,
        authority_account.key,
        &[&authority_account.key],
        amount,
    ).unwrap(); // Unsafe: Ignoring potential error

    let _ = solana_program::program::invoke(
        &transfer_ix,
        accounts,
    );
}
""",
"""use solana_program::{
    account_info::{AccountInfo, next_account_info},
    pubkey::Pubkey,
    entrypoint::ProgramResult,
    sysvar::{rent::Rent, Sysvar},
};
use spl_token::instruction::transfer;

pub fn safe_spl_token_transfer(accounts: &[AccountInfo], amount: u64, program_id: &Pubkey) -> ProgramResult {
    let accounts_iter = &mut accounts.iter();
    let source_account = next_account_info(accounts_iter)?;
    let destination_account = next_account_info(accounts_iter)?;
    let authority_account = next_account_info(accounts_iter)?;

    let transfer_ix = transfer(
        program_id,
        source_account.key,
        destination_account.key,
        authority_account.key,
        &[&authority_account.key],
        amount,
    )?;

    solana_program::program::invoke(
        &transfer_ix,
        accounts,
    )?;

    Ok(())
}
""",
#unsafe
"""use solana_program::account_info::AccountInfo;

pub fn safe_check_signer(account: &AccountInfo) {
    let _ = account.is_signer; // This is just accessed, not actually checked
}
""",
"""use solana_program::{
    account_info::AccountInfo,
    entrypoint::ProgramResult,
    program_error::ProgramError,
};

pub fn safe_check_signer(account: &AccountInfo) -> ProgramResult {
    if !account.is_signer {
        return Err(ProgramError::MissingRequiredSignature);
    }

    Ok(())
}
""",
#unsafe
"""use solana_program::entrypoint::ProgramResult;

pub fn safe_instruction_data_check(data: &[u8]) {
    let _instruction = data[0]; // Potential panic if data is empty
}
""",
"""use solana_program::{
    entrypoint::ProgramResult,
    program_error::ProgramError,
};

pub fn safe_instruction_data_check(data: &[u8]) -> ProgramResult {
    if data.is_empty() {
        return Err(ProgramError::InvalidInstructionData);
    }

    let _instruction = data[0];

    Ok(())
}
""",
#unsafe
"""use solana_program::account_info::AccountInfo;

pub fn safe_use_account_data(account: &AccountInfo) {
    let _data = account.data.borrow();
    let _value = _data[0]; // Potential panic if data is empty
}
""",
"""use solana_program::{
    account_info::AccountInfo,
    entrypoint::ProgramResult,
    program_error::ProgramError,
};

pub fn safe_use_account_data(account: &AccountInfo) -> ProgramResult {
    let data = account.data.borrow();
    if data.len() < 1 {
        return Err(ProgramError::InvalidAccountData);
    }

    let _value = data[0];

    Ok(())
}
""",
#unsafe
"""use solana_program::{
    program::invoke,
    instruction::Instruction,
    account_info::AccountInfo,
};

pub fn safe_cpi_invoke(instruction: &Instruction, accounts: &[AccountInfo]) {
    let _ = invoke(instruction, accounts);
}
""",
#safe
"""use solana_program::{
    program::invoke,
    instruction::Instruction,
    account_info::AccountInfo,
    entrypoint::ProgramResult,
};

pub fn safe_cpi_invoke(instruction: &Instruction, accounts: &[AccountInfo]) -> ProgramResult {
    invoke(instruction, accounts)?;

    Ok(())
}
""",
#unsafe
"""use solana_program::{account_info::AccountInfo, pubkey::Pubkey, entrypoint::ProgramResult};

pub fn safe_authority_check(user_account: &AccountInfo, authority: &Pubkey) -> bool {
    user_account.owner == authority
}
""",
#safe
"""use solana_program::{account_info::AccountInfo, pubkey::Pubkey, entrypoint::ProgramResult, program_error::ProgramError};

pub fn safe_authority_check(user_account: &AccountInfo, authority: &Pubkey) -> ProgramResult {
    if user_account.owner != authority {
        return Err(ProgramError::IllegalOwner);
    }
    Ok(())
}
""",
#// Unsafe: Proceeds without validating the input length
"""use solana_program::{entrypoint::ProgramResult, program_error::ProgramError};

pub fn safe_input_length_check(input: &[u8]) {
    
    let _ = input[0]; // Assumes input is non-empty without check
}
""",
#// Safe: Validates input length before proceeding
"""use solana_program::{entrypoint::ProgramResult, program_error::ProgramError};

pub fn safe_input_length_check(input: &[u8]) -> ProgramResult {
    
    if input.is_empty() {
        return Err(ProgramError::InvalidInstructionData);
    }
    let _ = input[0]; // Safe to access after check
    Ok(())
}
""",
# Unsafe: Directly modifies account data without validation
"""use solana_program::{account_info::AccountInfo, entrypoint::ProgramResult, program_error::ProgramError};

pub fn safe_account_data_usage(account: &AccountInfo) {
    account.data.borrow_mut()[0] = 42; // Arbitrary data modification
}
""",
"""use solana_program::{account_info::AccountInfo, entrypoint::ProgramResult, program_error::ProgramError};

pub fn safe_account_data_usage(account: &AccountInfo) -> ProgramResult {
    // Safe: Checks account's writability before modifying data
    if !account.is_writable {
        return Err(ProgramError::ReadOnly);
    }
    account.data.borrow_mut()[0] = 42; // Safe modification after check
    Ok(())
}
""",
#// Unsafe: Directly decreases lamports without any checks
"""use solana_program::{account_info::AccountInfo, entrypoint::ProgramResult};

pub fn safe_lamport_handling(account: &AccountInfo) {
    
    **account.lamports.borrow_mut() -= 100; // Arbitrary lamport deduction
}
""",
#// Safe: Verifies account has sufficient lamports before deduction
"""use solana_program::{account_info::AccountInfo, entrypoint::ProgramResult, program_error::ProgramError};

pub fn safe_lamport_handling(account: &AccountInfo) -> ProgramResult {
    
    let lamports = **account.lamports.borrow();
    if lamports < 100 {
        return Err(ProgramError::InsufficientFunds);
    }
    **account.lamports.borrow_mut() -= 100;
    Ok(())
}
""",
#// Unsafe: Ignores the outcome of a cross-program invocation
"""use solana_program::{program::invoke, instruction::Instruction, account_info::AccountInfo, entrypoint::ProgramResult};

pub fn safe_cpi_handling(instruction: &Instruction, accounts: &[AccountInfo]) {
    
    let _ = invoke(instruction, accounts);
}
""",
# Safe: Checks the outcome of a cross-program invocation
"""use solana_program::{program::invoke, instruction::Instruction, account_info::AccountInfo, entrypoint::ProgramResult, program_error::ProgramError};

pub fn safe_cpi_handling(instruction: &Instruction, accounts: &[AccountInfo]) -> ProgramResult {
    invoke(instruction, accounts)?;
    Ok(())
}
""",
# Unsafe: Executes a token transfer without checking the result
"""use solana_program::{program::invoke, instruction::Instruction, account_info::AccountInfo};

pub fn safe_token_transfer_cpi(instruction: &Instruction, accounts: &[AccountInfo]) {
    let _ = invoke(instruction, accounts);
}
""",

#Safe: Checks the result of the token transfer
"""use solana_program::{program::invoke, instruction::Instruction, account_info::AccountInfo, entrypoint::ProgramResult};

pub fn safe_token_transfer_cpi(instruction: &Instruction, accounts: &[AccountInfo]) -> ProgramResult {
    invoke(instruction, accounts)?;
    Ok(())
}
""",
    
# Unsafe: Deserializes account without handling potential errors
"""use solana_program::{program_pack::Pack, account_info::AccountInfo};
use spl_token::state::Account;

pub fn safe_deserialize_account(account: &AccountInfo) {
    let _ = Account::unpack_unchecked(&account.data.borrow());
}
""",

#Safe: Properly handles deserialization errors
"""use solana_program::{program_pack::Pack, account_info::AccountInfo, entrypoint::ProgramResult};
use spl_token::state::Account;

pub fn safe_deserialize_account(account: &AccountInfo) -> ProgramResult {
    Account::unpack(&account.data.borrow())?;
    Ok(())
}
""",

#Unsafe: Accesses account data without validating length
"""use solana_program::account_info::AccountInfo;

pub fn safe_account_data_access(account: &AccountInfo) {
    let _ = account.data.borrow()[0];
}
""",
#Safe: Validates account data length before access
"""use solana_program::{account_info::AccountInfo, entrypoint::ProgramResult, program_error::ProgramError};

pub fn safe_account_data_access(account: &AccountInfo) -> ProgramResult {
    let data = account.data.borrow();
    if data.len() < 1 {
        return Err(ProgramError::InvalidAccountData);
    }
    let _ = data[0];
    Ok(())
}
""",
#Unsafe: Assumes account is rent-exempt without verification
"""use solana_program::{account_info::AccountInfo, sysvar::rent::Rent};

pub fn safe_rent_exemption_check(account: &AccountInfo) {
    let _lamports = account.lamports();
}
""",
#Safe: Verifies account is rent-exempt
"""use solana_program::{account_info::AccountInfo, entrypoint::ProgramResult, program_error::ProgramError, sysvar::rent::Rent};

pub fn safe_rent_exemption_check(account: &AccountInfo) -> ProgramResult {
    let rent = Rent::get()?;
    if !rent.is_exempt(account.lamports(), account.data_len()) {
        return Err(ProgramError::AccountNotRentExempt);
    }
    Ok(())
}
""",
#Unsafe: Performs an action without verifying the signature
"""use solana_program::account_info::AccountInfo;

pub fn safe_signature_verification(account: &AccountInfo) {
    let _is_signer = account.is_signer;
}
""",
#Safe: Ensures the account provided a signature
"""use solana_program::{account_info::AccountInfo, entrypoint::ProgramResult, program_error::ProgramError};

pub fn safe_signature_verification(account: &AccountInfo) -> ProgramResult {
    if !account.is_signer {
        return Err(ProgramError::MissingRequiredSignature);
    }
    Ok(())
}
"""
]
labels = [0, 3, 1, 0, 3, 3, 1, 0, 3, 3, 2, 2, 3, 3, 1, 2, 0, 2, 0, 0, 1, 0, 1, 1, 1, 0, 1, 3, 0, 3, 1, 1, 1, 3, 2, 2, 3, 1, 3, 2, 3, 0, 0, 3, 3, 0, 0, 3, 0, 3, 0, 0, 0, 3, 1, 0, 2, 1]


test_snippets = [
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
test_labels = [1,0,2,0,3,2,1,0,1,3]
