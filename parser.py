from tokenizer import Tokenizer


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

    def parse(self, string):
        """
        Parse recursively starting from the main entry point, the Program:
        """
        self._string = string
        self._tokenizer.run(string)

        self._lookahead = self._tokenizer.get_next_token()

        return self.program()

    def program(self):
        return {"type": "Program", "body": self.literal()}

    def _eat(self, tokenType):
        token = self._lookahead

        if token == False:
            print("Unexpected end of input")

        if token["type"] != tokenType:
            print("Unexpected token")

        self._lookahead = self._tokenizer.get_next_token()

        return token

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


if __name__ == "__main__":
    parser = Parser()
    program = "  'foo'"
    ast = parser.parse(program)

    print(ast)
