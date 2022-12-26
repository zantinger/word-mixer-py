from tokenizer import Tokenizer
from pprint import pprint


class Parser:
    """
    Parses a string into an AST.

    Attributes
    ----------
    _string: str
        the string to be parsed
    _tokenizer: Tokenizer
        convert string to tokens

    Methods
    -------
    parse(string) -> program
        parses the string ans return AST
    program() -> Node

    _eat(tokenType) -> token

    literal() -> numericLiteral | stringLiteral

    stringLiteral() -> Node

    numericLiteral() -> Node
    """

    def __init__(self):
        self._string = ""
        self._tokenizer = Tokenizer()

    def _eat(self, tokenType):
        token = self._lookahead

        if token == False:
            print("Unexpected end of input")

        if token["type"] != tokenType:
            print("Unexpected token")

        self._lookahead = self._tokenizer.get_next_token()

        return token

    def parse(self, string):
        """
        Parse recursively starting from the main entry point, the Program:
        """
        self._string = string
        self._tokenizer.run(string)

        self._lookahead = self._tokenizer.get_next_token()

        return self.program()

    def program(self):
        """
        Main entry point.

        Program
            : StatementList
            ;
        """
        return {"type": "Program", "body": self.statement_list()}

    def statement_list(self, stopLookahead=False):
        """
        StatementList
            : Statement
            : StatementList Statement
            ;
        """
        list = [self.statement()]

        while self._lookahead and self._lookahead["type"] != stopLookahead:
            list.append(self.statement())

        return list

    def statement(self):
        """
        Statement
            : ExpressionStatement
            : BlockStatement
            ;
        """
        l_type = self._lookahead["type"]

        if l_type == "{":
            return self.block_statement()
        elif l_type == "|":
            self._eat("|")
            return self.statement()
        else:
            return self.expression_statement()

    def block_statement(self):
        """
        BlockStatement
            : '{' OptStatementList '}'
            ;
        """
        self._eat("{")

        body = ""
        if self._lookahead["type"] != "}":
            body = self.statement_list("}")
        else:
            body = []

        self._eat("}")

        return {"type": "BlockStatement", "body": body}

    def expression_statement(self):
        """
        ExpressionStatement
            : Expression ';'
            ;
        """
        expression = self.expression()
        # self._eat(";")
        return {"type": "ExpressionStatement", "expression": expression}

    def expression(self):
        """
        Expression
            : Literal
            ;
        """
        return self.literal()

    def literal(self):
        if self._lookahead["type"] == "NUMBER":
            return self.numericLiteral()
        elif self._lookahead["type"] == "STRING":
            return self.stringLiteral()

    def stringLiteral(self):
        token = self._eat("STRING")
        return {"type": "StringLiteral", "value": token["value"]}

    def numericLiteral(self):
        token = self._eat("NUMBER")
        return {"type": "NumericLiteral", "value": int(token["value"])}

