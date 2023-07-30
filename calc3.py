INTEGER, PLUS, EOF, MINUS = 'INTERGER', 'PLUS', 'EOF', 'MINUS'

class Token():
    """It is a common model for every single character, including a type and a value"""
    def __init__(self, type, value) -> None:
        self.type = type
        self.value = value

    def __str__(self) -> str:
        return f'Token({self.type}, {self.value})'
    
    def __repr__(self) -> str:
        return self.__str__()
    
class Interpreter():

    def __init__(self, text) -> None:
        self.text = text                            # Text is what user input.
        self.pos = 0                                # Position stands for where the pointer stays.
        self.current_token = None                   # Initially to be None
        self.current_char = self.text[self.pos]

    ##########################################################
    # Lexer code                                             #
    ##########################################################

    def error(self):
        raise Exception('Invalid syntax')
    
    def advance(self):
        
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None

        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        """Return a (multidigit) integer consumed from the input."""
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        
        return int(result)
    
    def get_next_token(self):
        """Token Interpreter. For breaking a sentence into \
            tokens. One token at a time"""
        
        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return Token(INTEGER, self.integer())
            
            if self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')
            
            if self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')
            
            self.error()

        return Token(EOF, None)

    ##########################################################
    # Parser / Interpreter code                              #
    ##########################################################
    
    def eat(self, token_type):
        # compare the current token type with the passed type
        # if they match then "eat" the current type
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()

    def term(self) -> int:
        token = self.current_token
        self.eat(INTEGER)
        return token.value
    
    def expr(self):

        # set the current token to the first token from input
        self.current_token = self.get_next_token()
        
        result = self.term()
        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
                result = result + self.term()
            elif token.type == MINUS:
                self.eat(MINUS)
                result = result - self.term()
        
        return result
    
def main():
    while True:
        try:
            text = input('calc> ')
        except EOFError:
            break
        if not text:
            continue
        interpreter = Interpreter(text)
        result = interpreter.expr()
        print(result)

if __name__ == '__main__':
    main()




