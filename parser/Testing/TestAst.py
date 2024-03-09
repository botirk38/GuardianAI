import unittest

from parser.ast_analysis.ast_comparer import compare_ast

class TestASTComparison(unittest.TestCase):

    def test_traverse_and_compare_finds_method_call(self):
        mock_ast = {
            "type": "MethodCall",
            "method": "unwrap",
            "children": []
        }
        pattern = {"type": "MethodCall", "method": "unwrap"}
        self.assertTrue(compare_ast(mock_ast, pattern))

    def test_traverse_and_compare_does_not_find_incorrect_method_call(self):
        mock_ast = {
            "type": "MethodCall",
            "method": "expect",
            "children": []
        }
        pattern = {"type": "MethodCall", "method": "unwrap"}
        self.assertFalse(compare_ast(mock_ast, pattern))

    def test_traverse_and_compare_handles_nested_structure(self):
        mock_ast = {
            "type": "Function",
            "name": "my_function",
            "children": [
                {
                    "type": "MethodCall",
                    "method": "unwrap",
                    "children": []
                }
            ]
        }
        pattern = {"type": "MethodCall", "method": "unwrap"}
        self.assertTrue(compare_ast(mock_ast, pattern))



if __name__ == '__main__':
    unittest.main()
