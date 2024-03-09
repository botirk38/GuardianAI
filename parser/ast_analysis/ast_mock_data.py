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

rawdata = {"children":[{"children":[{"children":[{"name":"#"},{"name":"["},{"children":[{"children":[{"children":[{"children":[{"name":"derive"}],"name":"identifier"}],"name":"simplePathSegment"}],"name":"simplePath"},{"children":[{"children":[{"name":"("},{"children":[{"children":[{"children":[{"children":[{"name":"Debug"}],"name":"identifier"}],"name":"macroIdentifierLikeToken"}],"name":"tokenTreeToken"}],"name":"tokenTree"},{"name":")"}],"name":"delimTokenTree"}],"name":"attrInput"}],"name":"attr"},{"name":"]"}],"name":"outerAttribute"},{"children":[{"children":[{"name":"pub"}],"name":"visibility"},{"children":[{"children":[{"name":"struct"},{"children":[{"name":"Rectangle"}],"name":"identifier"},{"name":"{"},{"children":[{"children":[{"children":[{"name":"length"}],"name":"identifier"},{"name":":"},{"children":[{"children":[{"children":[{"children":[{"children":[{"children":[{"children":[{"children":[{"name":"u32"}],"name":"identifier"}],"name":"pathIdentSegment"}],"name":"typePathSegment"}],"name":"typePath"}],"name":"traitBound"}],"name":"traitObjectTypeOneBound"}],"name":"typeNoBounds"}],"name":"type_"}],"name":"structField"},{"name":","},{"children":[{"children":[{"name":"width"}],"name":"identifier"},{"name":":"},{"children":[{"children":[{"children":[{"children":[{"children":[{"children":[{"children":[{"children":[{"name":"u32"}],"name":"identifier"}],"name":"pathIdentSegment"}],"name":"typePathSegment"}],"name":"typePath"}],"name":"traitBound"}],"name":"traitObjectTypeOneBound"}],"name":"typeNoBounds"}],"name":"type_"}],"name":"structField"},{"name":","}],"name":"structFields"},{"name":"}"}],"name":"structStruct"}],"name":"struct_"}],"name":"visItem"}],"name":"item"},{"children":[{"children":[{"children":[{"children":[{"name":"impl"},{"children":[{"children":[{"children":[{"children":[{"children":[{"children":[{"children":[{"children":[{"name":"Rectangle"}],"name":"identifier"}],"name":"pathIdentSegment"}],"name":"typePathSegment"}],"name":"typePath"}],"name":"traitBound"}],"name":"traitObjectTypeOneBound"}],"name":"typeNoBounds"}],"name":"type_"},{"name":"{"},{"children":[{"children":[{"name":"pub"}],"name":"visibility"},{"children":[{"children":[],"name":"functionQualifiers"},{"name":"fn"},{"children":[{"name":"can_hold"}],"name":"identifier"},{"name":"("},{"children":[{"children":[{"children":[{"name":"&"},{"name":"self"}],"name":"shorthandSelf"}],"name":"selfParam"},{"name":","},{"children":[{"children":[{"children":[{"children":[{"children":[{"children":[{"children":[{"name":"other"}],"name":"identifier"}],"name":"identifierPattern"}],"name":"patternWithoutRange"}],"name":"patternNoTopAlt"}],"name":"pattern"},{"name":":"},{"children":[{"children":[{"children":[{"name":"&"},{"children":[{"children":[{"children":[{"children":[{"children":[{"children":[{"children":[{"name":"Rectangle"}],"name":"identifier"}],"name":"pathIdentSegment"}],"name":"typePathSegment"}],"name":"typePath"}],"name":"traitBound"}],"name":"traitObjectTypeOneBound"}],"name":"typeNoBounds"}],"name":"referenceType"}],"name":"typeNoBounds"}],"name":"type_"}],"name":"functionParamPattern"}],"name":"functionParam"}],"name":"functionParameters"},{"name":")"},{"children":[{"name":"->"},{"children":[{"children":[{"children":[{"children":[{"children":[{"children":[{"children":[{"children":[{"name":"bool"}],"name":"identifier"}],"name":"pathIdentSegment"}],"name":"typePathSegment"}],"name":"typePath"}],"name":"traitBound"}],"name":"traitObjectTypeOneBound"}],"name":"typeNoBounds"}],"name":"type_"}],"name":"functionReturnType"},{"children":[{"name":"{"},{"children":[{"children":[{"children":[{"children":[{"children":[{"children":[{"children":[{"children":[{"children":[{"name":"self"}],"name":"pathIdentSegment"}],"name":"pathExprSegment"}],"name":"pathInExpression"}],"name":"pathExpression"}],"name":"expression"},{"name":"."},{"children":[{"name":"length"}],"name":"identifier"}],"name":"expression"},{"children":[{"name":">"}],"name":"comparisonOperator"},{"children":[{"children":[{"children":[{"children":[{"children":[{"children":[{"children":[{"name":"other"}],"name":"identifier"}],"name":"pathIdentSegment"}],"name":"pathExprSegment"}],"name":"pathInExpression"}],"name":"pathExpression"}],"name":"expression"},{"name":"."},{"children":[{"name":"length"}],"name":"identifier"}],"name":"expression"}],"name":"expression"},{"name":"&&"},{"children":[{"children":[{"children":[{"children":[{"children":[{"children":[{"children":[{"name":"self"}],"name":"pathIdentSegment"}],"name":"pathExprSegment"}],"name":"pathInExpression"}],"name":"pathExpression"}],"name":"expression"},{"name":"."},{"children":[{"name":"width"}],"name":"identifier"}],"name":"expression"},{"children":[{"name":">"}],"name":"comparisonOperator"},{"children":[{"children":[{"children":[{"children":[{"children":[{"children":[{"children":[{"name":"other"}],"name":"identifier"}],"name":"pathIdentSegment"}],"name":"pathExprSegment"}],"name":"pathInExpression"}],"name":"pathExpression"}],"name":"expression"},{"name":"."},{"children":[{"name":"width"}],"name":"identifier"}],"name":"expression"}],"name":"expression"}],"name":"expression"}],"name":"statements"},{"name":"}"}],"name":"blockExpression"}],"name":"function_"}],"name":"associatedItem"},{"name":"}"}],"name":"inherentImpl"}],"name":"implementation"}],"name":"visItem"}],"name":"item"},{"children":[{"children":[{"name":"#"},{"name":"["},{"children":[{"children":[{"children":[{"children":[{"name":"cfg"}],"name":"identifier"}],"name":"simplePathSegment"}],"name":"simplePath"},{"children":[{"children":[{"name":"("},{"children":[{"children":[{"children":[{"children":[{"name":"test"}],"name":"identifier"}],"name":"macroIdentifierLikeToken"}],"name":"tokenTreeToken"}],"name":"tokenTree"},{"name":")"}],"name":"delimTokenTree"}],"name":"attrInput"}],"name":"attr"},{"name":"]"}],"name":"outerAttribute"},{"children":[{"children":[{"name":"mod"},{"children":[{"name":"tests"}],"name":"identifier"},{"name":"{"},{"children":[{"children":[{"children":[{"name":"use"},{"children":[{"children":[{"children":[{"name":"super"}],"name":"simplePathSegment"}],"name":"simplePath"},{"name":"::"},{"name":"*"}],"name":"useTree"},{"name":";"}],"name":"useDeclaration"}],"name":"visItem"}],"name":"item"},{"children":[{"children":[{"name":"#"},{"name":"["},{"children":[{"children":[{"children":[{"children":[{"name":"test"}],"name":"identifier"}],"name":"simplePathSegment"}],"name":"simplePath"}],"name":"attr"},{"name":"]"}],"name":"outerAttribute"},{"children":[{"children":[{"children":[],"name":"functionQualifiers"},{"name":"fn"},{"children":[{"name":"larger_can_hold_smaller"}],"name":"identifier"},{"name":"("},{"name":")"},{"children":[{"name":"{"},{"children":[{"children":[{"children":[{"name":"let"},{"children":[{"children":[{"children":[{"children":[{"name":"larger"}],"name":"identifier"}],"name":"identifierPattern"}],"name":"patternWithoutRange"}],"name":"patternNoTopAlt"},{"name":"="},{"children":[{"children":[{"children":[{"children":[{"children":[{"children":[{"children":[{"name":"Rectangle"}],"name":"identifier"}],"name":"pathIdentSegment"}],"name":"pathExprSegment"}],"name":"pathInExpression"},{"name":"{"},{"children":[{"children":[{"children":[{"name":"length"}],"name":"identifier"},{"name":":"},{"children":[{"children":[{"name":"8"}],"name":"literalExpression"}],"name":"expression"}],"name":"structExprField"},{"name":","},{"children":[{"children":[{"name":"width"}],"name":"identifier"},{"name":":"},{"children":[{"children":[{"name":"7"}],"name":"literalExpression"}],"name":"expression"}],"name":"structExprField"},{"name":","}],"name":"structExprFields"},{"name":"}"}],"name":"structExprStruct"}],"name":"structExpression"}],"name":"expression"},{"name":";"}],"name":"letStatement"}],"name":"statement"},{"children":[{"children":[{"name":"let"},{"children":[{"children":[{"children":[{"children":[{"name":"smaller"}],"name":"identifier"}],"name":"identifierPattern"}],"name":"patternWithoutRange"}],"name":"patternNoTopAlt"},{"name":"="},{"children":[{"children":[{"children":[{"children":[{"children":[{"children":[{"children":[{"name":"Rectangle"}],"name":"identifier"}],"name":"pathIdentSegment"}],"name":"pathExprSegment"}],"name":"pathInExpression"},{"name":"{"},{"children":[{"children":[{"children":[{"name":"length"}],"name":"identifier"},{"name":":"},{"children":[{"children":[{"name":"5"}],"name":"literalExpression"}],"name":"expression"}],"name":"structExprField"},{"name":","},{"children":[{"children":[{"name":"width"}],"name":"identifier"},{"name":":"},{"children":[{"children":[{"name":"1"}],"name":"literalExpression"}],"name":"expression"}],"name":"structExprField"},{"name":","}],"name":"structExprFields"},{"name":"}"}],"name":"structExprStruct"}],"name":"structExpression"}],"name":"expression"},{"name":";"}],"name":"letStatement"}],"name":"statement"},{"children":[{"children":[{"children":[{"children":[{"children":[{"children":[{"children":[{"name":"assert"}],"name":"identifier"}],"name":"simplePathSegment"}],"name":"simplePath"},{"name":"!"},{"name":"("},{"children":[{"children":[{"children":[{"children":[{"name":"larger"}],"name":"identifier"}],"name":"macroIdentifierLikeToken"}],"name":"tokenTreeToken"},{"children":[{"children":[{"name":"."}],"name":"macroPunctuationToken"}],"name":"tokenTreeToken"},{"children":[{"children":[{"children":[{"name":"can_hold"}],"name":"identifier"}],"name":"macroIdentifierLikeToken"}],"name":"tokenTreeToken"}],"name":"tokenTree"},{"children":[{"children":[{"name":"("},{"children":[{"children":[{"children":[{"name":"&"}],"name":"macroPunctuationToken"}],"name":"tokenTreeToken"},{"children":[{"children":[{"children":[{"name":"smaller"}],"name":"identifier"}],"name":"macroIdentifierLikeToken"}],"name":"tokenTreeToken"}],"name":"tokenTree"},{"name":")"}],"name":"delimTokenTree"}],"name":"tokenTree"},{"name":")"},{"name":";"}],"name":"macroInvocationSemi"}],"name":"macroItem"}],"name":"item"}],"name":"statement"}],"name":"statements"},{"name":"}"}],"name":"blockExpression"}],"name":"function_"}],"name":"visItem"}],"name":"item"},{"children":[{"children":[{"name":"#"},{"name":"["},{"children":[{"children":[{"children":[{"children":[{"name":"test"}],"name":"identifier"}],"name":"simplePathSegment"}],"name":"simplePath"}],"name":"attr"},{"name":"]"}],"name":"outerAttribute"},{"children":[{"children":[{"children":[],"name":"functionQualifiers"},{"name":"fn"},{"children":[{"name":"smaller_can_hold_larger"}],"name":"identifier"},{"name":"("},{"name":")"},{"children":[{"name":"{"},{"children":[{"children":[{"children":[{"name":"let"},{"children":[{"children":[{"children":[{"children":[{"name":"larger"}],"name":"identifier"}],"name":"identifierPattern"}],"name":"patternWithoutRange"}],"name":"patternNoTopAlt"},{"name":"="},{"children":[{"children":[{"children":[{"children":[{"children":[{"children":[{"children":[{"name":"Rectangle"}],"name":"identifier"}],"name":"pathIdentSegment"}],"name":"pathExprSegment"}],"name":"pathInExpression"},{"name":"{"},{"children":[{"children":[{"children":[{"name":"length"}],"name":"identifier"},{"name":":"},{"children":[{"children":[{"name":"8"}],"name":"literalExpression"}],"name":"expression"}],"name":"structExprField"},{"name":","},{"children":[{"children":[{"name":"width"}],"name":"identifier"},{"name":":"},{"children":[{"children":[{"name":"7"}],"name":"literalExpression"}],"name":"expression"}],"name":"structExprField"},{"name":","}],"name":"structExprFields"},{"name":"}"}],"name":"structExprStruct"}],"name":"structExpression"}],"name":"expression"},{"name":";"}],"name":"letStatement"}],"name":"statement"},{"children":[{"children":[{"name":"let"},{"children":[{"children":[{"children":[{"children":[{"name":"smaller"}],"name":"identifier"}],"name":"identifierPattern"}],"name":"patternWithoutRange"}],"name":"patternNoTopAlt"},{"name":"="},{"children":[{"children":[{"children":[{"children":[{"children":[{"children":[{"children":[{"name":"Rectangle"}],"name":"identifier"}],"name":"pathIdentSegment"}],"name":"pathExprSegment"}],"name":"pathInExpression"},{"name":"{"},{"children":[{"children":[{"children":[{"name":"length"}],"name":"identifier"},{"name":":"},{"children":[{"children":[{"name":"5"}],"name":"literalExpression"}],"name":"expression"}],"name":"structExprField"},{"name":","},{"children":[{"children":[{"name":"width"}],"name":"identifier"},{"name":":"},{"children":[{"children":[{"name":"1"}],"name":"literalExpression"}],"name":"expression"}],"name":"structExprField"},{"name":","}],"name":"structExprFields"},{"name":"}"}],"name":"structExprStruct"}],"name":"structExpression"}],"name":"expression"},{"name":";"}],"name":"letStatement"}],"name":"statement"},{"children":[{"children":[{"children":[{"children":[{"children":[{"children":[{"children":[{"name":"assert"}],"name":"identifier"}],"name":"simplePathSegment"}],"name":"simplePath"},{"name":"!"},{"name":"("},{"children":[{"children":[{"children":[{"name":"!"}],"name":"macroPunctuationToken"}],"name":"tokenTreeToken"},{"children":[{"children":[{"children":[{"name":"smaller"}],"name":"identifier"}],"name":"macroIdentifierLikeToken"}],"name":"tokenTreeToken"},{"children":[{"children":[{"name":"."}],"name":"macroPunctuationToken"}],"name":"tokenTreeToken"},{"children":[{"children":[{"children":[{"name":"can_hold"}],"name":"identifier"}],"name":"macroIdentifierLikeToken"}],"name":"tokenTreeToken"}],"name":"tokenTree"},{"children":[{"children":[{"name":"("},{"children":[{"children":[{"children":[{"name":"&"}],"name":"macroPunctuationToken"}],"name":"tokenTreeToken"},{"children":[{"children":[{"children":[{"name":"larger"}],"name":"identifier"}],"name":"macroIdentifierLikeToken"}],"name":"tokenTreeToken"}],"name":"tokenTree"},{"name":")"}],"name":"delimTokenTree"}],"name":"tokenTree"},{"name":")"},{"name":";"}],"name":"macroInvocationSemi"}],"name":"macroItem"}],"name":"item"}],"name":"statement"}],"name":"statements"},{"name":"}"}],"name":"blockExpression"}],"name":"function_"}],"name":"visItem"}],"name":"item"},{"name":"}"}],"name":"module"}],"name":"visItem"}],"name":"item"},{"name":"<EOF>"}],"name":"crate"}

# A simple vulnerability pattern (looking for direct unwrap calls)
vulnerability_pattern = {
    "type": "identifier"
}
