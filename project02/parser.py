class Token:
    def __init__(self, type, value, pos=None, line=None, column=None):
        self.type = type
        self.value = value
        self.pos = pos
        self.line = line
        self.column = column

    def __repr__(self):
        return f"Token({self.type}, {self.value}, Pos={self.pos}, Line={self.line}, Column={self.column})"


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
        tokens = []
        while self.current_char is not None:
            if self.current_char.isspace():
                self.advance()
            elif self.current_char == '+':
                tokens.append(Token(KP_PLUS, '+', self.pos, self.line, self.column))
                self.advance()
            elif self.current_char.isdigit():
                tokens.append(self.make_number())
            else:
                tokens.append(self.error())
                self.advance()
        tokens.append(Token('EOF', None))  # Ensure EOF token is added
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
    

class NumberNode:
    def __init__(self, token):
        self.token = token
        self.value = token.value
    def __repr__(self):

        return f"Number({self.value})"
    
class BiOpNode:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):
        return f"({self.left} {self.op.value} {self.right})"
    
class UnaryOpNode:
    def __init__(self, op, node):
        self.op = op
        self.node = node

    def __repr__(self):
        return f"({self.op.value}{self.node})"

    
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[self.pos]

    def consume_token(self, token_type):
        if self.current_token.type == token_type:
            self.pos += 1
            if self.pos < len(self.tokens):
                self.current_token = self.tokens[self.pos]
            else:
                self.current_token = Token(Token.EOF, None)
        else:
            raise Exception(f"Unexpected token {self.current_token.type}, expected{token_type}")
    
    def factor(self):
        token = self.current_token
        if token.type == Token.INTEGER:
            self.consume_token(Token.INTEGER)
            return NumberNode(token)
        raise Exception("Invalid factor")

    def term(self):
        left = self.factor()
        while self.current_token.type in ('MUL', 'DIV'):
            op_token = self.current_token
            self.consume_token(op_token.type)
            right = self.factor()
            left = BiOpNode(left, op_token, right)
        return left

    def expression(self):
        left = self.term()
        while self.current_token.type in ('PLUS', 'MINUS'):
            op_token = self.current_token
            self.consume_token(op_token.type)
            right = self.term()
            left = BiOpNode(left, op_token, right)
        return left
    
    def parse(self):
        """Parse the entire expression and return an AST."""
        return self.expression()


# AST Printer
def print_ast(node, indent=""):
    """Print AST in structured format."""
    if isinstance(node, NumberNode):
        print(f"{indent}Number({node.value})")
    elif isinstance(node, BiOpNode):
        print(f"{indent}BinOp({node.op.value})")
        print(f"{indent} Left:")
        print_ast(node.left, indent + "  ")
        print(f"{indent} Right:")
        print_ast(node.right, indent + "  ")
    elif isinstance(node, UnaryOpNode):
        print(f"{indent}UnaryOp({node.op.value})")
        print(f"{indent} Operand:")
        print_ast(node.node, indent + "  ")


def run(text):
    lexer = Lexer("<stdin>", text)
    tokens = lexer.make_tokens()
    parser = Parser(tokens)
    ast = parser.parse()
    print_ast(ast)

