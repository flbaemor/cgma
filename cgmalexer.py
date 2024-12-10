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

clbra_dlm = ' =\n)'
clcur_dlm = ' \n)}'
clpar_dlm = ' \n}{)&|}' + ARITH_OPER
com_dlm =   ' ('
comma_dlm = ' _' + ALPHANUM
comnt_dlm = ' \n' + ASCII
endln_dlm = ' \n'
esc_dlm =   ' "'+ ASCII
equal_dlm = ' _[(-"+' + ALPHANUM
hawk_dlm =  ' \n{'
identif_dlm = ' \n)(&|;[],' + OPER
lit_dlm =   ' ,):\n;' + OPER
lwk_dlm =   ' \n&|=)' 
minus_dlm = ' -()' + ALPHANUM
npc_dlm =   ' :' + ALPHANUM
not_dlm =   ' =(' + ALPHANUM
opbra_dlm = ' "]' + ALPHANUM
opcur_dlm = ' \n' + ALPHANUM
operator_dlm = ' _(' + ALPHANUM
oppar_dlm = ' _)("-' + ALPHANUM
plus_dlm =  ' _("+)' + ALPHANUM
relat_dlm = ' _("' + ALPHANUM
scolon_dlm = ' _+-' + ALPHANUM
spc_dlm =   ' '
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
    def as_string(self):
        return f"Ln {self.pos_start.ln + 1} Col {self.pos_start.col + 1} ERROR: Invalid delimiter after {self.details}"


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

TT_OPPAR        = 'OPPAR'   # '('
TT_CLPAR        = 'CLPAR'   # ')'
TT_OPBRA        = 'OPBRA'   # '['
TT_CLBRA        = 'CLBRA'   # ']'
TT_OPCUR        = 'OPCUR'   # '{'
TT_CLCUR        = 'CLCUR'   # '}'
TT_SEMICOL      = 'SEMICOL' # ';'
TT_COL          = 'COLON'   # ':'
TT_COMMA        = 'COMMA'   # ','

TT_NL           = 'NL'      # New Line
TT_EOF          = 'EOF'     # End of File

TT_KEYWORD      = 'KEYWORD' # Keywords
TT_IDENTIFIER   = 'IDENTIFIER' # Identifiers

TT_ESCAPESEQUENCE = 'ESCAPESEQUENCE' # Escape Sequence
TT_COMMENT      = 'COMMENT' # Comments

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
            if self.current_char in ALPHA:
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
                                        self.advance()
                                        if self.current_char in com_dlm:
                                            tokens.append(Token(TT_KEYWORD, ident_str))
                                            continue
                                        else:
                                            tokens.append(Token(TT_KEYWORD, ident_str))
                                            return tokens, IllegalCharError(pos_start, self.pos, f"'{ident_str}'")

                                            
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
                                self.advance()
                                if self.current_char in spc_dlm:
                                    tokens.append(Token(TT_KEYWORD, ident_str))
                                    continue
                                else:
                                    tokens.append(Token(TT_KEYWORD, ident_str))
                                    return tokens, IllegalCharError(pos_start, self.pos, f"'{ident_str}'")
                #Letter B
                if self.current_char == "b":
                    ident_str += self.current_char
                    ident_count += 1
                    self.advance()
                    if self.current_char == "a":
                        ident_str += self.current_char
                        ident_count += 1
                        self.advance()
                        if self.current_char == "c":
                            ident_str += self.current_char
                            ident_count += 1
                            self.advance()
                            if self.current_char == "k":
                                ident_str += self.current_char
                                ident_count+=1
                                self.advance()
                                if self.current_char in spc_dlm:
                                    tokens.append(Token(TT_KEYWORD, ident_str))
                                    continue
                                else:
                                    tokens.append(Token(TT_KEYWORD, ident_str))
                                    return tokens, IllegalCharError(pos_start, self.pos, f"'{ident_str}'")

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
                                        ident_count+=1
                                        self.advance()
                                        if self.current_char in spc_dlm:
                                            tokens.append(Token(TT_KEYWORD, ident_str))
                                            continue
                                        else:
                                            tokens.append(Token(TT_KEYWORD, ident_str))
                                            return tokens, IllegalCharError(pos_start, self.pos, f"'{ident_str}'")
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
                                ident_count+=1
                                self.advance()
                                if self.current_char in com_dlm:
                                    tokens.append(Token(TT_KEYWORD, ident_str))
                                    continue
                                else:
                                    tokens.append(Token(TT_KEYWORD, ident_str))
                                    return tokens, IllegalCharError(pos_start, self.pos, f"'{ident_str}'")
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
                                            self.advance()
                                            if self.current_char in spc_dlm:
                                                tokens.append(Token(TT_KEYWORD, ident_str))
                                                continue
                                            else:
                                                tokens.append(Token(TT_KEYWORD, ident_str))
                                                return tokens, IllegalCharError(pos_start, self.pos, f"'{ident_str}'")
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
                                                self.advance()
                                                if self.current_char in spc_dlm:
                                                    tokens.append(Token(TT_KEYWORD, ident_str))
                                                    continue
                                                else:
                                                    tokens.append(Token(TT_KEYWORD, ident_str))
                                                    return tokens, IllegalCharError(pos_start, self.pos, f"'{ident_str}'")      

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
                                    ident_count+=1
                                    self.advance()
                                    if self.current_char in lwk_dlm:
                                        tokens.append(Token(TT_KEYWORD, ident_str))
                                        continue
                                    else:
                                        tokens.append(Token(TT_KEYWORD, ident_str))
                                        return tokens, IllegalCharError(pos_start, self.pos, f"'{ident_str}'")
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
                                        ident_count+=1
                                        self.advance()
                                        if self.current_char in spc_dlm:
                                            tokens.append(Token(TT_KEYWORD, ident_str))
                                            continue
                                        else:
                                            tokens.append(Token(TT_KEYWORD, ident_str))
                                            return tokens, IllegalCharError(pos_start, self.pos, f"'{ident_str}'")
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
                                        ident_count+=1
                                        self.advance()
                                        if self.current_char in endln_dlm:
                                            tokens.append(Token(TT_KEYWORD, ident_str))
                                            continue
                                        else:
                                            tokens.append(Token(TT_KEYWORD, ident_str))
                                            return tokens, IllegalCharError(pos_start, self.pos, f"'{ident_str}'")
                    if self.current_char == "n":
                        ident_str += self.current_char
                        ident_count += 1
                        self.advance
                        if self.current_char == "g":
                            ident_str += self.current_char
                            ident_count+=1
                            self.advance()
                            if self.current_char in spc_dlm:
                                tokens.append(Token(TT_KEYWORD, ident_str))
                                continue
                            else:
                                return [], IllegalCharError(pos_start, self.pos, f"'{ident_str}'")   

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
                                ident_count+=1
                                self.advance()
                                if self.current_char in hawk_dlm:
                                    tokens.append(Token(TT_KEYWORD, ident_str))
                                    continue
                                else:
                                    tokens.append(Token(TT_KEYWORD, ident_str))
                                    return tokens, IllegalCharError(pos_start, self.pos, f"'{ident_str}'")
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
                                                ident_count+=1
                                                self.advance()
                                                if self.current_char in com_dlm:
                                                    tokens.append(Token(TT_KEYWORD, ident_str))
                                                    continue
                                                else:
                                                    tokens.append(Token(TT_KEYWORD, ident_str))
                                                    return tokens, IllegalCharError(pos_start, self.pos, f"'{ident_str}'")
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
                                        ident_count+=1
                                        self.advance()
                                        if self.current_char in com_dlm:
                                            tokens.append(Token(TT_KEYWORD, ident_str))
                                            continue
                                        else:
                                            tokens.append(Token(TT_KEYWORD, ident_str))
                                            return tokens, IllegalCharError(pos_start, self.pos, f"'{ident_str}'")
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
                            ident_count+=1
                            self.advance()
                            if self.current_char in com_dlm:
                                tokens.append(Token(TT_KEYWORD, ident_str))
                                continue
                            else:
                                tokens.append(Token(TT_KEYWORD, ident_str))
                                return tokens, IllegalCharError(pos_start, self.pos, f"'{ident_str}'")

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
                                                        ident_count+=1
                                                        self.advance()
                                                        if self.current_char in com_dlm:
                                                            tokens.append(Token(TT_KEYWORD, ident_str))
                                                            continue
                                                        else:
                                                            tokens.append(Token(TT_KEYWORD, ident_str))
                                                            return tokens, IllegalCharError(pos_start, self.pos, f"'{ident_str}'")
                    if self.current_char == "w":
                        ident_str += self.current_char
                        ident_count += 1
                        self.advance()
                        if self.current_char == "k":
                            ident_str += self.current_char
                            ident_count+=1
                            self.advance()
                            if self.current_char in spc_dlm:
                                tokens.append(Token(TT_KEYWORD, ident_str))
                                continue
                            else:
                                tokens.append(Token(TT_KEYWORD, ident_str))
                                return tokens, IllegalCharError(pos_start, self.pos, f"'{ident_str}'")

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
                                    ident_count+=1
                                    self.advance()
                                    if self.current_char in spc_dlm:
                                        tokens.append(Token(TT_KEYWORD, ident_str))
                                        continue
                                    else:
                                        tokens.append(Token(TT_KEYWORD, ident_str))
                                        return tokens, IllegalCharError(pos_start, self.pos, f"'{ident_str}'")
                    if self.current_char == "p":
                        ident_str += self.current_char
                        ident_count += 1
                        self.advance()
                        if self.current_char == "c":
                            ident_str += self.current_char
                            ident_count+=1
                            self.advance()
                            if self.current_char in npc_dlm:
                                tokens.append(Token(TT_KEYWORD, ident_str))
                                continue
                            else:
                                tokens.append(Token(TT_KEYWORD, ident_str))
                                return tokens, IllegalCharError(pos_start, self.pos, f"'{ident_str}'")
                        
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
                                    ident_count+=1
                                    self.advance()
                                    if self.current_char in endln_dlm:
                                        tokens.append(Token(TT_KEYWORD, ident_str))
                                        continue
                                    else:
                                        tokens.append(Token(TT_KEYWORD, ident_str))
                                        return tokens, IllegalCharError(pos_start, self.pos, f"'{ident_str}'")
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
                                    ident_count+=1
                                    self.advance()
                                    if self.current_char in com_dlm:
                                        tokens.append(Token(TT_KEYWORD, ident_str))
                                        continue
                                    else:
                                        tokens.append(Token(TT_KEYWORD, ident_str))
                                        return tokens, IllegalCharError(pos_start, self.pos, f"'{ident_str}'")

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
                                        ident_count+=1
                                        self.advance()
                                        if self.current_char in com_dlm:
                                            tokens.append(Token(TT_KEYWORD, ident_str))
                                            continue
                                        else:
                                            tokens.append(Token(TT_KEYWORD, ident_str))
                                            return tokens, IllegalCharError(pos_start, self.pos, f"'{ident_str}'")
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
                                            ident_count+=1
                                            self.advance()
                                            if self.current_char in com_dlm:
                                                tokens.append(Token(TT_KEYWORD, ident_str))
                                                continue
                                            else:
                                                tokens.append(Token(TT_KEYWORD, ident_str))
                                                return tokens, IllegalCharError(pos_start, self.pos, f"'{ident_str}'")
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
                                        ident_count+=1
                                        self.advance()
                                        if self.current_char in spc_dlm:
                                            tokens.append(Token(TT_KEYWORD, ident_str))
                                            continue
                                        else:
                                            tokens.append(Token(TT_KEYWORD, ident_str))
                                            return tokens, IllegalCharError(pos_start, self.pos, f"'{ident_str}'")

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
                                ident_count+=1
                                self.advance()
                                if self.current_char in lwk_dlm:
                                    tokens.append(Token(TT_KEYWORD, ident_str))
                                    continue
                                else:
                                    tokens.append(Token(TT_KEYWORD, ident_str))
                                    return tokens, IllegalCharError(pos_start, self.pos, f"'{ident_str}'")
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
                                ident_count+=1
                                self.advance()
                                if self.current_char in com_dlm:
                                    tokens.append(Token(TT_KEYWORD, ident_str))
                                    continue
                                else:
                                    tokens.append(Token(TT_KEYWORD, ident_str))
                                    return tokens, IllegalCharError(pos_start, self.pos, f"'{ident_str}'")
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
                            ident_count+=1
                            self.advance()
                            if self.current_char in com_dlm:
                                tokens.append(Token(TT_KEYWORD, ident_str))
                                continue
                            else:
                                tokens.append(Token(TT_KEYWORD, ident_str))
                                return tokens, IllegalCharError(pos_start, self.pos, f"'{ident_str}'")
                            
                while self.current_char is not None and (self.current_char in ALPHANUM or self.current_char == '_'):
                    ident_str += self.current_char
                    self.advance()
                
                if self.current_char in identif_dlm:
                    tokens.append(Token(TT_IDENTIFIER, ident_str))
                    
                else:
                    tokens.append(Token(TT_IDENTIFIER, ident_str))
                    return [], IllegalCharError(pos_start, self.pos, f"'{ident_str}'")


            elif self.current_char == "+":
                ident_str = self.current_char
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char == "+":
                    ident_str += self.current_char
                    self.advance()
                    if self.current_char in unary_dlm:
                        tokens.append(Token(TT_INC, ident_str))
                        continue
                    else:
                        tokens.append(Token(TT_INC, ident_str))
                        return tokens, IllegalCharError(pos_start, self.pos, f"'{ident_str}'")
                elif self.current_char in plus_dlm:
                    tokens.append(Token(TT_PLUS, ident_str))
                    continue
                else:
                    tokens.append(Token(TT_PLUS, ident_str))
                    return tokens, IllegalCharError(pos_start, self.pos, f"'{ident_str}'")
                
            elif self.current_char == "!":
                ident_str = self.current_char
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char == "=":
                    ident_str += self.current_char
                    self.advance()
                    if self.current_char in relat_dlm:
                        tokens.append(Token(TT_INC, ident_str))
                        continue
                    else:
                        tokens.append(Token(TT_INC, ident_str))
                        return tokens, IllegalCharError(pos_start, self.pos, f"'{ident_str}'")
                elif self.current_char in not_dlm:
                    tokens.append(Token(TT_PLUS, ident_str))
                    continue
                else:
                    tokens.append(Token(TT_PLUS, ident_str))
                    return tokens, IllegalCharError(pos_start, self.pos, f"'{ident_str}'")

                
            elif self.current_char == "%":
                ident_str = self.current_char
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char in operator_dlm:
                    tokens.append(Token(TT_MOD, ident_str))
                    continue
                else:
                    tokens.append(Token(TT_MOD, ident_str))
                    return tokens, IllegalCharError(pos_start, self.pos, f"'{ident_str}'")
    
            elif self.current_char == "&":
                ident_str = self.current_char
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char == "&":
                    ident_str += self.current_char
                    self.advance()
                    if self.current_char in operator_dlm:
                        tokens.append(Token(TT_AND, ident_str))
                        continue
                    else:
                        tokens.append(Token(TT_AND, ident_str))
                        return tokens, IllegalCharError(pos_start, self.pos, f"'{ident_str}'")
                    
            elif self.current_char == "(":
                ident_str = self.current_char
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char in oppar_dlm:
                    tokens.append(Token(TT_OPPAR, ident_str))
                    continue
                else:
                    tokens.append(Token(TT_OPPAR, ident_str))
                    return tokens, IllegalCharError(pos_start, self.pos, f"'{ident_str}'")
                
            elif self.current_char == ")":
                ident_str = self.current_char
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char in clpar_dlm:
                    tokens.append(Token(TT_CLPAR, ident_str))
                    continue
                else:
                    tokens.append(Token(TT_CLPAR, ident_str))
                    return tokens, IllegalCharError(pos_start, self.pos, f"'{ident_str}'")
                

            elif self.current_char == "-":
                ident_str = self.current_char
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char == "-":
                    ident_str += self.current_char
                    self.advance()
                    if self.current_char in unary_dlm:
                        tokens.append(Token(TT_DEC, ident_str))
                        continue
                    else:
                        tokens.append(Token(TT_DEC, ident_str))
                        return tokens, IllegalCharError(pos_start, self.pos, f"'{ident_str}'")
                elif self.current_char in minus_dlm:
                    tokens.append(Token(TT_MINUS, ident_str))
                    continue
                else:
                    tokens.append(Token(TT_MINUS, ident_str))
                    return tokens, IllegalCharError(pos_start, self.pos, f"'{ident_str}'")

            elif self.current_char == "*":
                ident_str = self.current_char
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char in operator_dlm:
                    tokens.append(Token(TT_MUL, ident_str))
                    continue
                else:
                    tokens.append(Token(TT_MUL, ident_str))
                    return tokens, IllegalCharError(pos_start, self.pos, f"'{ident_str}'")
                
            elif self.current_char == ",":
                ident_str = self.current_char
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char in comma_dlm:
                    tokens.append(Token(TT_COMMA, ident_str))
                    continue
                else:
                    tokens.append(Token(TT_COMMA, ident_str))
                    return tokens, IllegalCharError(pos_start, self.pos, f"'{ident_str}'")
            
            elif self.current_char == "\\":
                ident_str = self.current_char
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char == "\"":
                    ident_str += self.current_char
                    self.advance()
                    if self.current_char in esc_dlm:
                        tokens.append(Token(TT_ESCAPESEQUENCE, ident_str))
                        continue
                    else:
                        tokens.append(Token(TT_ESCAPESEQUENCE, ident_str))
                        return tokens, IllegalCharError(pos_start, self.pos, f"'{ident_str}'")
                elif self.current_char == "*":
                    ident_str += self.current_char
                    self.advance()
                    if self.current_char in esc_dlm:
                        tokens.append(Token(TT_ESCAPESEQUENCE, ident_str))
                        continue
                    else:
                        tokens.append(Token(TT_ESCAPESEQUENCE, ident_str))
                        return tokens, IllegalCharError(pos_start, self.pos, f"'{ident_str}'")
                elif self.current_char == "{":
                    ident_str += self.current_char
                    self.advance()
                    if self.current_char in esc_dlm:
                        tokens.append(Token(TT_ESCAPESEQUENCE, ident_str))
                        continue
                    else:
                        tokens.append(Token(TT_ESCAPESEQUENCE, ident_str))
                        return tokens, IllegalCharError(pos_start, self.pos, f"'{ident_str}'")
                elif self.current_char == "}":
                    ident_str += self.current_char
                    self.advance()
                    if self.current_char in esc_dlm:
                        tokens.append(Token(TT_ESCAPESEQUENCE, ident_str))
                        continue
                    else:
                        tokens.append(Token(TT_ESCAPESEQUENCE, ident_str))
                        return tokens, IllegalCharError(pos_start, self.pos, f"'{ident_str}'")
                elif self.current_char == "n":
                    ident_str += self.current_char
                    self.advance()
                    if self.current_char in esc_dlm:
                        tokens.append(Token(TT_ESCAPESEQUENCE, ident_str))
                        continue
                    else:
                        tokens.append(Token(TT_ESCAPESEQUENCE, ident_str))
                        return tokens, IllegalCharError(pos_start, self.pos, f"'{ident_str}'")
                elif self.current_char == "t":
                    ident_str += self.current_char
                    self.advance()
                    if self.current_char in esc_dlm:
                        tokens.append(Token(TT_ESCAPESEQUENCE, ident_str))
                        continue
                    else:
                        tokens.append(Token(TT_ESCAPESEQUENCE, ident_str))
                        return tokens, IllegalCharError(pos_start, self.pos, f"'{ident_str}'")
                else:
                    tokens.append(Token(TT_ESCAPESEQUENCE, ident_str))
                    return tokens, IllegalCharError(pos_start, self.pos, f"'{self.current_char}'")
                
            elif self.current_char == ";":
                ident_str = self.current_char
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char in scolon_dlm:
                    tokens.append(Token(TT_SEMICOL, ident_str))
                    continue
                else:
                    tokens.append(Token(TT_SEMICOL, ident_str))
                    return tokens, IllegalCharError(pos_start, self.pos, f"'{ident_str}'")
                
            elif self.current_char == "[":
                ident_str = self.current_char
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char in opbra_dlm:
                    tokens.append(Token(TT_OPBRA, ident_str))
                    continue
                else:
                    tokens.append(Token(TT_OPBRA, ident_str))
                    return tokens, IllegalCharError(pos_start, self.pos, f"'{ident_str}'")
                
            elif self.current_char == "]":
                ident_str = self.current_char
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char in clbra_dlm:
                    tokens.append(Token(TT_CLBRA, ident_str))
                    continue
                else:
                    tokens.append(Token(TT_CLBRA, ident_str))
                    return tokens, IllegalCharError(pos_start, self.pos, f"'{ident_str}'")
                
            elif self.current_char == "{":
                ident_str = self.current_char
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char in opcur_dlm:
                    tokens.append(Token(TT_OPCUR, ident_str))
                    continue
                else:
                    tokens.append(Token(TT_OPCUR, ident_str))
                    return tokens, IllegalCharError(pos_start, self.pos, f"'{ident_str}'")
                
            elif self.current_char == "}":
                ident_str = self.current_char 
                pos_start = self.pos.copy() 
                self.advance()
                if self.current_char is None or self.current_char in clcur_dlm:
                    tokens.append(Token(TT_CLCUR, ident_str))
                    continue
                else: 
                    tokens.append(Token(TT_CLCUR, ident_str))
                    return tokens, IllegalCharError(pos_start, self.pos, f"Invalid delimiter after '{ident_str}'")

            elif self.current_char == '|':
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char == '|' and (self.pos.idx + 1 < len(self.text) and self.text[self.pos.idx + 1] in operator_dlm):
                    self.advance()
                    tokens.append(Token(TT_OR))  # Token for '||'

            elif self.current_char == "<":
                ident_str = self.current_char
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char == "=":
                    ident_str += self.current_char
                    self.advance()
                    if self.current_char in operator_dlm:
                        tokens.append(Token(TT_LTE, ident_str))
                        continue
                    else:
                        tokens.append(Token(TT_LTE, ident_str))
                        return tokens, IllegalCharError(pos_start, self.pos, f"'{ident_str}'")
                elif self.current_char in operator_dlm:
                    tokens.append(Token(TT_LT, ident_str))
                    continue
                else:
                    tokens.append(Token(TT_LT, ident_str))
                    return tokens, IllegalCharError(pos_start, self.pos, f"'{self.current_char}'")

            elif self.current_char == ">":
                ident_str = self.current_char
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char == "=":
                    ident_str += self.current_char
                    self.advance()
                    if self.current_char in operator_dlm:
                        tokens.append(Token(TT_GTE, ident_str))
                        continue
                    else:
                        tokens.append(Token(TT_GTE, ident_str))
                        return tokens, IllegalCharError(pos_start, self.pos, f"'{ident_str}'")
                elif self.current_char in operator_dlm:
                    tokens.append(Token(TT_GT, ident_str))
                    continue
                else:
                    tokens.append(Token(TT_GT, ident_str))
                    return tokens, IllegalCharError(pos_start, self.pos, f"'{self.current_char}'")

            elif self.current_char == "=":
                ident_str = self.current_char
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char == "=":
                    ident_str += self.current_char
                    self.advance()
                    if self.current_char in relat_dlm:
                        tokens.append(Token(TT_EQ, ident_str))
                        continue
                    else:
                        tokens.append(Token(TT_EQ, ident_str))
                        return tokens, IllegalCharError(pos_start, self.pos, f"'{ident_str}'")
                elif self.current_char in equal_dlm:
                    tokens.append(Token(TT_IS, ident_str))
                    continue
                else:
                    tokens.append(Token(TT_IS, ident_str))
                    return tokens, IllegalCharError(pos_start, self.pos, f"'{self.current_char}'")
            
            elif self.current_char == ":":
                ident_str = self.current_char
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char in endln_dlm:
                    tokens.append(Token(TT_COL, ident_str))
                    continue
                else:
                    tokens.append(Token(TT_COL, ident_str))
                    return tokens, IllegalCharError(pos_start, self.pos, f"'{ident_str}'")
                
            elif self.current_char == '\n':
                self.advance()

            elif self.current_char == '\t':
                self.advance()

            elif self.current_char == ' ':
                self.advance()

            elif self.current_char in NUM:
                dot_count = 0
                ident_str = ""
                pos_start = self.pos.copy()

                while self.current_char is not None and self.current_char in NUM + ".":
                    if self.current_char == ".":
                        if dot_count == 1: 
                            break
                        dot_count += 1
                    ident_str += self.current_char
                    self.advance()

                if self.current_char is not None and self.current_char not in lit_dlm:
                    return tokens, IllegalCharError(pos_start, self.pos, f"'{ident_str}'")

                if dot_count == 0: 
                    if len(ident_str) > 10: 
                        return tokens, IllegalCharError(pos_start, self.pos, f"'{ident_str}' (integer too long)")
                    tokens.append(Token(TT_CHUNGUS, ident_str))
                else:  
                    parts = ident_str.split(".")
                    if len(parts[0]) > 10 or len(parts[1]) > 5:
                        return tokens, IllegalCharError(pos_start, self.pos, f"'{ident_str}' (invalid decimal length)")
                    tokens.append(Token(TT_CHUDELUXE, ident_str))

            elif self.current_char == '"':
                tokens.append(self.make_string())  # Token for Strings

            elif self.current_char == "/":
                ident_str = self.current_char
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char == "/":
                    ident_str += self.current_char
                    self.advance()
                    while self.current_char is not None and self.current_char not in endln_dlm:
                        ident_str += self.current_char
                        self.advance()
                    tokens.append(Token(TT_COMMENT, ident_str))
                    continue
                elif self.current_char == "*":
                    ident_str += self.current_char
                    self.advance()
                    while self.current_char is not None:
                        if self.current_char == "*" and self.pos.idx + 1 < len(self.text) and self.text[self.pos.idx + 1] == "/":
                            ident_str += "*/"
                            self.advance()
                            self.advance()
                            break
                        else:
                            ident_str += self.current_char
                            self.advance()
                    tokens.append(Token(TT_COMMENT, ident_str))
                    continue
                elif self.current_char in operator_dlm:
                    tokens.append(Token(TT_DIV, ident_str))
                    continue
                else:
                    tokens.append(Token(TT_DIV, ident_str))
                    return tokens, IllegalCharError(pos_start, self.pos, f"'{ident_str}'")
            
            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return[], IllegalCharError(pos_start, self.pos, "'" + char + "'")
                
    
        return tokens, None

    def make_number(self):
        num_str = ''
        pos_start = self.pos.copy()
        dot_count = 0
        whole_part_length = 0
        decimal_part_length = 0
        
        while self.current_char is not None and self.current_char in NUM + '.':
            if self.current_char == '.':
                if dot_count == 1: 
                    break
                dot_count += 1
                num_str += '.'
            else:
                if dot_count == 0:
                    whole_part_length += 1
                    if whole_part_length > 10:
                        break
                else:
                    decimal_part_length += 1
                    if decimal_part_length > 5:
                        break
                num_str += self.current_char
            self.advance()

        if self.current_char is not None and self.current_char not in lit_dlm:
            return [], IllegalCharError(pos_start, self.pos, f"'{self.current_char}'")

        if dot_count == 0:
            if num_str == '0':
                return Token(TT_CHUNGUS, '0')
            return Token(TT_CHUNGUS, int(num_str))
        else:
            return Token(TT_CHUNGUS, float(num_str))
        
    
    def make_string(self):
        string = ''
        pos_start = self.pos.copy()
        escape_character = False
        self.advance()

        escape_characters = {
            'n': '\n',
            't': '\t'
        }

        while self.current_char != None and (self.current_char != '"' or escape_character):
            if escape_character:
                string += escape_characters.get(self.current_char, self.current_char)
                escape_character = False
            else:
                if self.current_char == '\\':
                    escape_character = True
                else:
                    string += self.current_char
            self.advance()

        if self.current_char != '"':
            pos_end = self.pos.copy()
            return [], IllegalCharError(pos_start, pos_end, "Missing \" after string literal")

        self.advance()

        if self.pos.idx < len(self.text) and self.text[self.pos.idx] not in lit_dlm:
            pos_end = self.pos.copy()
            return [], IllegalCharError(pos_start, self.pos, f"'{self.current_char}'")

        return Token(TT_FORSEN, string)

    def make_newline(self): 
        self.advance()
        return Token(TT_NL)
    
def run(fn, text):
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()

    return tokens, error