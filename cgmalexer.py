#CONSTANTS

ALPHA_LOWER = 'abcdefghijklmnopqrstuvwxyz'
ALPHA_UPPER = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
ALPHA = ALPHA_LOWER + ALPHA_UPPER
ZERO = '0'
DIGITS = '123456789'
NUM = ZERO + DIGITS
ALPHANUM = ALPHA + NUM
PUNCTUATIONS = '!@#$%^&*()-_=+[]}{|\:;’”,<>.?/ '
ASCII = ALPHANUM + PUNCTUATIONS
ARITH_OPER = '+-/*%'
RELAT_OPER = '<>!='
OPER = ARITH_OPER + RELAT_OPER

#DELIMITERS

clbra_dlm = ' +='
clcur_dlm = ' \n)}'
clpar_dlm = ' \n}{)&|}' + ARITH_OPER
com_dlm = ' ('
comma_dlm = ' _' + ALPHANUM
comnt_dlm = ' \n' + ASCII
endln_dlm = ' \n'
esc_dlm = ' "'+ ASCII
equal_dlm = ' _[(-"+' + ALPHANUM
hawk_dlm = ' \n{'
identif_dlm = ' )(' + OPER
lit_dlm = ' ,)' + OPER
npc_dlm = ' :'
opbra_dlm = ' "' + ALPHANUM
opcur_dlm = ' \n' + ALPHANUM
operator_dlm = ' _(' + ALPHANUM
oppar_dlm = ' _)("-' + ALPHANUM
plus_dlm = ' _(["' + ALPHANUM
relat_dlm = ' _("' + ALPHANUM
scolon_dlm = ' _+-' + ALPHANUM
space_dlm = ' '
unary_dlm = ' _)' + ALPHANUM

#POSITION TRACK

class Position:
    def __init__(self, idx, ln, col, fn, ftxt):
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fn = fn
        self.ftxt = ftxt

    def advance(self, current_char):
        self.idx += 1
        self.col += 1

        if current_char == '\n':
            self.ln +=1
            self.col = 0

        return self
    
    def copy(self):
        return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)
        

#ERROR

class Error:
    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details

    def as_string(self):
        result = f'{self.error_name}: {self.details}'
        result += f'File {self.pos_start.fn}, line {self.pos_start.ln + 1}'
        return result
    
class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Illegal Character', details)

#TOKENS

TT_CHUNGUS      = 'CHUNGUS'     # Whole Numbers '3'
TT_CHUDELUXE    = 'CHUDELUXE'   # Decimal Numbers '3.14'
TT_FORSEN       = 'FORSEN'  # Strings 

TT_PLUS         = 'PLUS'    # '+'
TT_MINUS        = 'MINUS'   # '-'
TT_MUL          = 'MUL'     # '*'
TT_DIV          = 'DIV'     # '/'
TT_MOD          = 'MOD'     # '%'
TT_IS           = 'IS'      # '='

TT_EQ           = 'EQ'      # '=='  
TT_NEQ          = 'NEQ'     # '!='
TT_INC          = 'INC'     # '++'
TT_DEC          = 'DEC'     # '--'

TT_NOT          = 'NOT'     # '!'
TT_AND          = 'AND'     # '&&'
TT_OR           = 'OR'      # '||'
TT_LT           = 'LT'      # '<'
TT_GT           = 'GT'      # '>'
TT_LTE          = 'LTE'     # '<='
TT_GTE          = 'GTE'     # '>='

TT_OPPAR       = 'OPPAR'  # '('
TT_CLPAR       = 'CLPAR'  # ')'
TT_LSQUARE      = 'LSQUARE' # '['
TT_RSQUARE      = 'RSQUARE' # ']'
TT_LBRACE       = 'LBRACE'  # '{'
TT_RBRACE       = 'RBRACE'  # '}'
TT_SEMICOL      = 'SEMICOL' # ';'
TT_COL          = 'COLON'   # ':'
TT_COMMA        = 'COMMA'   # ','

TT_EOF          = 'EOF'     # End of File

TT_KEYWORD      = 'KEYWORD' # Keywords
TT_IDENTIFIER   = 'IDENTIFIER' # Identifiers

TT_ESCAPESEQUENCE = 'ESCAPESEQUENCE' # Escape Sequence

RESERVED_KEYWORDS = ['append', 'aura', 'back', 'caseoh', 'chat', 'chudeluxe', 'chungus', 'false', 'forsen', 'getout', 'gng', 'hawk', 'hawk tuah', 'insert', 'jit', 'lethimcook', 'lwk', 'nocap', 'npc', 'pause', 'plug', 'remove', 'skibidi', 'sturdy', 'true', 'tuah', 'yap']
RESERVED_SYMBOLS = [
    # Unary Operators
    '++', '--', '-',

    # Relational Operators
    '==', '!=', '>', '<', '>=', '<=',

    # Arithmetic Operators
    '+', '-', '*', '/', '%',

    # Logical Operators
    '&&', '||', '!',

    # Other Symbols
    '“', '\\', '(', ')', '[', ']', '{', '}', ',', '//', '/*', '*/', ';'
]

class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

    def __repr__(self):
        if self.value: return f'{self.type}:{self.value}'  
        return f'{self.type}'
    

#LEXER

class Lexer:
    def __init__(self, fn, text):
        self.fn = fn
        self.text = text
        self.pos = Position(-1, 0, -1, fn, text)
        self.current_char = None
        self.advance()

    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.idx] if self.pos.idx<len(self.text) else None

    def make_tokens(self):
        tokens = []
        
        while self.current_char != None:
            if self. current_char in ' \t':
                self.advance()
                
            elif self.current_char in ALPHA:
                ident_str = ''
                ident_count = 0
                pos_start = self.pos.copy()
                #Letter A
                if self.current_char == "a":
                    ident_str += self.current_char
                    ident_count+=1
                    self.advance()
                    if self.current_char == "p":
                        ident_str += self.current_char
                        ident_count+=1
                        self.advance()
                        if self.current_char == "p":
                            ident_str += self.current_char
                            ident_count+=1
                            self.advance()
                            if self.current_char == "e":
                                ident_str += self.current_char
                                ident_count+=1
                                self.advance()
                                if  self.current_char == "n":
                                    ident_str += self.current_char
                                    ident_count+=1
                                    self.advance()
                                    if self.current_char == "d":
                                        ident_str += self.current_char
                                        ident_count+=1
                                        tokens.append(Token(TT_KEYWORD))
                                        self.advance()
                    elif self.current_char == "u":
                        ident_str += self.current_char
                        ident_count+=1
                        self.advance()
                        if self.current_char == "r":
                            ident_str += self.current_char
                            ident_count+=1
                            self.advance()
                            if self.current_char == "a":
                                ident_str += self.current_char
                                ident_count+=1
                                tokens.append(Token(TT_KEYWORD))
                                self.advance()
                #Letter B
                if self.current_char == "b":
                    ident_str += self.current_char
                    ident_count+=1
                    self.advance()
                    if self.current_char == "a":
                        ident_str += self.current_char
                        ident_count+=1
                        self.advance()
                        if self.current_char == "c":
                            ident_str += self.current_char
                            ident_count+=1
                            self.advance()
                            if self.current_char == "k":
                                ident_str += self.current_char
                                ident_count+=1
                                tokens.append(Token(TT_KEYWORD))
                                self.advance()
                #Letter C
                if self.current_char == "c":
                    ident_str += self.current_char
                    ident_count += 1
                    self.advance()
                    if self.current_char == "a":
                        ident_str += self.current_char
                        ident_count += 1
                        self.advance()
                        if self.current_char == "s":
                            ident_str += self.current_char
                            ident_count += 1
                            self.advance()
                            if self.current_char == "e":
                                ident_str += self.current_char
                                ident_count += 1
                                self.advance()
                                if self.current_char == "o":
                                    ident_str += self.current_char
                                    ident_count += 1
                                    self.advance()
                                    if self.current_char == "h":
                                        ident_str += self.current_char
                                        ident_count += 1
                                        tokens.append(Token(TT_KEYWORD))
                                        self.advance()
                    elif self.current_char == "h":
                        ident_str += self.current_char
                        ident_count += 1
                        self.advance()
                        if self.current_char == "a":
                            ident_str += self.current_char
                            ident_count += 1
                            self.advance()
                            if self.current_char == "t":
                                ident_str += self.current_char
                                ident_count += 1
                                tokens.append(Token(TT_KEYWORD))
                                self.advance()
                        if self.current_char == "u":
                            ident_str += self.current_char
                            ident_count+=1
                            self.advance()
                            if self.current_char == "n":
                                ident_str += self.current_char
                                ident_count+=1
                                self.advance()
                                if self.current_char == "g":
                                    ident_str += self.current_char
                                    ident_count+=1
                                    self.advance() 
                                    if self.current_char == "u":
                                        ident_str += self.current_char
                                        ident_count+=1
                                        self.advance()      
                                        if self.current_char == "s":
                                            ident_str += self.current_char
                                            ident_count+=1
                                            tokens.append(Token(TT_KEYWORD))
                                            self.advance()  
                        elif self.current_char == "d":
                            ident_str += self.current_char
                            ident_count+=1
                            self.advance()
                            if self.current_char == "e":
                                ident_str += self.current_char
                                ident_count+=1
                                self.advance()
                                if self.current_char == "l":
                                    ident_str += self.current_char
                                    ident_count+=1
                                    self.advance()
                                    if self.current_char == "u":
                                        ident_str += self.current_char
                                        ident_count+=1
                                        self.advance()
                                        if self.current_char == "x":
                                            ident_str += self.current_char
                                            ident_count+=1
                                            self.advance()
                                            if self.current_char == "e":
                                                ident_str += self.current_char
                                                ident_count+=1
                                                tokens.append(Token(TT_KEYWORD))
                                                self.advance()        

                # Letter F
                if self.current_char == "f":
                    ident_str += self.current_char
                    ident_count += 1
                    self.advance()
                    if self.current_char == "a":
                        ident_str += self.current_char
                        ident_count += 1
                        self.advance()
                        if self.current_char == "l":
                            ident_str += self.current_char
                            ident_count += 1
                            self.advance()
                            if self.current_char == "s":
                                ident_str += self.current_char
                                ident_count += 1
                                self.advance()
                                if self.current_char == "e":
                                    ident_str += self.current_char
                                    ident_count += 1
                                    tokens.append(Token(TT_KEYWORD))
                                    self.advance()
                    if self.current_char == "o":
                        ident_str += self.current_char
                        ident_count += 1
                        self.advance()
                        if self.current_char == "r":
                            ident_str += self.current_char
                            ident_count += 1
                            self.advance()
                            if self.current_char == "s":
                                ident_str += self.current_char
                                ident_count += 1
                                self.advance()
                                if self.current_char == "e":
                                    ident_str += self.current_char
                                    ident_count += 1
                                    self.advance()
                                    if self.current_char == "n":
                                        ident_str += self.current_char
                                        ident_count += 1
                                        tokens.append(Token(TT_KEYWORD))
                                        self.advance()
                # Letter G
                if self.current_char == "g":
                    ident_str += self.current_char
                    ident_count += 1
                    self.advance()
                    if self.current_char == "e":
                        ident_str += self.current_char
                        ident_count += 1
                        self.advance()
                        if self.current_char == "t":
                            ident_str += self.current_char
                            ident_count += 1
                            self.advance()
                            if self.current_char == "o":
                                ident_str += self.current_char
                                ident_count += 1
                                self.advance()
                                if self.current_char == "u":
                                    ident_str += self.current_char
                                    ident_count += 1
                                    self.advance
                                    if self.current_char == "t":
                                        ident_str += self.current_char
                                        ident_count += 1
                                        tokens.append(Token(TT_KEYWORD))
                                        self.advance()
                    if self.current_char == "n":
                        ident_str += self.current_char
                        ident_count += 1
                        self.advance
                        if self.current_char == "g":
                            ident_str += self.current_char
                            ident_count += 1
                            tokens.append(Token(TT_KEYWORD))
                            self.advance()

                # Letter H
                if self.current_char == "h":
                    ident_str += self.current_char
                    ident_count += 1
                    self.advance()
                    if self.current_char == "a":
                        ident_str += self.current_char
                        ident_count += 1
                        self.advance()
                        if self.current_char == "w":
                            ident_str += self.current_char
                            ident_count += 1
                            self.advance()
                            if self.current_char == "k":
                                ident_str += self.current_char
                                ident_count += 1
                                tokens.append(Token(TT_KEYWORD))
                                self.advance()
                            if self.current_char == " ":
                                ident_str += self.current_char
                                ident_count += 1
                                self.advance()
                                if self.current_char == "t":
                                    ident_str += self.current_char
                                    ident_count += 1
                                    self.advance()
                                    if self.current_char == "u":
                                        ident_str += self.current_char
                                        ident_count += 1
                                        self.advance()
                                        if self.current_char == "a":
                                            ident_str += self.current_char
                                            ident_count += 1
                                            self.advance()
                                            if self.current_char == "h":
                                                ident_str += self.current_char
                                                ident_count += 1
                                                self.advance()
                                                tokens.append(Token(TT_KEYWORD))    
                # Letter I
                if self.current_char == "i":
                    ident_str += self.current_char
                    ident_count += 1
                    self.advance()
                    if self.current_char == "n":
                        ident_str += self.current_char
                        ident_count += 1
                        self.advance()
                        if self.current_char == "s":
                            ident_str += self.current_char
                            ident_count += 1
                            self.advance()
                            if self.current_char == "e":
                                ident_str += self.current_char
                                ident_count += 1
                                self.advance()
                                if self.current_char == "r":
                                    ident_str += self.current_char
                                    ident_count += 1
                                    self.advance()
                                    if self.current_char == "t":
                                        ident_str += self.current_char
                                        ident_count += 1
                                        tokens.append(Token(TT_KEYWORD))
                                        self.advance()
                # Letter J
                if self.current_char == "j":
                    ident_str += self.current_char
                    ident_count += 1
                    self.advance()
                    if self.current_char == "i":
                        ident_str += self.current_char
                        ident_count += 1
                        self.advance()
                        if self.current_char == "t":
                            ident_str += self.current_char
                            ident_count += 1
                            tokens.append(Token(TT_KEYWORD))
                            self.advance()

                # Letter L
                if self.current_char == "l":
                    ident_str += self.current_char
                    ident_count += 1
                    self.advance()
                    if self.current_char == "e":
                        ident_str += self.current_char
                        ident_count += 1
                        self.advance()
                        if self.current_char == "t":
                            ident_str += self.current_char
                            ident_count += 1
                            self.advance()
                            if self.current_char == "h":
                                ident_str += self.current_char
                                ident_count += 1
                                self.advance()
                                if self.current_char == "i":
                                    ident_str += self.current_char
                                    ident_count += 1
                                    self.advance()
                                    if self.current_char == "m":
                                        ident_str += self.current_char
                                        ident_count += 1
                                        self.advance()
                                        if self.current_char == "c":
                                            ident_str += self.current_char
                                            ident_count += 1
                                            self.advance()
                                            if self.current_char == "o":
                                                ident_str += self.current_char
                                                ident_count += 1
                                                self.advance()
                                                if self.current_char == "o":
                                                    ident_str += self.current_char
                                                    ident_count += 1
                                                    self.advance()
                                                    if self.current_char == "k":
                                                        ident_str += self.current_char
                                                        ident_count += 1
                                                        tokens.append(Token(TT_KEYWORD))
                                                        self.advance()
                    if self.current_char == "w":
                        ident_str += self.current_char
                        ident_count += 1
                        self.advance()
                        if self.current_char == "k":
                            ident_str += self.current_char
                            ident_count += 1
                            tokens.append(Token(TT_KEYWORD))
                            self.advance()

                # Letter N
                if self.current_char == "n":
                    ident_str += self.current_char
                    ident_count += 1
                    self.advance()
                    if self.current_char == "o":
                        ident_str += self.current_char
                        ident_count += 1
                        self.advance()
                        if self.current_char == "c":
                            ident_str += self.current_char
                            ident_count += 1
                            self.advance()
                            if self.current_char == "a":
                                ident_str += self.current_char
                                ident_count += 1
                                self.advance()
                                if self.current_char == "p":
                                    ident_str += self.current_char
                                    ident_count += 1
                                    tokens.append(Token(TT_KEYWORD))
                                    self.advance()
                    if self.current_char == "p":
                        ident_str += self.current_char
                        ident_count += 1
                        self.advance()
                        if self.current_char == "c":
                            ident_str += self.current_char
                            ident_count += 1
                            tokens.append(Token(TT_KEYWORD))
                            self.advance()
                        
                # Letter P
                if self.current_char == "p":
                    ident_str += self.current_char
                    ident_count += 1
                    self.advance()
                    if self.current_char == "a":
                        ident_str += self.current_char
                        ident_count += 1
                        self.advance()
                        if self.current_char == "u":
                            ident_str += self.current_char
                            ident_count += 1
                            self.advance()
                            if self.current_char == "s":
                                ident_str += self.current_char
                                ident_count += 1
                                self.advance()
                                if self.current_char == "e":
                                    ident_str += self.current_char
                                    ident_count += 1
                                    tokens.append(Token(TT_KEYWORD))
                                    self.advance()
                    if self.current_char == "l":
                            ident_str += self.current_char
                            ident_count += 1
                            self.advance()
                            if self.current_char == "u":
                                ident_str += self.current_char
                                ident_count += 1
                                self.advance()
                                if self.current_char == "g":
                                    ident_str += self.current_char
                                    ident_count += 1
                                    tokens.append(Token(TT_KEYWORD))
                                    self.advance()

                # Letter R
                if self.current_char == "r":
                    ident_str += self.current_char
                    ident_count += 1
                    self.advance()
                    if self.current_char == "e":
                        ident_str += self.current_char
                        ident_count += 1
                        self.advance()
                        if self.current_char == "m":
                            ident_str += self.current_char
                            ident_count += 1
                            self.advance()
                            if self.current_char == "o":
                                ident_str += self.current_char
                                ident_count += 1
                                self.advance()
                                if self.current_char == "v":
                                    ident_str += self.current_char
                                    ident_count += 1
                                    self.advance()
                                    if self.current_char == "e":
                                        ident_str += self.current_char
                                        ident_count += 1
                                        tokens.append(Token(TT_KEYWORD))
                                        self.advance()
                # Letter S
                if self.current_char == "s":
                    ident_str += self.current_char
                    ident_count += 1
                    self.advance()
                    if self.current_char == "k":
                        ident_str += self.current_char
                        ident_count += 1
                        self.advance()
                        if self.current_char == "i":
                            ident_str += self.current_char
                            ident_count += 1
                            self.advance()
                            if self.current_char == "b":
                                ident_str += self.current_char
                                ident_count += 1
                                self.advance()
                                if self.current_char == "i":
                                    ident_str += self.current_char
                                    ident_count += 1
                                    self.advance()
                                    if self.current_char == "d":
                                        ident_str += self.current_char
                                        ident_count += 1
                                        self.advance()
                                        if self.current_char == "i":
                                            ident_str += self.current_char
                                            ident_count += 1
                                            tokens.append(Token(TT_KEYWORD))
                                            self.advance()
                    if self.current_char == "t":
                        ident_str += self.current_char
                        ident_count += 1
                        self.advance()
                        if self.current_char == "u":
                            ident_str += self.current_char
                            ident_count += 1
                            self.advance()
                            if self.current_char == "r":
                                ident_str += self.current_char
                                ident_count += 1
                                self.advance()
                                if self.current_char == "d":
                                    ident_str += self.current_char
                                    ident_count += 1
                                    self.advance()
                                    if self.current_char == "y":
                                        ident_str += self.current_char
                                        ident_count += 1
                                        tokens.append(Token(TT_KEYWORD))
                                        self.advance()

                # Letter T
                if self.current_char == "t":
                    ident_str += self.current_char
                    ident_count += 1
                    self.advance()
                    if self.current_char == "r":
                        ident_str += self.current_char
                        ident_count += 1
                        self.advance()
                        if self.current_char == "u":
                            ident_str += self.current_char
                            ident_count += 1
                            self.advance()
                            if self.current_char == "e":
                                ident_str += self.current_char
                                ident_count += 1
                                tokens.append(Token(TT_KEYWORD))
                                self.advance()
                    if self.current_char == "u":
                        ident_str += self.current_char
                        ident_count += 1
                        self.advance()
                        if self.current_char == "a":
                            ident_str += self.current_char
                            ident_count += 1
                            self.advance()
                            if self.current_char == "h":
                                ident_str += self.current_char
                                ident_count += 1
                                tokens.append(Token(TT_KEYWORD))
                                self.advance()
                # Letter Y
                if self.current_char == "y":
                    ident_str += self.current_char
                    ident_count += 1
                    self.advance()
                    if self.current_char == "a":
                        ident_str += self.current_char
                        ident_count += 1
                        self.advance()
                        if self.current_char == "p":
                            ident_str += self.current_char
                            ident_count += 1
                            tokens.append(Token(TT_KEYWORD))
                            self.advance()

            elif self.current_char in NUM:
                tokens.append(self.make_number())

            elif self.current_char == '+':
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char == '+':
                    self.advance()
                    tokens.append(Token(TT_INC))  # Token for '++'
                else:
                    tokens.append(Token(TT_PLUS))  # Token for '+'
            elif self.current_char == '!':
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    tokens.append(Token(TT_NEQ))  # Token for '!='
                else:
                    tokens.append(Token(TT_NOT))  # Token for '!'
            elif self.current_char == '%':
                tokens.append(Token(TT_MOD))
                self.advance()
            elif self.current_char == '&':
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char == '&':
                    self.advance()
                    tokens.append(Token(TT_AND))  # Token for '&&'
                else:
                    [], IllegalCharError(pos_start, self.pos, "'&'") #ERROR FOR '&'
            elif self.current_char == '(': 
                tokens.append(Token(TT_OPPAR))  # Token for '('
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(TT_CLPAR))  # Token for ')'
                self.advance()
            elif self.current_char == '-':
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char == '--':
                    self.advance()
                    tokens.append(Token(TT_DEC))  # Token for '--'
                else:
                    tokens.append(Token(TT_MINUS))  # Token for '-'
            elif self.current_char == '*':
                tokens.append(Token(TT_MUL))  # Token for '*'
                self.advance()
            elif self.current_char == ',':
                tokens.append(Token(TT_COMMA))  # Token for ','
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token(TT_DIV))  # Token for '/'
                self.advance()
            elif self.current_char == '\\':
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char == '"':
                    self.advance()
                    tokens.append(Token(TT_ESCAPESEQUENCE))  # Token for '\"'
                elif self.current_char == '*':
                    self.advance()
                    tokens.append(Token(TT_ESCAPESEQUENCE))  # Token for '\*'
                elif self.current_char == '{':
                    self.advance()
                    tokens.append(Token(TT_ESCAPESEQUENCE))  # Token for '\{'
                elif self.current_char == '}':
                    self.advance()
                    tokens.append(Token(TT_ESCAPESEQUENCE))  # Token for '\}'
                elif self.current_char == 'n':
                    self.advance()
                    tokens.append(Token(TT_ESCAPESEQUENCE))  # Token for '\n'
                elif self.current_char == 't':
                    self.advance()
                    tokens.append(Token(TT_ESCAPESEQUENCE))  # Token for '\t'
                else:
                    return [], IllegalCharError(pos_start, self.pos, "'\\'")  # ERROR FOR '\'
            elif self.current_char == ';':
                tokens.append(Token(TT_SEMICOL))  # Token for ';'
                self.advance()
            elif self.current_char == '[':
                tokens.append(Token(TT_LSQUARE))  # Token for '['
                self.advance()
            elif self.current_char == ']':
                tokens.append(Token(TT_RSQUARE))  # Token for ']'
                self.advance()
            elif self.current_char == '{':
                tokens.append(Token(TT_LBRACE))  # Token for '{'
                self.advance()
            elif self.current_char == '}':
                tokens.append(Token(TT_RBRACE))  # Token for '}'
                self.advance()
            elif self.current_char == '|':
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char == '|':
                    self.advance()
                    tokens.append(Token(TT_OR))  # Token for '||'
                else:
                    return [], IllegalCharError(pos_start, self.pos, "'|'")  # ERROR FOR '|'
            elif self.current_char == '<':
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    tokens.append(Token(TT_LTE))  # Token for '<='
                else:
                    tokens.append(Token(TT_LT))  # Token for '<'
            elif self.current_char == '>':
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    tokens.append(Token(TT_GTE))  # Token for '>='
                else:
                    tokens.append(Token(TT_GT))  # Token for '>'
            elif self.current_char == '=':
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    tokens.append(Token(TT_EQ))  # Token for '=='
                else:
                    tokens.append(Token(TT_IS))  # Token for '='

            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return[], IllegalCharError(pos_start, self.pos, "'" + char + "'")
    
        return tokens, None


    def make_number(self):
        num_str = ''
        dot_count = 0

        while self.current_char != None and self.current_char in NUM + '.':
            if self.current_char == '.':
                if dot_count == 1: break
                dot_count +=1
                num_str += '.'
            else:
                num_str += self.current_char
            self.advance()

        if dot_count == 0:
            return Token(TT_CHUNGUS, int(num_str))
        else:
            return Token(TT_CHUDELUXE, float(num_str))
        
def run(fn, text):
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()

    return tokens, error