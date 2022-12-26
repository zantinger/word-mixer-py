import re

SPECS = [
    ('[^({|}|\|)]*', "STRING"),
    ("{", "{"),
    ("}", "}"),
    ("\|", "|"),
]


class Tokenizer:
    """
    Tokenizer class.

    Lazily pulls a token from a stream.

    Attribute
    ---------
    _string: str
    _cursor: int

    Methods
    -------
    has_more_token() -> Boolean

    is_integer(string, num) -> Boolean

    isEOF() -> Boolean

     _match(regexp, string) -> group|None

    get_next_token() -> Node|Raise
    """

    def _match(self, regexp, string):
        """Look for matched regep in string."""
        matched = re.match(regexp, string)
        if matched:
            group = matched.group()
            self._cursor += len(group)
            return group
        else:
            return matched

    # Initializing
    def run(self, string):
        self._string = string
        self._cursor = 0

    def has_more_token(self):
        """Whether we still have more tokens."""
        return self._cursor < len(self._string)

    def is_integer(self, string, num):
        """Save check if char is integer."""
        number = string[num]
        try:
            number = int(string[num])
        except ValueError:
            print("I am afraid %s is not a number" % number)
            return False
        except IndexError:
            print("I am afraid you are out of range")
            return False
        else:
            print("number is %s" % number)
            return True

    def isEOF(self):
        """Wheter the tokenizer reached EOF."""
        return self._cursor == len(self._string)

    # Obtains next token.
    def get_next_token(self):
        """Get the next matched group and assign it to a token"""
        if not self.has_more_token():
            return False
        else:
            string = self._string[self._cursor :]

            for regexp, token_type in SPECS:
                token_value = self._match(regexp, string)
                # print("----")
                # print(token_type)
                # print(token_value)
                # print(string)


                if token_value and token_type == "EMPTY":
                    return self.get_next_token()
                elif token_value:
                    return {"type": token_type, "value": token_value}
                else:
                    continue

            raise Exception("FEHLER")
