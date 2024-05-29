use analyzer::analyzer_client::AnalyzerClient;
use analyzer::AnalyzeRequest;

pub mod analyzer {
    tonic::include_proto!("analyzer");
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let mut client = AnalyzerClient::connect("http://[::1]:50051").await?;

    let contract_code = r#"
    // Solana smart contract code with vulnerabilities
    use solana_program::{
        account_info::{next_account_info, AccountInfo},
        entrypoint,
        entrypoint::ProgramResult,
        msg,
        program_error::ProgramError,
        pubkey::Pubkey,
    };

    entrypoint!(process_instruction);

    fn process_instruction(
        program_id: &Pubkey,
        accounts: &[AccountInfo],
        instruction_data: &[u8],
    ) -> ProgramResult {
        let accounts_iter = &mut accounts.iter();

        let user_account = next_account_info(accounts_iter)?;
        let authority_account = next_account_info(accounts_iter)?;
        let frozen_account = next_account_info(accounts_iter)?;

        // Authority check vulnerability
        if user_account.is_signer == false {
            return Err(ProgramError::MissingRequiredSignature);
        }

        // Handling instruction data (e.g., modify balance)
        let mut data = user_account.try_borrow_mut_data()?;
        let amount = instruction_data[0] as u64;

        // Overflow/Underflow vulnerability
        let balance = data[0] as u64;
        let new_balance = balance + amount;
        data[0] = new_balance as u8;

        // Reentrancy attack vulnerability
        if new_balance > 100 {
            // Simulate an external call
            process_instruction(program_id, accounts, instruction_data)?;
        }

        // Signature verification vulnerability
        if instruction_data[1] != 0 {
            return Err(ProgramError::InvalidInstructionData);
        }

        // Frozen account modification vulnerability
        if frozen_account.data.borrow()[0] == 1 {
            return Err(ProgramError::AccountFrozen);
        }

        Ok(())
    }
    "#;

    let request = tonic::Request::new(AnalyzeRequest {
        code: contract_code.to_string(),
    });

    let response = client.analyze_contract(request).await?;

    println!("RESPONSE={:?}", response.into_inner().features_json);

    Ok(())
}

