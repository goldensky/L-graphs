from collections import OrderedDict
from enum import Enum      
from  L_class_Token import Token



ID = 'ID'

TD = [
    "null",
    "+",    # 1
    "-",    # 2
    "*",    # 3
    "/",    # 4
    "(",    # 5
    ")",    # 6
    "{",    # 7
    "}",    # 8
    "[",    # 9
    "]",    # 10
    ";",    # 11
    "=",    # 12
    ":",    # 13
    ":=",   # 14
    "<",    # 15
    ">",    # 16
    "<>",   # 17
    "<=",   # 18
    ">=",   # 19
    ".",    # 20
    ",",    # 21
    "'",    # 22
    "^",    # 23
    "@"     # 24
    ]


class dlms(Enum):
    NULL = 0
    PLUS =  1
    MINUS = 2
    TIMES = 3
    SLASH = 4
    LPAREN = 5
    RPAREN = 6
    L_COMMENT = 7
    R_COMMENT = 8
    LSQB = 9
    RSQB = 10
    SEMI = 11
    EQ = 12
    COLON = 13
    ASSIGN = 14
    LT = 15
    GT = 16
    NEQ = 17
    LEQ = 18
    GEQ = 19
    DOT = 20
    COMMA = 21
    QUOTE_MARK = 22
    CIRCUMFLEX = 23
    AT = 24



TW = [
    "null",              
    "and",          # 1
    "array",        # 2
    "begin",        # 3
    "case",         # 4
    "const",        # 5
    "div",          # 6
    "do",           # 7
    "downto",       # 8
    "else",         # 9
    "end",          # 10
    "file",         # 11
    "for",          # 12
    "function",     # 13
    "goto",         # 14
    "if",           # 15
    "label",        # 16
    "mod",          # 17
    "nil",          # 18
    "not",          # 19
    "of",           # 20
    "or",           # 21
    "procedure",    # 22
    "program",      # 23
    "record",       # 24
    "repeat",      # 25
    "then",         # 26
    "to",           # 27
    "type",         # 28
    "until",        # 29
    "var",          # 30
    "while",        # 31
    "with",         # 32
    "xor"         # 33
    ]

class words(Enum):
    NULL = 0             
    AND = 1
    ARRAY = 2
    BEGIN = 3
    CASE = 4
    CONST = 5
    DIV = 6
    DO = 7
    DOWNTO = 8
    ELSE = 9
    END = 10
    FILE = 11
    FOR = 12
    FUNCTION = 13
    GOTO = 14
    IF = 15
    LABEL = 16
    MOD = 17
    NIL = 18
    NOT = 19
    OF = 20
    OR = 21
    PROCEDURE = 22
    PROGRAM = 23
    RECORD = 24
    REPEAT = 25
    THEN = 26
    TO = 27
    TYPE = 28
    UNTIL = 29
    VAR = 30
    WHILE = 31
    WITH = 32
    XOR = 33




ST_ID = [
    "null",
    "abs",          # 1
    "arctan",       # 2
    "integer",      # 3
    "real",         # 4
    "read",         # 5
    "readln",       # 6
    "write",        # 7
    "writeln",      # 8
    "input",        # 9
    "output",       # 10
    "sin",          # 11
    "cos",          # 12
    "ln",           # 13
    "sqr",          # 14
    "sqrt",         # 15
    "chr",          # 16
    "ord",          # 17
    "odd",          # 18
    "eoln",         # 19
    "eof",          # 20
    "exp",          # 21
    "round",        # 22
    "trunc",        # 23
    "frac",         # 24
    "MaxInt",       # 25
    "sizeof",       # 26
    "pred",         # 27
    "succ",         # 28
    "string",       # 29
    "boolean",      # 30
    "char",         # 31
    "byte",         # 32
    "true",         # 33
    "false",         # 34
    "ID" ,           # 35
    "UNEXPECTED_LEXEM"    # 36
    ]


class st_id_lex(Enum):
    NULL = 0
    ABS = 1
    ARCTAN = 2
    INTEGER = 3  #
    REAL = 4     #
    READ = 5
    READLN = 6
    WRITE = 7
    WRITELN = 8
    INPUT = 9
    OUTPUT = 10
    SIN = 11
    COS = 12
    LN = 13
    SQR = 14
    SQRT = 15
    CHR = 16
    ORD = 17
    ODD = 18
    EOLN = 19
    EOF = 20
    EXP = 21
    ROUND = 22
    TRUNC = 23
    FRAC = 24
    MAXINT = 25
    SIZEOF = 26
    PRED = 27
    SUCC = 28
    STRING = 29
    BOOLEAN = 30
    CHAR = 31
    BYTE = 32
    TRUE = 33
    FALSE = 34   
    ID = 35
    UNEXPECTED_LEXEM = 36


flag_Unexpected_Lexem = False

STRING_LEXEM = 'STRING_LEXEM'
UNEXPECTED_LEXEM = 'UNEXPECTED_LEXEM'
INTEGER_CONST = 'INTEGER_CONST'
REAL_CONST = 'REAL_CONST'
EOF = 'EOF'


class UnexpectedLexem(Exception):
    def __init__(self, message):
        self.message = message
        #print(message)
        self.end_prog()
        
    def end_prog(self):
        global flag_Unexpected_Lexem
        flag_Unexpected_Lexem =  Token(UNEXPECTED_LEXEM, 36)

        
class Ident:
    def __init__(self, name):
        self.name = name
        self.declare = False

    def __str__(self):
        return '{0}'.format(self.name)

    def __repr__(self):
        return self.__str__()
        

class Table_Ident:
    def __init__(self):
        self._table = []
        self.size = 0

    def put(self, new_name, declare=False):
        try:
            l = [ident.name for ident in self._table]
            line = l.index(new_name)
        except (ValueError, UnboundLocalError):
            ident = Ident(new_name)
            if declare == True:
                ident.declare = True
            self._table.append(ident)
            l2 = [ident.name for ident in self._table]
            line = l2.index(new_name)
            self.size += 1
        return line


    def __str__(self):
        return 'Table {s}'.format(
            s = [s for s in self._table])   

    def __repr__(self):
        return self.__str__()


 
class Lexer:    
    '''
    Returns one token each time it is accessed

    '''
    def __init__(self, student_solution_text):
        self.text = student_solution_text
        self.pos = 0
        self.current_char = self.text[self.pos]
        self.line_number = 1
        self.table = Table_Ident()
    

    def advance(self):
        '''
        Reading one leading symbol and assigning its value 
        to the current symbol.
        '''
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def peek(self):
        '''
        Reading one leading symbol.
        '''
        peek_pos = self.pos + 1
        if peek_pos > len(self.text) - 1:
            return None
        else:
            return self.text[peek_pos]

    def skip_whitespace(self):
        '''
        Skipping whitespaces.
        '''
        while self.current_char is not None and self.current_char.isspace():
            if self.current_char == '\n':
                self.line_number += 1           
            self.advance()
   
    def number(self):
        '''
        Returns the number(integer, real).
        '''
        number = ''
        while self.current_char is not None and self.current_char.isdigit():
            number += self.current_char
            self.advance()

        if self.current_char == '.':
            number += self.current_char
            self.advance()
            
            while (self.current_char is not None
                   and self.current_char.isdigit()):
                number += self.current_char
                self.advance()
            token = Token(REAL_CONST, float(number))
        else:
            token = Token(INTEGER_CONST,  int(number))
        return token

    def skip_comments(self):
        while self.current_char != '}':
            self.advance()
        self.advance()

    def identifier(self):
        '''
        Returns an identifier or a keyword.
        '''
        ident = ''
        while (self.current_char is not None
               and (self.current_char.isalnum() or self.current_char == '_')):
            ident += self.current_char
            self.advance()
            
        try:
            j = TW.index(ident.lower())
            token = Token(words(j).name, j)

        except ValueError as err:
            try:
                j = ST_ID.index(ident.lower())
                token = Token(st_id_lex(j).name, j)

            except ValueError as er2:
                
                j = self.table.put(ident)
                token = Token(ID, j)
 
        return token

    def make_string_lexem(self):
        '''
        Collects the string lexeme this_is_string_lexem inside
        quotation marks
        write(max,'this_is_string_lexem',  min)
    
        '''
        flag = 0
        end_string_lexem_flag = 0
        string_lexem = ''
        while self.current_char is not None and end_string_lexem_flag != 1:
            if flag == 1:
                if self.current_char == "'":
                    flag = 0           #   string_lexem ends
                    token = Token(STRING_LEXEM, "{0}".format(str(string_lexem)))
                    string_lexem = ''
                    end_string_lexem_flag = 1
                else:
                    string_lexem += self.current_char
            else:                       # flag == 0
                if self.current_char == "'":
                    flag = 1
            self.advance()
        return token

    def get_next_token(self):
        try:
            while self.current_char is not None:
                if self.current_char.isspace():
                    self.skip_whitespace()
                    continue
                
                elif self.current_char == '{':
                    self.advance()
                    self.skip_comments()
                    continue

                elif self.current_char.isdigit():
                    return self.number()

                elif self.current_char.isalpha() or self.current_char == '_':
                    return self.identifier()

                elif self.current_char == '+':  #   Token(PLUS, '+')
                    j = TD.index(self.current_char)
                    self.advance()
                    token = Token(dlms(j).name, j)
                    return token    

                elif self.current_char == '-':  #  Token(TIMES, '*')
                    j = TD.index(self.current_char)
                    self.advance()
                    token = Token(dlms(j).name, j)
                    return token 

                elif self.current_char == '*':   
                    j = TD.index(self.current_char)
                    self.advance()
                    token = Token(dlms(j).name, j)
                    return token

                elif self.current_char == '/':  # Token(DIVIDE, '/')
                    j = TD.index(self.current_char)
                    self.advance()
                    token = Token(dlms(j).name, j)
                    return token

                elif self.current_char == '(':
                    j = TD.index(self.current_char)
                    self.advance()
                    token = Token(dlms(j).name, j)
                    return token

                elif self.current_char == ')':  #  Token(RPAREN, ')')
                    j = TD.index(self.current_char)
                    self.advance()
                    token = Token(dlms(j).name, j)
                    return token

                elif self.current_char == '{':  # Token(L_COMMENT, '{')
                    j = TD.index(self.current_char)
                    self.advance()
                    token = Token(dlms(j).name, j)
                    return token
                    

                elif self.current_char == '}':  # Token(R_COMMENT, '}')
                    j = TD.index(self.current_char)
                    self.advance()
                    token = Token(dlms(j).name, j)
                    return token

                elif self.current_char == ';':  # Token(SEMI, ';')
                    j = TD.index(self.current_char)
                    self.advance()
                    token = Token(dlms(j).name, j)
                    return token

                elif self.current_char == '=':  # Token(EQ, '=')
                    j = TD.index(self.current_char)
                    self.advance()
                    token = Token(dlms(j).name, j)
                    return token

                elif self.current_char == ':' and self.peek() == '=':   # Token(ASSIGN, ':=')
                    temp = self.current_char + self.peek()
                    j = TD.index(temp)
                    self.advance()
                    self.advance()
                    token = Token(dlms(j).name, j)
                    return token
                
                elif self.current_char == ':':  # Token(COLON, ':')
                    j = TD.index(self.current_char)
                    self.advance()
                    token = Token(dlms(j).name, j)
                    return token

                elif self.current_char == '<' and self.peek() == '>':  # Token(NEQ, '<>')
                    temp = self.current_char + self.peek()
                    j = TD.index(temp)
                    self.advance()
                    self.advance()
                    token = Token(dlms(j).name, j)
                    return token

                elif self.current_char == '<' and self.peek() == '=':  # Token(LEQ, '<=')
                    temp = self.current_char + self.peek()
                    j = TD.index(temp)
                    self.advance()
                    self.advance()
                    token = Token(dlms(j).name, j)
                    return token

                elif self.current_char == '<':  # Token(LT, '<')
                    j = TD.index(self.current_char )
                    self.advance()
                    token = Token(dlms(j).name, j)
                    return token
                
                elif self.current_char == '>' and self.peek() == '=':   # Token(GEQ, '>=')
                    temp = self.current_char + self.peek()
                    j = TD.index(temp)
                    self.advance()
                    self.advance()
                    token = Token(dlms(j).name, j)
                    return token

                elif self.current_char == '>' and self.peek() == '=':  # Token(GEQ, '>=')
                    temp = self.current_char + self.peek()
                    j = TD.index(temp)
                    self.advance()
                    self.advance()
                    token = Token(dlms(j).name, j)
                    return token

                elif self.current_char == '>':  # Token(GT, '>')
                    j = TD.index(self.current_char)
                    self.advance()
                    token = Token(dlms(j).name, j)
                    return token

                elif self.current_char == '[':  # Token(LSQB, '[')
                    j = TD.index(self.current_char)
                    self.advance()
                    token = Token(dlms(j).name, j)
                    return token

                elif self.current_char == ']':  # Token(RSQB, ']')
                    j = TD.index(self.current_char)
                    self.advance()
                    token = Token(dlms(j).name, j)
                    return token

                elif self.current_char == '.':  # Token(DOT, '.')
                    j = TD.index(self.current_char)
                    self.advance()
                    token = Token(dlms(j).name, j)
                    return token

                elif self.current_char == '@':  # Token(AT, '@')
                    j = TD.index(self.current_char)
                    self.advance()
                    token = Token(dlms(j).name, j)
                    return token

                elif self.current_char == ',':  # Token(COMMA, ',')
                    j = TD.index(self.current_char)
                    self.advance()
                    token = Token(dlms(j).name, j)
                    return token

                elif self.current_char == "'":
                    return self.make_string_lexem()

                

                elif self.current_char == "^":       
                    j = TD.index(self.current_char)
                    self.advance()
                    token = Token(dlms(j).name, j)
                    return token
                
                    
                else:
                    raise UnexpectedLexem("Unexpected lexem '{0}' was found in {1} string"
                                        .format(self.current_char, self.line_number))

        
        except UnexpectedLexem as err1:
            print(err1)
            return Token(EOF, 20)   #   Token(EOF, None)# 
                    
        except AttributeError as err:
            return Token(EOF, 20)

        return Token(EOF, 20)



def main():
    file = 'task1.pas'
    all_tokens = []
    with open(file) as fh:
        text = fh.read()
    print(text)

    lexer = Lexer(text)
    token = lexer.get_next_token()
    all_tokens.append(token)
    while token.type != EOF:
        token = lexer.get_next_token()
        all_tokens.append(token)
   
    for i in all_tokens:
        print(i)
        
    print(lexer.table)
    print(lexer.table.size)


    
if __name__ == '__main__':
    main()
    
