

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
unwrap_ast = {
    "type": "MethodCall",
    "name": "unwrap",
    "children": [
        {
            "type": "Variable",
            "name": "possible_error",
        }
    ],
    "line": 10
}
wildcard_import_ast = {
    "type": "UseDeclaration",
    "path": "std::io::*",
    "line": 5
}
magic_number_ast = {
    "type": "Literal",
    "value": 42,
    "line": 20
}
clippy_lints_ignored_ast = {
    "type": "Attribute",
    "name": "allow(clippy::some_lint)",
    "line": 8
}
todo_comment_ast = {
    "type": "Comment",
    "value": "TODO: Refactor this function to use better error handling",
    "line": 15
}

