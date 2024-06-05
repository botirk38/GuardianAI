use crate::engine::analyze_code;

#[test]
fn test_overflow_detection() {
    let code = r#"
        pub fn add(a: u32, b: u32) -> u32 {
            a + b
        }

        pub fn multiply(a: u32, b: u32) -> u32 {
            a * b
        }
    "#;

    let features = analyze_code(code);
    assert!(features
        .possible_overflow_statements
        .contains(&"a + b".to_string()));
    assert!(features
        .possible_overflow_statements
        .contains(&"a * b".to_string()));
}

#[test]
fn test_underflow_detection() {
    let code = r#"
        pub fn subtract(a: u32, b: u32) -> u32 {
            a - b
        }

        pub fn divide(a: u32, b: u32) -> u32 {
            a / b
        }
    "#;

    let features = analyze_code(code);
    assert!(features
        .possible_underflow_statements
        .contains(&"a - b".to_string()));
    assert!(features
        .possible_underflow_statements
        .contains(&"a / b".to_string()));
}

#[test]
fn test_authority_check_detection() {
    let code = r#"
        pub fn transfer(to: Address, amount: u32) {
            self.balance -= amount;
            to.send(amount);
        }

        pub fn modify_balance(account: Address, amount: u32) {
            self.balance[account] += amount;
        }
    "#;

    let features = analyze_code(code);
    assert!(features
        .possible_authority_vulnerabilities
        .contains(&"to . send (amount) ;".to_string()));
}

#[test]
fn test_signature_verification_detection() {
    let code = r#"
        pub fn execute(transaction: Transaction) {
            self.execute_transaction(transaction);
        }

        pub fn withdraw(amount: u32, signature: &Signature) {
            if self.verify_signature(signature) {
                self.balance -= amount;
                self.msg.sender.send(amount);
            }
        }
    "#;

    let features = analyze_code(code);
    assert!(features
        .possible_signature_vulnerabilities
        .contains(&"self . execute_transaction (transaction) ;".to_string()));
    assert!(!features.possible_signature_vulnerabilities.contains(&"if self.verify_signature(signature) { self.balance -= amount; self.msg.sender.send(amount); }".to_string()));
}

#[test]
fn test_frozen_account_modification_detection() {
    let code = r#"
        struct Test {
            balance: std::collections::HashMap<String, i32>,
            msg: Msg,
        }

        struct Msg {
            sender: String,
        }

        impl Test {
            fn is_frozen(&self, account: &str) -> bool {
                // Dummy implementation for test
                false
            }

            fn update_balance(&mut self, account: &str, amount: i32, to: &str) {
                if self.is_frozen(account) {
                    panic!("Account is frozen");
                }
                self.balance.entry(account.to_string()).and_modify(|e| *e += amount).or_insert(amount);
                self.balance.entry(to.to_string()).and_modify(|e| *e += amount).or_insert(amount);
                self.balance.entry(self.msg.sender.clone()).and_modify(|e| *e -= amount).or_insert(-amount);
            }
        }
    "#;

    let features = analyze_code(code);

    assert!(features.possible_frozen_account_vulnerabilities.contains(&"self . balance . entry (account . to_string ()) . and_modify (| e | * e += amount) . or_insert (amount) ;".to_string()));
}

#[test]
fn test_struct_detection() {
    let code = r#"
        pub struct TestStruct {
            value: u32,
        }

        pub struct AnotherStruct {
            count: u64,
        }
    "#;

    let features = analyze_code(code);
    assert_eq!(features.structs.len(), 2);
    assert!(features.structs.iter().any(|s| s.name == "TestStruct"));
    assert!(features.structs.iter().any(|s| s.name == "AnotherStruct"));
}

#[test]
fn test_static_detection() {
    let code = r#"
        static mut COUNTER: u32 = 0;
        static MAX_LIMIT: u64 = 100;
    "#;

    let features = analyze_code(code);
    assert_eq!(features.static_variables.len(), 2);
    assert!(features
        .static_variables
        .iter()
        .any(|s| s.name == "COUNTER"));
    assert!(features
        .static_variables
        .iter()
        .any(|s| s.name == "MAX_LIMIT"));
}

#[test]
fn test_nested_function_calls() {
    let code = r#"
        pub fn transfer(to: Address, amount: u32) {
            self.update_balance(to, amount);
            self.log_transfer(to, amount);
        }

        pub fn update_balance(to: Address, amount: u32) {
            self.balance[to] += amount;
        }

        pub fn log_transfer(to: Address, amount: u32) {
            // log the transfer
        }
    "#;

    let features = analyze_code(code);
    assert!(features
        .possible_frozen_account_vulnerabilities
        .contains(&"self . update_balance (to , amount) ;".to_string()));
    assert!(features
        .possible_frozen_account_vulnerabilities
        .contains(&"self . log_transfer (to , amount) ;".to_string()));
}

#[test]
fn test_mixed_arithmetic_operations() {
    let code = r#"
        pub fn calculate(a: u32, b: u32) -> u32 {
            let mut result = a + b;
            result *= 2;
            result -= 3;
            result /= 4;
            result
        }
    "#;

    let features = analyze_code(code);
    assert!(features
        .possible_overflow_statements
        .contains(&"let mut result = a + b ;".to_string()));

    assert!(features
        .possible_overflow_statements
        .contains(&"result *= 2 ;".to_string()));
    assert!(features
        .possible_underflow_statements
        .contains(&"result -= 3 ;".to_string()));
    assert!(features
        .possible_underflow_statements
        .contains(&"result /= 4 ;".to_string()));
}

#[test]
fn test_deeply_nested_conditionals() {
    let code = r#"
        pub fn complex_logic(a: u32, b: u32) -> u32 {
            if a > b {
                if b > 10 {
                    if a + b > 100 {
                        return a - b;
                    } else {
                        return a + b;
                    }
                } else {
                    return a * b;
                }
            } else {
                return a / b;
            }
        }
    "#;

    let features = analyze_code(code);

    assert!(features.possible_overflow_statements.contains(&"if a > b { if b > 10 { if a + b > 100 { return a - b ; } else { return a + b ; } } else { return a * b ; } } else { return a / b ; }".to_string()));
}

#[test]
fn test_multiple_vulnerabilities_in_single_function() {
    let code = r#"
        struct Msg {
            sender: String,
        }

        struct Test {
            balance: std::collections::HashMap<String, u32>,
            msg: Msg,
        }

        impl Test {
            pub fn complex_function(&mut self, a: u32, b: u32) -> u32 {
                if self.is_frozen(&self.msg.sender) {
                    panic!("Account is frozen");
                }
                self.balance.entry(self.msg.sender.clone()).and_modify(|e| *e -= a).or_insert(0);
                if !self.call_with_value(&self.msg.sender, b) {
                    panic!("Call failed");
                }
                if a > b {
                    return a + b;
                } else {
                    return a - b;
                }
            }

            fn is_frozen(&self, account: &str) -> bool {
                // Dummy implementation for test
                false
            }

            fn call_with_value(&self, _to: &str, _value: u32) -> bool {
                // Dummy implementation for test
                true
            }
        }
    "#;

    let features = analyze_code(code);
    assert!(features.possible_reentrancy_statements.contains(
        &"if ! self . call_with_value (& self . msg . sender , b) { panic ! (\"Call failed\") ; }"
            .to_string()
    ));
    assert!(features.possible_frozen_account_vulnerabilities.contains(&"self . balance . entry (self . msg . sender . clone ()) . and_modify (| e | * e -= a) . or_insert (0) ;".to_string()));
    assert!(features
        .possible_overflow_statements
        .contains(&"if a > b { return a + b ; } else { return a - b ; }".to_string()));
    assert!(features
        .possible_underflow_statements
        .contains(&"if a > b { return a + b ; } else { return a - b ; }".to_string()));
}
