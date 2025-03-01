import sys
import json
import re
#CONSTANTS

ALPHA_LOWER = 'abcdefghijklmnopqrstuvwxyz'
ALPHA_UPPER = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
ALPHA = ALPHA_LOWER + ALPHA_UPPER
ZERO = '0'
DIGITS = '123456789'
NUM = ZERO + DIGITS
ALPHANUM = ALPHA + NUM
PUNCTUATIONS = '!@#$%^&*()-_=+[]}{|:;’”,<>.?/ \\x'
ASCII = ALPHANUM + PUNCTUATIONS
NOT_OPER = '!'
ARITH_OPER = '+-/*%'
RELAT_OPER = '<>='
OPER = ARITH_OPER + RELAT_OPER

#DELIMITERS

clbra_dlm = ' =\n)\t'
clcur_dlm = ' \n)}\t'
clpar_dlm = ' \n}{)&|}\t.,(' + ARITH_OPER + ALPHANUM
com_dlm   =   '('
comma_dlm = ' _"\t' + ALPHANUM
convert_dlm = ' )\t,\n' + OPER
comnt_dlm = ' \n\t' + ASCII
endln_dlm = ' \n\t'
esc_dlm =   ' "\t'+ ASCII
equal_dlm = ' _[(-"+\t!' + ALPHANUM
hawk_dlm =  ' \n{\t'
identif_dlm = ' \n)(&|;[],.\t' + OPER
lit_dlm =   ' ,):\n;\t/+-%*' + OPER
lwk_dlm =   ' \n&|=)\t' 
minus_dlm = ' -()\t' + ALPHANUM
npc_dlm =   ' :\t' + ALPHANUM
not_dlm =   ' =(\t' + ALPHA
opbra_dlm = ' "]\t!\'' + ALPHANUM 
opcur_dlm = ' \n\t}' + ALPHANUM
operator_dlm = ' _(\t!' + ALPHANUM
oppar_dlm = ' _)("-\t!' + ALPHANUM
plus_dlm =  ' _("+)\t' + ALPHANUM
relat_dlm = ' _("\t!' + ALPHANUM
scolon_dlm = ' _+-\t' + ALPHANUM
spc_dlm =   ' \t'
unary_dlm = ' _)\t\n' + ALPHANUM

#TOKENS

TT_CHUNGUS      = 'CHU_LIT'     # Whole Numbers '3'
TT_CHUDELUXE    = 'CHUDEL_LIT'   # Decimal Numbers '3.14'
TT_FORSEN       = 'FORSEN_LIT'  # Strings 
TT_FORSENCD     = 'FORSENCD_LIT' #Char
TT_LWK          = 'LWK_LIT'     # Boolean 'true' or 'false'

TT_PLUS         = 'PLUS'    # '+'
TT_MINUS        = 'MINUS'   # '-'
TT_MUL          = 'MUL'     # '*'
TT_DIV          = 'DIV'     # '/'
TT_MOD          = 'MOD'     # '%'
TT_IS           = 'IS'      # '='
TT_NEGAT        = 'NEGAT'   # '-'

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
TT_DOT          = 'DOT'     # '.'
TT_DBLQT         = 'DBLQT'   # '"'

TT_SPC          = 'SPC'     # ' '
TT_NL           = 'NL'      # New Line
TT_TAB          = 'TAB'     # Tab
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
        self.details = self.details.replace('\n', '\\n')
        return f"Ln {self.pos_start.ln + 1} Lexical Error: {self.details}"

#TOKEN

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
        errors = []
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
                                        if self.current_char is not None and self.current_char in com_dlm:
                                            tokens.append(Token(TT_KEYWORD, ident_str))
                                            continue
                                        elif self.current_char is not None and self.current_char not in com_dlm and self.current_char not in ALPHANUM:
                                            errors.append(IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                                            self.advance()
                                            continue
                                            
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
                                if self.current_char is None or self.current_char in spc_dlm:
                                    tokens.append(Token(TT_KEYWORD, ident_str))
                                    continue
                                elif self.current_char is not None and self.current_char not in spc_dlm and self.current_char not in ALPHANUM:
                                    errors.append(IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                                    self.advance()
                                    continue
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
                                if self.current_char is None or self.current_char in spc_dlm:
                                    tokens.append(Token(TT_KEYWORD, ident_str))
                                    continue
                                elif self.current_char is not None and self.current_char not in spc_dlm and self.current_char not in ALPHANUM:
                                    errors.append(IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                                    self.advance()
                                    continue

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
                                        if self.current_char is None or self.current_char in spc_dlm:
                                            tokens.append(Token(TT_KEYWORD, ident_str))
                                            continue
                                        elif self.current_char is not None and self.current_char not in spc_dlm and self.current_char not in ALPHANUM:
                                            errors.append(IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                                            self.advance()
                                            continue
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
                                if self.current_char is not None and self.current_char in com_dlm:
                                    tokens.append(Token(TT_KEYWORD, ident_str))
                                    continue
                                elif self.current_char is not None and self.current_char not in com_dlm and self.current_char not in ALPHANUM:
                                    errors.append(IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                                    self.advance()
                                    continue
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
                                            if self.current_char is None or self.current_char in convert_dlm:
                                                tokens.append(Token(TT_KEYWORD, ident_str))
                                                continue
                                            elif self.current_char is not None and self.current_char not in convert_dlm and self.current_char not in ALPHANUM:
                                                errors.append(IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                                                self.advance()
                                                continue
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
                                                    if self.current_char is None or self.current_char in convert_dlm:
                                                        tokens.append(Token(TT_KEYWORD, ident_str))
                                                        continue
                                                    elif self.current_char is not None and self.current_char not in convert_dlm and self.current_char not in ALPHANUM:
                                                        errors.append(IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                                                        self.advance()
                                                        continue

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
                                    if self.current_char is None or self.current_char in lwk_dlm:
                                        tokens.append(Token(TT_KEYWORD, ident_str))
                                        continue
                                    elif self.current_char is not None and self.current_char not in lwk_dlm and self.current_char not in ALPHANUM:
                                        errors.append(IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                                        self.advance()
                                        continue
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
                                        if self.current_char == "c":
                                            ident_str += self.current_char
                                            ident_count += 1
                                            self.advance()
                                            if self.current_char == "d":
                                                ident_str += self.current_char
                                                ident_count += 1
                                                self.advance()
                                                if self.current_char is None or self.current_char in spc_dlm:
                                                    tokens.append(Token(TT_KEYWORD, ident_str))
                                                    continue
                                                elif self.current_char is not None and self.current_char not in spc_dlm and self.current_char not in ALPHANUM:
                                                    errors.append(IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                                                    self.advance()
                                                    continue
                                        if self.current_char is None or self.current_char in spc_dlm:
                                            tokens.append(Token(TT_KEYWORD, ident_str))
                                            continue
                                        elif self.current_char is not None and self.current_char not in spc_dlm and self.current_char not in ALPHANUM:
                                            errors.append(IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                                            self.advance()
                                            continue
                                            

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
                                    self.advance()
                                    if self.current_char == "t":
                                        ident_str += self.current_char
                                        ident_count+=1
                                        self.advance()
                                        if self.current_char is None or self.current_char in endln_dlm:
                                            tokens.append(Token(TT_KEYWORD, ident_str))
                                            continue
                                        elif self.current_char is not None and self.current_char not in endln_dlm and self.current_char not in ALPHANUM:
                                            errors.append(IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                                            self.advance()
                                            continue
                    if self.current_char == "n":
                        ident_str += self.current_char
                        ident_count += 1
                        self.advance
                        if self.current_char == "g":
                            ident_str += self.current_char
                            ident_count+=1
                            self.advance()
                            if self.current_char is None or self.current_char in spc_dlm:
                                tokens.append(Token(TT_KEYWORD, ident_str))
                                continue
                            elif self.current_char is not None and self.current_char not in spc_dlm and self.current_char not in ALPHANUM:
                                errors.append(IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                                self.advance()
                                continue

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
                                                if self.current_char is not None and self.current_char in com_dlm:
                                                    tokens.append(Token(TT_KEYWORD, ident_str))
                                                    continue
                                                elif self.current_char is not None and self.current_char not in com_dlm and self.current_char not in ALPHANUM:
                                                    errors.append(IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                                                    continue
                                elif self.current_char is not None and self.current_char in hawk_dlm:
                                    tokens.append(Token(TT_KEYWORD, ident_str))
                                    continue
                                elif self.current_char is not None and self.current_char not in hawk_dlm and self.current_char not in ALPHANUM:
                                    errors.append(IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                                    self.advance()
                                    continue

                                
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
                                        if self.current_char is not None and self.current_char in com_dlm:
                                            tokens.append(Token(TT_KEYWORD, ident_str))
                                            continue
                                        elif self.current_char is not None and self.current_char not in com_dlm and self.current_char not in ALPHANUM:
                                            errors.append(IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                                            self.advance()
                                            continue

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
                            if self.current_char is None or self.current_char in com_dlm:
                                tokens.append(Token(TT_KEYWORD, ident_str))
                                continue
                            elif self.current_char is not None and self.current_char not in com_dlm and self.current_char not in ALPHANUM:
                                errors.append(IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                                self.advance()
                                continue

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
                                                        if self.current_char is not None and self.current_char in com_dlm:
                                                            tokens.append(Token(TT_KEYWORD, ident_str))
                                                            continue
                                                        elif self.current_char is not None and self.current_char not in com_dlm and self.current_char not in ALPHANUM:
                                                            errors.append(IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                                                            self.advance()
                                                            continue

                    if self.current_char == "i":
                        ident_str += self.current_char
                        ident_count += 1
                        self.advance()
                        if self.current_char == "l":
                            ident_str += self.current_char
                            ident_count+=1
                            self.advance()
                            if self.current_char is None or self.current_char in hawk_dlm:
                                tokens.append(Token(TT_KEYWORD, ident_str))
                                continue
                            elif self.current_char is not None and self.current_char not in hawk_dlm and self.current_char not in ALPHANUM:
                                errors.append(IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                                self.advance()
                                continue
                        
                    if self.current_char == "w":
                        ident_str += self.current_char
                        ident_count += 1
                        self.advance()
                        if self.current_char == "k":
                            ident_str += self.current_char
                            ident_count+=1
                            self.advance()
                            if self.current_char is None or self.current_char in spc_dlm:
                                tokens.append(Token(TT_KEYWORD, ident_str))
                                continue
                            elif self.current_char is not None and self.current_char not in spc_dlm and self.current_char not in ALPHANUM:
                                errors.append(IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                                self.advance()
                                continue

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
                                    if self.current_char is None or self.current_char in spc_dlm:
                                        tokens.append(Token(TT_KEYWORD, ident_str))
                                        continue
                                    elif self.current_char is not None and self.current_char not in spc_dlm and self.current_char not in ALPHANUM:
                                        errors.append(IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                                        self.advance()
                                        continue

                    if self.current_char == "p":
                        ident_str += self.current_char
                        ident_count += 1
                        self.advance()
                        if self.current_char == "c":
                            ident_str += self.current_char
                            ident_count+=1
                            self.advance()
                            if self.current_char is None or self.current_char in npc_dlm:
                                tokens.append(Token(TT_KEYWORD, ident_str))
                                continue
                            elif self.current_char is not None and self.current_char not in npc_dlm and self.current_char not in ALPHANUM:
                                errors.append(IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                                self.advance()
                                continue
                        
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
                                    if self.current_char is None or self.current_char in endln_dlm:
                                        tokens.append(Token(TT_KEYWORD, ident_str))
                                        continue
                                    elif self.current_char is not None and self.current_char not in endln_dlm and self.current_char not in ALPHANUM:
                                        errors.append(IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                                        self.advance()
                                        continue

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
                                    if self.current_char is not None and self.current_char in com_dlm:
                                        tokens.append(Token(TT_KEYWORD, ident_str))
                                        continue
                                    elif self.current_char is not None and self.current_char not in com_dlm and self.current_char not in ALPHANUM:
                                        errors.append(IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                                        self.advance()
                                        continue


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
                                        if self.current_char is not None and self.current_char in com_dlm:
                                            tokens.append(Token(TT_KEYWORD, ident_str))
                                            continue
                                        elif self.current_char is not None and self.current_char not in com_dlm and self.current_char not in ALPHANUM:
                                            errors.append(IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                                            self.advance()
                                            continue

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
                                            if self.current_char is not None and self.current_char in com_dlm:
                                                tokens.append(Token(TT_KEYWORD, ident_str))
                                                continue
                                            elif self.current_char is not None and self.current_char not in com_dlm and self.current_char not in ALPHANUM:
                                                errors.append(IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                                                self.advance()
                                                continue

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
                                        if self.current_char is None or self.current_char in spc_dlm:
                                            tokens.append(Token(TT_KEYWORD, ident_str))
                                            continue
                                        elif self.current_char is not None and self.current_char not in spc_dlm and self.current_char not in ALPHANUM:
                                            errors.append(IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                                            self.advance()
                                            continue


                # Letter T
                if self.current_char == "t":
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
                            self.advance()
                            if self.current_char == "e":
                                ident_str += self.current_char
                                ident_count+=1
                                self.advance()
                                if self.current_char == "r":
                                    ident_str += self.current_char
                                    ident_count+=1
                                    self.advance()
                                    if self.current_char is None or self.current_char in com_dlm:
                                        tokens.append(Token(TT_KEYWORD, ident_str))
                                        continue
                                    elif self.current_char is not None and self.current_char not in com_dlm and self.current_char not in ALPHANUM:
                                        errors.append(IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                                        self.advance()
                                        continue

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
                                if self.current_char is None or self.current_char in lwk_dlm:
                                    tokens.append(Token(TT_KEYWORD, ident_str))
                                    continue
                                elif self.current_char is not None and self.current_char not in lwk_dlm and self.current_char not in ALPHANUM:
                                    errors.append(IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                                    self.advance()
                                    continue

                    if self.current_char == 's':
                        ident_str += self.current_char
                        ident_count+=1
                        self.advance()
                        if self.current_char is None or self.current_char in com_dlm:
                            tokens.append(Token(TT_KEYWORD, ident_str))
                            continue
                        elif self.current_char is not None and self.current_char not in com_dlm and self.current_char not in ALPHANUM:
                            errors.append(IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                            self.advance()
                            continue

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
                                if self.current_char is None or self.current_char in com_dlm:
                                    tokens.append(Token(TT_KEYWORD, ident_str))
                                    continue
                                elif self.current_char is not None and self.current_char not in com_dlm and self.current_char not in ALPHANUM:
                                    errors.append(IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                                    self.advance()
                                    continue

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
                            if self.current_char is not None and self.current_char in com_dlm:
                                tokens.append(Token(TT_KEYWORD, ident_str))
                                continue
                            elif self.current_char is not None and self.current_char not in com_dlm and self.current_char not in ALPHANUM:
                                errors.append(IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                                self.advance()
                                continue

                            
                maxIdentifierLength = 20

                while self.current_char is not None and self.current_char in ALPHANUM:
                    ident_str += self.current_char
                    self.advance()

                if len(ident_str) > maxIdentifierLength:
                    errors.append(IllegalCharError(pos_start, self.pos, f"Identifier '{ident_str}' exceeds maximum length of {maxIdentifierLength} characters."))
                    continue

                elif self.current_char is None or self.current_char in identif_dlm:
                    tokens.append(Token(TT_IDENTIFIER, ident_str))
                    continue

                elif self.current_char is not None and self.current_char not in identif_dlm and self.current_char not in ALPHANUM:
                    errors.append(IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                    self.advance()
                    continue



            elif self.current_char == "+":
                ident_str = self.current_char
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char == "+":
                    ident_str += self.current_char
                    self.advance()
                    if self.current_char is None or self.current_char in unary_dlm:
                        tokens.append(Token(TT_INC, ident_str))
                        continue
                    else:
                        errors.append(IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                        self.advance()
                        continue
                elif self.current_char is not None and self.current_char in plus_dlm:
                    tokens.append(Token(TT_PLUS, ident_str))
                    continue
                else:
                    errors.append(IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                    self.advance()
                    continue
                
            elif self.current_char == "!":
                ident_str = self.current_char
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char == "=":
                    ident_str += self.current_char
                    self.advance()
                    if self.current_char is not None and self.current_char in relat_dlm:
                        tokens.append(Token(TT_NEQ, ident_str))
                        continue
                    else:
                        errors.append(IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                        self.advance()
                        continue
                elif self.current_char is not None and self.current_char in not_dlm:
                    tokens.append(Token(TT_NOT, ident_str))
                    continue
                else:
                    errors.append(IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                    self.advance()
                    continue

                
            elif self.current_char == "%":
                ident_str = self.current_char
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char is not None and self.current_char in operator_dlm:
                    tokens.append(Token(TT_MOD, ident_str))
                    continue
                else:
                    errors.append(IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                    self.advance()
                    continue
    
            elif self.current_char == "&":
                ident_str = self.current_char
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char == "&":
                    ident_str += self.current_char
                    self.advance()
                    if self.current_char is not None and self.current_char in operator_dlm:
                        tokens.append(Token(TT_AND, ident_str))
                        continue
                    else:
                        errors.append(IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                        self.advance()
                        continue
                else:
                    errors.append(IllegalCharError(pos_start, self.pos, f"Invalid character '{ident_str}'"))
                    self.advance()
                    continue
                    
            elif self.current_char == "(":
                ident_str = self.current_char
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char is not None and self.current_char in oppar_dlm:
                    tokens.append(Token(TT_OPPAR, ident_str))
                    continue
                else:
                    errors.append(IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                    self.advance()
                    continue
                
            elif self.current_char == ")":
                ident_str = self.current_char
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char is None or self.current_char in clpar_dlm:
                    tokens.append(Token(TT_CLPAR, ident_str))
                    continue
                else:
                    errors.append(IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                    self.advance()
                    continue
                

            elif self.current_char == "-":
                ident_str = self.current_char
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char in ALPHANUM:
                    tokens.append(Token(TT_NEGAT, ident_str))
                    continue
                elif self.current_char == "-":
                    ident_str += self.current_char
                    self.advance()
                    if self.current_char is None or self.current_char in unary_dlm:
                        tokens.append(Token(TT_DEC, ident_str))
                        continue
                    else:
                        errors.append(IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                        self.advance()
                        continue
                elif self.current_char is not None and self.current_char in minus_dlm:
                    tokens.append(Token(TT_MINUS, ident_str))
                    continue
                else:
                    errors.append(IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                    self.advance()
                    continue

            elif self.current_char == "*":
                ident_str = self.current_char
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char is None or self.current_char in operator_dlm:
                    tokens.append(Token(TT_MUL, ident_str))
                    continue
                else:
                    errors.append(IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                    self.advance()
                    continue
                
            elif self.current_char == ",":
                ident_str = self.current_char
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char is not None and self.current_char in comma_dlm:
                    tokens.append(Token(TT_COMMA, ident_str))
                    continue
                else:
                    errors.append(IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                    self.advance()
                    continue
            
            elif self.current_char == "\\":
                ident_str = self.current_char
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char == "\"":
                    ident_str += self.current_char
                    self.advance()
                    if self.current_char is None or self.current_char in esc_dlm:
                        tokens.append(Token(TT_ESCAPESEQUENCE, ident_str))
                        continue
                    else:
                        errors.append(IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                        self.advance()
                        continue
                elif self.current_char == "*":
                    ident_str += self.current_char
                    self.advance()
                    if self.current_char is None or self.current_char in esc_dlm:
                        tokens.append(Token(TT_ESCAPESEQUENCE, ident_str))
                        continue
                    else:
                        errors.append(IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                        self.advance()
                        continue
                elif self.current_char == "{":
                    ident_str += self.current_char
                    self.advance()
                    if self.current_char is None or self.current_char in esc_dlm:
                        tokens.append(Token(TT_ESCAPESEQUENCE, ident_str))
                        continue
                    else:
                        errors.append(IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                        self.advance()
                        continue
                elif self.current_char == "}":
                    ident_str += self.current_char
                    self.advance()
                    if self.current_char is None or self.current_char in esc_dlm:
                        tokens.append(Token(TT_ESCAPESEQUENCE, ident_str))
                        continue
                    else:
                        errors.append(IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                        self.advance()
                        continue
                elif self.current_char == "n":
                    ident_str += self.current_char
                    self.advance()
                    if self.current_char is None or self.current_char in esc_dlm:
                        tokens.append(Token(TT_ESCAPESEQUENCE, ident_str))
                        continue
                    else:
                        errors.append(IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                        self.advance()
                        continue
                elif self.current_char == "t":
                    ident_str += self.current_char
                    self.advance()
                    if self.current_char is None or self.current_char in esc_dlm:
                        tokens.append(Token(TT_ESCAPESEQUENCE, ident_str))
                        continue
                    else:
                        errors.append(IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                        self.advance()
                        continue
                else:
                    errors.append(IllegalCharError(pos_start, self.pos, f"Invalid character '{ident_str}'"))
                    self.advance()
                    continue    
                
            elif self.current_char == ";":
                ident_str = self.current_char
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char is not None and self.current_char in scolon_dlm:
                    tokens.append(Token(TT_SEMICOL, ident_str))
                    continue
                else:
                    errors.append(IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                    self.advance()
                    continue
                
            elif self.current_char == "[":
                ident_str = self.current_char
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char is not None and self.current_char in opbra_dlm:
                    tokens.append(Token(TT_OPBRA, ident_str))
                    continue
                else:
                    errors.append(IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                    self.advance()
                    continue
                
            elif self.current_char == "]":
                ident_str = self.current_char
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char is None or self.current_char in clbra_dlm:
                    tokens.append(Token(TT_CLBRA, ident_str))
                    continue
                else:
                    errors.append(IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                    self.advance()
                    continue
                
            elif self.current_char == "{":
                ident_str = self.current_char
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char is not None and self.current_char in opcur_dlm:
                    tokens.append(Token(TT_OPCUR, ident_str))
                    continue
                else:
                    errors.append(IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                    self.advance()
                    continue
                
            elif self.current_char == "}":
                ident_str = self.current_char 
                pos_start = self.pos.copy() 
                self.advance()
                if self.current_char is None or self.current_char in clcur_dlm:
                    tokens.append(Token(TT_CLCUR, ident_str))
                    continue
                else: 
                    errors.append(IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                    self.advance()
                    continue

            elif self.current_char == "|":
                ident_str = self.current_char
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char == "|":
                    ident_str += self.current_char
                    self.advance()
                    if self.current_char is not None and self.current_char in operator_dlm:
                        tokens.append(Token(TT_OR, ident_str))
                        continue
                    else:
                        errors.append(IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                        self.advance()
                        continue
                else:
                    errors.append(IllegalCharError(pos_start, self.pos, f"Invalid character '{ident_str}'"))
                    self.advance()
                    continue

            elif self.current_char == "<":
                ident_str = self.current_char
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char == "=":
                    ident_str += self.current_char
                    self.advance()
                    if self.current_char is not None and self.current_char in operator_dlm:
                        tokens.append(Token(TT_LTE, ident_str))
                        continue
                    else:
                        errors.append(IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                        self.advance()
                        continue
                elif self.current_char is not None and self.current_char in operator_dlm:
                    tokens.append(Token(TT_LT, ident_str))
                    continue
                else:
                    errors.append(IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                    self.advance()
                    continue

            elif self.current_char == ">":
                ident_str = self.current_char
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char == "=":
                    ident_str += self.current_char
                    self.advance()
                    if self.current_char is not None and self.current_char in operator_dlm:
                        tokens.append(Token(TT_GTE, ident_str))
                        continue
                    else:
                        errors.append(IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                        self.advance()
                        continue
                elif self.current_char is not None and self.current_char in operator_dlm:
                    tokens.append(Token(TT_GT, ident_str))
                    continue
                else:
                    errors.append(IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                    self.advance()
                    continue

            elif self.current_char == "=":
                ident_str = self.current_char
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char == "=":
                    ident_str += self.current_char
                    self.advance()
                    if self.current_char is not None and self.current_char in relat_dlm:
                        tokens.append(Token(TT_EQ, ident_str))
                        continue
                    else:
                        errors.append(IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                        self.advance()
                        continue
                elif self.current_char is not None and self.current_char in equal_dlm:
                    tokens.append(Token(TT_IS, ident_str))
                    continue
                else:
                    errors.append(IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                    self.advance()
                    continue
            
            elif self.current_char == ":":
                ident_str = self.current_char
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char is None or self.current_char in endln_dlm:
                    tokens.append(Token(TT_COL, ident_str))
                    continue
                else:
                    errors.append(IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                    self.advance()
                    continue
                
            elif self.current_char == ".":
                ident_str = self.current_char
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char is not None and self.current_char in ALPHA:
                    tokens.append(Token(TT_DOT, ident_str))
                    continue
                elif self.current_char is not None and self.current_char in NUM:
                    ident_str += self.current_char
                    errors.append(IllegalCharError(pos_start, self.pos, f"Invalid integer value before '{ident_str}'"))
                    self.advance()
                    continue
                else:
                    errors.append(IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                    self.advance()
                    continue

            elif self.current_char == '\n':
                ident_str = self.current_char
                pos_start = self.pos.copy()
                tokens.append(Token(TT_NL, "\\n"))
                self.advance()
                

            elif self.current_char == '\t':
                ident_str = self.current_char
                pos_start = self.pos.copy()
                while self.current_char == '\t':
                    self.advance()
                

            elif self.current_char == ' ':
                ident_str = self.current_char
                pos_start = self.pos.copy()
                self.advance()
                while self.current_char == ' ':
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
                    invalid_part = ""
                    while self.current_char is not None and self.current_char not in NUM + lit_dlm and self.current_char in ALPHA:
                        invalid_part += self.current_char
                        self.advance()

                    ident_str += invalid_part
                    errors.append(IllegalCharError(pos_start, self.pos, f"Invalid identifier '{ident_str}'"))
                    self.advance()
                    continue

                if dot_count == 0: 
                    ident_str = ident_str.lstrip("0") or "0"
                    if len(ident_str) > 10: 
                        errors.append(IllegalCharError(pos_start, self.pos, f"'{ident_str}' exceeds maximum number of characters"))
                        self.advance()
                        continue
                    tokens.append(Token(TT_CHUNGUS, ident_str))
                    
                else:  # Float case
                    parts = ident_str.split(".")
                    integer_part = parts[0].lstrip("0") or "0"
                    fractional_part = parts[1].rstrip("0") or "0"

                    ident_str = f"{integer_part}.{fractional_part}"

                    if len(integer_part) > 10 or len(fractional_part) > 5:
                        errors.append(IllegalCharError(pos_start, self.pos, f"'{ident_str}' exceeds maximum number of characters"))
                        self.advance()
                        continue
                    tokens.append(Token(TT_CHUDELUXE, ident_str))

            elif self.current_char == '"':
                string = ''
                pos_start = self.pos.copy()
                escape_character = False
                string += self.current_char
                self.advance()

                escape_characters = {
                    'n': '\n',
                    't': '\t'
                }

                while self.current_char is not None and (self.current_char != '"' or escape_character):
                    if escape_character:
                        string += escape_characters.get(self.current_char, self.current_char)
                        escape_character = False
                    else:
                        if self.current_char == '\\':
                            escape_character = True
                        elif self.current_char == '\n':
                            pos_end = self.pos.copy()
                            break
                        else:
                            string += self.current_char
                    self.advance()

                if self.current_char == '"':
                    string += self.current_char
                    self.advance()

                else:
                    pos_end = self.pos.copy()
                    errors.append(IllegalCharError(pos_start, pos_end, f"Missing closing '\"' after '{string}'"))
                    continue

                if self.current_char is not None and self.current_char not in lit_dlm:
                    errors.append(IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after string literal '{string}'"))
                    self.advance()
                    continue
            
                string = string.replace('\n', '\\n')
                tokens.append(Token(TT_FORSENCD, string))
                continue
    
            elif self.current_char == "'":
                string = ''
                char = ''
                pos_start = self.pos.copy()
                string += self.current_char
                self.advance()

                while self.current_char is not None and self.current_char != "'":
                    if self.current_char == '\n':
                        pos_end = self.pos.copy()
                        break
                    elif self.current_char == '\\':
                        pos_end = self.pos.copy()
                        break
                    else:
                        string += self.current_char
                        char += self.current_char
                    self.advance()

                if self.current_char == "'":
                    string += self.current_char
                    self.advance()
                    
                else:
                    pos_end = self.pos.copy()
                    errors.append(IllegalCharError(pos_start, pos_end, f"Missing closing '\'' after '{string}'"))
                    continue

                if len(char) > 1:
                    errors.append(IllegalCharError(pos_start, self.pos, f"Character literal '{string}' exceeds maximum length of 1 character."))
                    continue

                if self.current_char is not None and self.current_char not in lit_dlm:
                    errors.append(IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{string}'"))
                    self.advance()
                    continue

                tokens.append(Token(TT_FORSEN, string))
                continue


            elif self.current_char == "/":
                ident_str = self.current_char
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char == "/":
                    ident_str += self.current_char
                    self.advance()
                    while self.current_char is not None and self.current_char != "\n":
                        ident_str += self.current_char
                        self.advance()
                    tokens.append(Token(TT_COMMENT, ident_str))
                    continue
                elif self.current_char == "*":
                    ident_str += self.current_char
                    self.advance()
                    while self.current_char is not None:
                        if self.current_char == "*" and self.text[self.pos.idx + 1] == "/":
                            ident_str += "*/"
                            self.advance()
                            self.advance()
                            break
                        else:
                            ident_str += self.current_char
                            self.advance()
                    tokens.append(Token(TT_COMMENT, ident_str))
                    continue    
                elif self.current_char is not None and self.current_char in operator_dlm:
                    tokens.append(Token(TT_DIV, ident_str))
                    continue
                else:
                    errors.append(IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{string}'"))
                    self.advance()
                    continue
            
            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                errors.append(IllegalCharError(pos_start, self.pos, f"Invalid character '" + char + "'"))
                self.advance()
                continue
                
        if self.current_char is None:
            tokens.append(Token(TT_EOF, "EOF"))
        return tokens, errors

    
def run(fn, text):
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    return tokens, error