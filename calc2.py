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

    def error(self):
        raise Exception('Error parsing input')
    
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

    def eat(self, token_type):
        
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()

    def expr(self):
        
        self.current_token = self.get_next_token()

        left = self.current_token
        self.eat(INTEGER)

        op = self.current_token
        if op.type == PLUS:
            self.eat(PLUS)
        else:
            self.eat(MINUS)

        right = self.current_token
        self.eat(INTEGER)

        if op.type == PLUS: 
            result = left.value + right.value3
        else:
            result = left.value - right.value

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




