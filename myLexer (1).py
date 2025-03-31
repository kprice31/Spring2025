# Author: Kelsi Price
# Date: 02/23/2025
# Time Taken: 3 hours
# Your commenting character used for the lexer: !

import re

# Create a Token class
class Token:
    def __init__(self, type_, value=None, index=0, line=1, column=1):
        self.type = type_
        self.value = value
        self.index = index
        self.line = line
        self.column = column

    def __repr__(self):
        return f"Output {self.type}: {repr(self.value)}\n line {self.line},\n Column: {self.column} \n(Index {self.index})"

# Token types
KP_INT = 'KP_INT'
KP_FLOAT = 'KP_FLOAT'
KP_PLUS = 'KP_PLUS'
KP_MINUS = 'KP_MINUS'
KP_MULT = 'KP_MULT'
KP_DIV = 'KP_DIV'
KP_LPAREN = 'KP_LPAREN'
KP_RPAREN = 'KP_RPAREN'
KP_COMMENT = 'KP_COMMENT'
KP_ILLEGAL = 'KP_ILLEGAL'

# Regular expression for digits
DIGITS = re.compile(r'\d+(\.\d+)?')

# Lexer class
class Lexer:
    COMMENT_CHAR = '!'

    def __init__(self, fn, text):
        self.fn = fn    
        self.text = text
        self.pos = -1 
        self.current_char = None
        self.line = 1
        self.column = 0
        self.advance()
        
    def advance(self):
        """Move to the next character."""
        self.pos += 1
        self.column += 1
        if self.pos < len(self.text):
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None

    def make_tokens(self):
        """Tokenize the input text."""
        tokens = []
        
        while self.current_char is not None:
            if self.current_char.isspace():
                if self.current_char == '\n':  # Newline handling
                    self.line += 1
                    self.column = 0
                self.advance()
            elif self.current_char == self.COMMENT_CHAR:
                self.skip_comment()
            elif self.current_char == '+':
                tokens.append(Token(KP_PLUS, '+', self.pos, self.line, self.column))
                self.advance()
            elif self.current_char == '-':
                tokens.append(Token(KP_MINUS, '-', self.pos, self.line, self.column))
                self.advance()
            elif self.current_char == '*':
                tokens.append(Token(KP_MULT, '*', self.pos, self.line, self.column))
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token(KP_DIV, '/', self.pos, self.line, self.column))
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token(KP_LPAREN, '(', self.pos, self.line, self.column))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(KP_RPAREN, ')', self.pos, self.line, self.column))
                self.advance()
            elif self.current_char.isdigit(): 
                tokens.append(self.make_number())
            else:
                tokens.append(self.error())
                self.advance()
        
        return tokens

    def make_number(self):
        """ Extracts an integer or floating-point number from the input."""
        num_str = ''
        dot_count = 0
        start_pos = self.pos
        start_column = self.column
        
        while self.current_char is not None and (self.current_char.isdigit() or self.current_char == '.'):
            if self.current_char == '.':
                if dot_count == 1:  # Prevent multiple dots
                    break
                dot_count += 1
            
            num_str += self.current_char
            self.advance()
        
        if not num_str:  
            return self.error()  # Return error if no valid number was formed

        if dot_count == 0:
            return Token(KP_INT, int(num_str), start_pos, self.line, start_column)
        else:
            return Token(KP_FLOAT, float(num_str), start_pos, self.line, start_column)

        

    def skip_comment(self):
        """Skip everything after the comment character on the same line."""
        while self.current_char is not None and self.current_char != '\n':
            self.advance()
    
    def error(self):
        """Report an error for an unrecognized character."""
        return Token(KP_ILLEGAL, self.current_char, self.pos, self.line, self.column)

# Executing function
def run(fn, text):
    lexer = Lexer(fn, text)
    tokens = lexer.make_tokens() 
    return tokens

