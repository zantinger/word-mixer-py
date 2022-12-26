import unittest
from parser import Parser


class TestParser(unittest.TestCase):

    maxDiff = None

    def test_no_blockstatement(self):
        parser = Parser()
        program = "Hello World"
        ast = parser.parse(program)

        expect = {
            "type": "Program",
            "body": [
                {
                    "type": "ExpressionStatement",
                    "expression": {"type": "StringLiteral", "value": "Hello World"},
                },
            ],
        }
        self.assertEqual(ast, expect)

    def test_string_in_blockstatement(self):
        parser = Parser()
        program = "Hello {World}"
        ast = parser.parse(program)

        expect = {
            "type": "Program",
            "body": [
                {
                    "type": "ExpressionStatement",
                    "expression": {"type": "StringLiteral", "value": "Hello "},
                },
                {
                    "type": "BlockStatement",
                    "body": [
                        {
                            "type": "ExpressionStatement",
                            "expression": {"type": "StringLiteral", "value": "World"},
                        },
                    ],
                },
            ],
        }
        self.assertEqual(ast, expect)

    def test_blockstatement(self):
        parser = Parser()
        program = "Hello {World|Earth} !"
        ast = parser.parse(program)

        expect = {
            "type": "Program",
            "body": [
                {
                    "type": "ExpressionStatement",
                    "expression": {"type": "StringLiteral", "value": "Hello "},
                },
                {
                    "type": "BlockStatement",
                    "body": [
                        {
                            "type": "ExpressionStatement",
                            "expression": {"type": "StringLiteral", "value": "World"},
                        },
                        {
                            "type": "ExpressionStatement",
                            "expression": {"type": "StringLiteral", "value": "Earth"},
                        },
                    ],
                },
                {
                    "type": "ExpressionStatement",
                    "expression": {"type": "StringLiteral", "value": " !"},
                },
            ],
        }
        self.assertEqual(ast, expect)

    def test_nested_blockstatement(self):
        parser = Parser()
        program = "Hello {World|{John|Marry}} !"
        ast = parser.parse(program)

        expect = {
            "type": "Program",
            "body": [
                {
                    "type": "ExpressionStatement",
                    "expression": {"type": "StringLiteral", "value": "Hello "},
                },
                {
                    "type": "BlockStatement",
                    "body": [
                        {
                            "type": "ExpressionStatement",
                            "expression": {"type": "StringLiteral", "value": "World"},
                        },
                        {
                            "type": "BlockStatement",
                            "body": [
                                {
                                    "type": "ExpressionStatement",
                                    "expression": {
                                        "type": "StringLiteral",
                                        "value": "John",
                                    },
                                },
                                {
                                    "type": "ExpressionStatement",
                                    "expression": {
                                        "type": "StringLiteral",
                                        "value": "Marry",
                                    },
                                },
                            ],
                        },
                    ],
                },
                {
                    "type": "ExpressionStatement",
                    "expression": {"type": "StringLiteral", "value": " !"},
                },
            ],
        }
        self.assertEqual(ast, expect)


if __name__ == "__main__":
    unittest.main()
