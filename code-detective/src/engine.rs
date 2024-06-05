pub mod ast;
use ast::{StaticInfo, StructInfo, EnumInfo};
use serde::{Deserialize, Serialize};

#[derive(Debug, Default, Serialize, Deserialize)]
pub struct CodeFeatures {
    pub possible_overflow_statements: Vec<String>,
    pub possible_underflow_statements: Vec<String>,
    pub possible_reentrancy_statements: Vec<String>,
    pub possible_authority_vulnerabilities: Vec<String>,
    pub possible_signature_vulnerabilities: Vec<String>,
    pub possible_frozen_account_vulnerabilities: Vec<String>,
    pub structs: Vec<StructInfo>,
    pub static_variables: Vec<StaticInfo>,
    pub enums: Vec<EnumInfo>,
}

pub fn analyze_code(code: &str) -> CodeFeatures {
    let ast = match ast::parse_code_ast(code) {
        Ok(ast) => ast,
        Err(e) => {
            eprintln!("Error parsing code: {}", e);
            return CodeFeatures::default();
        }
    };

    let mut features = CodeFeatures::default();

    for item in ast {
        match item {
            ast::AstItem::Function(func_info) => {
                parse_function(&func_info, &mut features);
            }

            ast::AstItem::Impl(impl_info) => {
                println!("Impl: {:?}", impl_info);

                for func in impl_info.methods {
                    parse_function(&func, &mut features);
                }
            }

            ast::AstItem::Enum(enum_info) => {
                features.enums.push(enum_info);
            }

            ast::AstItem::Struct(struct_info) => {
                features.structs.push(struct_info);
            }

            ast::AstItem::Static(static_info) => {
                features.static_variables.push(static_info);
            }
            _ => {}
        }
    }

    println!("Features: {:?}", features);

    features
}

fn parse_function(func_info: &ast::FunctionInfo, features: &mut CodeFeatures) {
    for stmt in &func_info.expressions {
        println!("Analyzing statement: {}", stmt);

        if is_potential_reentrancy(stmt) {
            println!("Possible reentrancy detected for statement: {}", stmt);
            features.possible_reentrancy_statements.push(stmt.clone());
        }

        if is_potential_authority_check(stmt) {
            println!(
                "Possible authority vulnerability detected for statement: {}",
                stmt
            );
            features
                .possible_authority_vulnerabilities
                .push(stmt.clone());
        }

        if is_potential_signature_verification(stmt) {
            println!(
                "Possible signature vulnerability detected for statement: {}",
                stmt
            );
            features
                .possible_signature_vulnerabilities
                .push(stmt.clone());
        }

        if is_potential_frozen_account_modification(stmt) {
            println!(
                "Possible frozen account modification vulnerability detected for statement: {}",
                stmt
            );
            features
                .possible_frozen_account_vulnerabilities
                .push(stmt.clone());
        }

        if is_potential_overflow(stmt) || is_conditional(stmt) {
            println!("Possible overflow detected for statement: {}", stmt);
            features.possible_overflow_statements.push(stmt.clone());
        }
        if is_potential_underflow(stmt) || is_conditional(stmt) {
            println!("Possible underflow detected for statement: {}", stmt);
            features.possible_underflow_statements.push(stmt.clone());
        }
    }
}

fn is_potential_overflow(stmt: &str) -> bool {
    stmt.contains('+') || stmt.contains('*')
}

fn is_potential_underflow(stmt: &str) -> bool {
    stmt.contains('-') || stmt.contains('/')
}

fn is_conditional(stmt: &str) -> bool {
    stmt.contains("if") || stmt.contains("else") || stmt.contains("match")
}

fn is_potential_reentrancy(stmt: &str) -> bool {
    let external_call_patterns = ["invoke", "invoke_signed", "call_with_value"];

    let external_call_detected = external_call_patterns
        .iter()
        .any(|&pattern| stmt.contains(pattern));

    external_call_detected
}

fn is_potential_authority_check(stmt: &str) -> bool {
    let sensitive_operations = [
        "transfer",
        "send",
        "invoke",
        "invoke_signed",
        "set_authority",
        "delegate",
    ];
    let permission_checks = ["require!", "assert!"];

    let mut sensitive_operation_detected = false;
    let mut authority_check_present = false;

    for operation in sensitive_operations.iter() {
        if stmt.contains(operation) {
            sensitive_operation_detected = true;
        }
    }

    for check in permission_checks.iter() {
        if stmt.contains(check) {
            authority_check_present = true;
        }
    }

    sensitive_operation_detected && !authority_check_present
}

fn is_potential_signature_verification(stmt: &str) -> bool {
    let sensitive_operations = [
        "transfer",
        "send",
        "invoke",
        "invoke_signed",
        "execute",
        "withdraw",
    ];
    let signature_checks = [
        "verify_signature",
        "check_sig",
        "is_valid_signature",
        "signer_key",
    ];

    let mut sensitive_operation_detected = false;
    let mut signature_check_present = false;

    for operation in sensitive_operations.iter() {
        if stmt.contains(operation) {
            sensitive_operation_detected = true;
        }
    }

    for check in signature_checks.iter() {
        if stmt.contains(check) {
            signature_check_present = true;
        }
    }

    sensitive_operation_detected && !signature_check_present
}

fn is_potential_frozen_account_modification(stmt: &str) -> bool {
    let sensitive_operations = [
        "transfer",
        "withdraw",
        "update_balance",
        "modify",
        "change",
        "+=",
        "-=",
    ];
    let frozen_account_checks = ["is_frozen", "require_not_frozen", "assert_not_frozen"];

    let mut sensitive_operation_detected = false;
    let mut frozen_account_check_present = false;

    for operation in sensitive_operations.iter() {
        if stmt.contains(operation) {
            sensitive_operation_detected = true;
        }
    }

    for check in frozen_account_checks.iter() {
        if stmt.contains(check) {
            frozen_account_check_present = true;
        }
    }

    sensitive_operation_detected && !frozen_account_check_present
}
