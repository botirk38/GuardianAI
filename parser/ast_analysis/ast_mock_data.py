mock_ast_vulnerabilities = {
    "reentrancy": {
        "type": "function_call",
        "name": "invoke",
        "args": ["another_program_id", "accounts", "instruction_data"],
        "comments": "Potential for reentrancy if external program modifies state."
    },
    "logic_error": {
        "type": "conditional",
        "condition": "account_balance < expected_balance",
        "true_branch": "proceed_with_transaction",
        "false_branch": "refund_transaction",
        "comments": "Logic error leading to funds being stuck if conditions not met."
    },
    "signature_verification": {
        "type": "function_call",
        "name": "verify_signatures",
        "args": ["transaction_signatures"],
        "result_handling": "if result.is_err() { panic!(); }",
        "comments": "Missing or incorrect signature verification can lead to unauthorized actions."
    },
    "arithmetic_overflow": {
        "type": "arithmetic_operation",
        "operation": "addition",
        "operands": ["user_balance", "deposit_amount"],
        "comments": "Lack of overflow checks can lead to incorrect balance calculations."
    }
}

mock_submission_ast = {
    "type": "function_definition",
    "name": "process_transaction",
    "body": [
        {
            "type": "variable_declaration",
            "name": "user_balance",
            "dataType": "u64",
            "value": "get_balance(user_id)"
        },
        {
            "type": "conditional_statement",
            "condition": {
                "type": "binary_operation",
                "operation": "less_than",
                "left": {"type": "variable", "name": "user_balance"},
                "right": {"type": "literal", "value": "minimum_balance", "dataType": "u64"}
            },
            "then": [
                {
                    "type": "function_call",
                    "name": "refund_user",
                    "args": ["user_id"]
                }
            ],
            "else": [
                {
                    "type": "arithmetic_operation",
                    "operation": "addition",
                    "operands": [
                        {"type": "variable", "name": "user_balance"},
                        {"type": "literal", "value": "deposit_amount", "dataType": "u64"}
                    ],
                    "comments": "Potential arithmetic overflow if not properly checked."
                },
                {
                    "type": "function_call",
                    "name": "update_balance",
                    "args": ["user_id", "new_balance"]
                }
            ]
        }
    ],
    "comments": "Example Rust function that could contain vulnerabilities."
}

mock_submission_ast1 = {
    "type": "Function",
    "name": "process_payment",
    "body": [  # Using 'body' to contain the function's statements and expressions
        {
            "type": "VariableDeclaration",
            "name": "user_balance",
            "dataType": "Result<u64, Error>",
            "initializer": {
                "type": "FunctionCall",
                "name": "query_balance",
                "arguments": ["user_id"]
            }
        },
        {
            "type": "ExpressionStatement",
            "expression": {
                "type": "MethodCall",
                "receiver": "user_balance",
                "method": "unwrap",
                "arguments": [],
                "line": 5
            }
        }
    ]
}
mock_submission_ast2 = {
    "type": "Program",
    "children": [
        {
            "type": "Item",
            "children": [
                {
                    "type": "Attribute",
                    "name": "derive(Debug)",
                    "children": []
                },
                {
                    "type": "Struct",
                    "name": "Rectangle",
                    "children": [
                        {
                            "type": "Field",
                            "name": "width",
                            "dataType": "u32",
                            "children": []
                        },
                        {
                            "type": "Field",
                            "name": "height",
                            "dataType": "u32",
                            "children": []
                        }
                    ]
                }
            ]
        },
        {
            "type": "Item",
            "children": [
                {
                    "type": "Impl",
                    "target": "Rectangle",
                    "children": [
                        {
                            "type": "Method",
                            "name": "area",
                            "returnType": "u32",
                            "children": [
                                {
                                    "type": "Block",
                                    "children": [
                                        {
                                            "type": "ExpressionStatement",
                                            "children": [
                                                {
                                                    "type": "BinaryOperation",
                                                    "operator": "*",
                                                    "left": {
                                                        "type": "FieldAccess",
                                                        "field": "width",
                                                        "children": []
                                                    },
                                                    "right": {
                                                        "type": "FieldAccess",
                                                        "field": "height",
                                                        "children": []
                                                    }
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "type": "Method",
                            "name": "can_hold",
                            "returnType": "bool",
                            "children": [
                                {
                                    "type": "Block",
                                    "children": [
                                        {
                                            "type": "ExpressionStatement",
                                            "children": [
                                                {
                                                    "type": "MethodCall",
                                                    "method": "unwrap",
                                                    "children": [
                                                        {
                                                            "type": "CallArgument",
                                                            "children": [
                                                                {
                                                                    "type": "LocalVariable",
                                                                    "name": "other_area",
                                                                    "children": []
                                                                }
                                                            ]
                                                        }
                                                    ]
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    ]
}



# A simple vulnerability pattern (looking for direct unwrap calls)
vulnerability_pattern = {
    "type": "unwrap"
}
