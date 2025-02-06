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
ARITH_OPER = '+-/*%'
RELAT_OPER = '<>!='
OPER = ARITH_OPER + RELAT_OPER

#DELIMITERS

clbra_dlm = ' =\n)\t'
clcur_dlm = ' \n)}\t'
clpar_dlm = ' \n}{)&|}\t' + ARITH_OPER
com_dlm =   '('
comma_dlm = ' _"\t' + ALPHANUM
comnt_dlm = ' \n\t' + ASCII
dot_dlm = ALPHA
endln_dlm = ' \n\t'
esc_dlm =   ' "\t'+ ASCII
equal_dlm = ' _[(-"+\t' + ALPHANUM
hawk_dlm =  ' \n{\t'
identif_dlm = ' \n)(&|;[],.\t' + OPER
lit_dlm =   ' ,):\n;\t/+-%*' + OPER
lwk_dlm =   ' \n&|=)\t' 
minus_dlm = ' -()\t' + ALPHANUM
npc_dlm =   ' :\t' + ALPHANUM
not_dlm =   ' =(\t' + ALPHANUM
opbra_dlm = ' "]\t' + ALPHANUM
opcur_dlm = ' \n\t}' + ALPHANUM
operator_dlm = ' _(\t' + ALPHANUM
oppar_dlm = ' _)("-\t' + ALPHANUM
plus_dlm =  ' _("+)\t' + ALPHANUM
relat_dlm = ' _("\t' + ALPHANUM
scolon_dlm = ' _+-\t' + ALPHANUM
spc_dlm =   ' \t'
unary_dlm = ' _)\t' + ALPHANUM

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
        return f"Ln {self.pos_start.ln + 1} Col {self.pos_start.col + 1} Lexical Error: {self.details}"


#TOKENS

TT_CHUNGUS      = 'CHUNGUS'     # Whole Numbers '3'
TT_CHUDELUXE    = 'CHUDELUXE'   # Decimal Numbers '3.14'
TT_FORSEN       = 'FORSEN'  # Strings 
TT_FORSENCD     = 'FORSENCD' #Char

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
                                        if self.current_char is not None and self.current_char in com_dlm:
                                            tokens.append(Token(TT_KEYWORD, ident_str))
                                            continue
                                        else:
                                            tokens.append(Token(TT_KEYWORD, ident_str))
                                            return tokens, IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'")

                                            
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
                                else:
                                    tokens.append(Token(TT_KEYWORD, ident_str))
                                    return tokens, IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'")
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
                                else:
                                    tokens.append(Token(TT_KEYWORD, ident_str))
                                    return tokens, IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'")

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
                                        else:
                                            tokens.append(Token(TT_KEYWORD, ident_str))
                                            return tokens, IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'")
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
                                else:
                                    tokens.append(Token(TT_KEYWORD, ident_str))
                                    return tokens, IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'")
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
                                            if self.current_char is None or self.current_char in spc_dlm:
                                                tokens.append(Token(TT_KEYWORD, ident_str))
                                                continue
                                            else:
                                                tokens.append(Token(TT_KEYWORD, ident_str))
                                                return tokens, IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'")
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
                                                    if self.current_char is None or self.current_char in spc_dlm:
                                                        tokens.append(Token(TT_KEYWORD, ident_str))
                                                        continue
                                                    else:
                                                        tokens.append(Token(TT_KEYWORD, ident_str))
                                                        return tokens, IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'")  

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
                                    else:
                                        tokens.append(Token(TT_KEYWORD, ident_str))
                                        return tokens, IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'")
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
                                        if self.current_char is None or self.current_char in spc_dlm:
                                            tokens.append(Token(TT_KEYWORD, ident_str))
                                            continue
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
                                                else:
                                                    return tokens, IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'")
                                            

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
                                        if self.current_char is None or self.current_char in endln_dlm:
                                            tokens.append(Token(TT_KEYWORD, ident_str))
                                            continue
                                        else:
                                            tokens.append(Token(TT_KEYWORD, ident_str))
                                            return tokens, IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'")
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
                            else:
                                return tokens, IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'") 

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
                                                    if self.current_char is not None and self.current_char in com_dlm:
                                                        tokens.append(Token(TT_KEYWORD, ident_str))
                                                        continue
                                                    else:
                                                        tokens.append(Token(TT_KEYWORD, ident_str))
                                                        return tokens, IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'")
                                if self.current_char is None or self.current_char in hawk_dlm:
                                    tokens.append(Token(TT_KEYWORD, ident_str))
                                    continue
                                else:
                                    tokens.append(Token(TT_KEYWORD, ident_str))
                                    return tokens, IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'")
                                
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
                                        else:
                                            tokens.append(Token(TT_KEYWORD, ident_str))
                                            return tokens, IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'")
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
                            else:
                                tokens.append(Token(TT_KEYWORD, ident_str))
                                return tokens, IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'")

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
                                                        else:
                                                            tokens.append(Token(TT_KEYWORD, ident_str))
                                                            return tokens, IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'")
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
                            else:
                                tokens.append(Token(TT_KEYWORD, ident_str))
                                return tokens, IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'")
                        
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
                            else:
                                tokens.append(Token(TT_KEYWORD, ident_str))
                                return tokens, IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'")

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
                                    else:
                                        tokens.append(Token(TT_KEYWORD, ident_str))
                                        return tokens, IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'")
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
                            else:
                                tokens.append(Token(TT_KEYWORD, ident_str))
                                return tokens, IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'")
                        
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
                                    else:
                                        tokens.append(Token(TT_KEYWORD, ident_str))
                                        return tokens, IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'")
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
                                    else:
                                        tokens.append(Token(TT_KEYWORD, ident_str))
                                        return tokens, IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'")

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
                                        else:
                                            tokens.append(Token(TT_KEYWORD, ident_str))
                                            return tokens, IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'")
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
                                            else:
                                                tokens.append(Token(TT_KEYWORD, ident_str))
                                                return tokens, IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'")
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
                                        else:
                                            tokens.append(Token(TT_KEYWORD, ident_str))
                                            return tokens, IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'")

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
                                    else:
                                        tokens.append(Token(TT_KEYWORD, ident_str))
                                        return tokens, IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'")
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
                                else:
                                    tokens.append(Token(TT_KEYWORD, ident_str))
                                    return tokens, IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'")
                    if self.current_char == 's':
                        ident_str += self.current_char
                        ident_count+=1
                        self.advance()
                        if self.current_char is None or self.current_char in com_dlm:
                            tokens.append(Token(TT_KEYWORD, ident_str))
                            continue
                        else:
                            tokens.append(Token(TT_KEYWORD, ident_str))
                            return tokens, IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'")
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
                                else:
                                    tokens.append(Token(TT_KEYWORD, ident_str))
                                    return tokens, IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'")
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
                            else:
                                tokens.append(Token(TT_KEYWORD, ident_str))
                                return tokens, IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'")
                            
                MAX_IDENTIFIER_LENGTH = 20

                while self.current_char is not None and self.current_char in ALPHANUM:
                    if len(ident_str) < MAX_IDENTIFIER_LENGTH:
                        ident_str += self.current_char
                    else:
                        self.advance()
                        return tokens, IllegalCharError(
                            pos_start, self.pos, 
                            f"Identifier '{ident_str + self.current_char}' exceeds maximum length of {MAX_IDENTIFIER_LENGTH} characters."
                        )
                    self.advance()

                if self.current_char is None or self.current_char in identif_dlm:
                    tokens.append(Token(TT_IDENTIFIER, ident_str))
                else:
                    tokens.append(Token(TT_IDENTIFIER, ident_str))
                    return tokens, IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'")



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
                        tokens.append(Token(TT_INC, ident_str))
                        return tokens, IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'")
                elif self.current_char is not None and self.current_char in plus_dlm:
                    tokens.append(Token(TT_PLUS, ident_str))
                    continue
                else:
                    tokens.append(Token(TT_PLUS, ident_str))
                    return tokens, IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'")
                
            elif self.current_char == "!":
                ident_str = self.current_char
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char == "=":
                    ident_str += self.current_char
                    self.advance()
                    if self.current_char is not None and self.current_char in relat_dlm:
                        tokens.append(Token(TT_INC, ident_str))
                        continue
                    else:
                        tokens.append(Token(TT_INC, ident_str))
                        return tokens, IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'")
                elif self.current_char is None or self.current_char in not_dlm:
                    tokens.append(Token(TT_PLUS, ident_str))
                    continue
                else:
                    tokens.append(Token(TT_PLUS, ident_str))
                    return tokens, IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'")

                
            elif self.current_char == "%":
                ident_str = self.current_char
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char is not None and self.current_char in operator_dlm:
                    tokens.append(Token(TT_MOD, ident_str))
                    continue
                else:
                    tokens.append(Token(TT_MOD, ident_str))
                    return tokens, IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'")
    
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
                        tokens.append(Token(TT_AND, ident_str))
                        return tokens, IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'")
                    
            elif self.current_char == "(":
                ident_str = self.current_char
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char is not None and self.current_char in oppar_dlm:
                    tokens.append(Token(TT_OPPAR, ident_str))
                    continue
                else:
                    tokens.append(Token(TT_OPPAR, ident_str))
                    return tokens, IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'")
                
            elif self.current_char == ")":
                ident_str = self.current_char
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char is None or self.current_char in clpar_dlm:
                    tokens.append(Token(TT_CLPAR, ident_str))
                    continue
                else:
                    tokens.append(Token(TT_CLPAR, ident_str))
                    return tokens, IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'")
                

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
                        tokens.append(Token(TT_DEC, ident_str))
                        return tokens, IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'")
                elif self.current_char is not None and self.current_char in minus_dlm:
                    tokens.append(Token(TT_MINUS, ident_str))
                    continue
                else:
                    tokens.append(Token(TT_MINUS, ident_str))
                    return tokens, IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'")

            elif self.current_char == "*":
                ident_str = self.current_char
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char is None or self.current_char in operator_dlm:
                    tokens.append(Token(TT_MUL, ident_str))
                    continue
                else:
                    tokens.append(Token(TT_MUL, ident_str))
                    return tokens, IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'")
                
            elif self.current_char == ",":
                ident_str = self.current_char
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char is not None and self.current_char in comma_dlm:
                    tokens.append(Token(TT_COMMA, ident_str))
                    continue
                else:
                    tokens.append(Token(TT_COMMA, ident_str))
                    return tokens, IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'")
            
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
                        tokens.append(Token(TT_ESCAPESEQUENCE, ident_str))
                        return tokens, IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'")
                elif self.current_char == "*":
                    ident_str += self.current_char
                    self.advance()
                    if self.current_char is None or self.current_char in esc_dlm:
                        tokens.append(Token(TT_ESCAPESEQUENCE, ident_str))
                        continue
                    else:
                        tokens.append(Token(TT_ESCAPESEQUENCE, ident_str))
                        return tokens, IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'")
                elif self.current_char == "{":
                    ident_str += self.current_char
                    self.advance()
                    if self.current_char is None or self.current_char in esc_dlm:
                        tokens.append(Token(TT_ESCAPESEQUENCE, ident_str))
                        continue
                    else:
                        tokens.append(Token(TT_ESCAPESEQUENCE, ident_str))
                        return tokens, IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'")
                elif self.current_char == "}":
                    ident_str += self.current_char
                    self.advance()
                    if self.current_char is None or self.current_char in esc_dlm:
                        tokens.append(Token(TT_ESCAPESEQUENCE, ident_str))
                        continue
                    else:
                        tokens.append(Token(TT_ESCAPESEQUENCE, ident_str))
                        return tokens, IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'")
                elif self.current_char == "n":
                    ident_str += self.current_char
                    self.advance()
                    if self.current_char is None or self.current_char in esc_dlm:
                        tokens.append(Token(TT_ESCAPESEQUENCE, ident_str))
                        continue
                    else:
                        tokens.append(Token(TT_ESCAPESEQUENCE, ident_str))
                        return tokens, IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'")
                elif self.current_char == "t":
                    ident_str += self.current_char
                    self.advance()
                    if self.current_char is None or self.current_char in esc_dlm:
                        tokens.append(Token(TT_ESCAPESEQUENCE, ident_str))
                        continue
                    else:
                        tokens.append(Token(TT_ESCAPESEQUENCE, ident_str))
                        return tokens, IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'")
                else:
                    tokens.append(Token(TT_ESCAPESEQUENCE, ident_str))
                    return tokens, IllegalCharError(pos_start, self.pos, f"Invalid delimiter after '{self.current_char}'")
                
            elif self.current_char == ";":
                ident_str = self.current_char
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char is not None and self.current_char in scolon_dlm:
                    tokens.append(Token(TT_SEMICOL, ident_str))
                    continue
                else:
                    tokens.append(Token(TT_SEMICOL, ident_str))
                    return tokens, IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'")
                
            elif self.current_char == "[":
                ident_str = self.current_char
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char is not None and self.current_char in opbra_dlm:
                    tokens.append(Token(TT_OPBRA, ident_str))
                    continue
                else:
                    tokens.append(Token(TT_OPBRA, ident_str))
                    return tokens, IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'")
                
            elif self.current_char == "]":
                ident_str = self.current_char
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char is None or self.current_char in clbra_dlm:
                    tokens.append(Token(TT_CLBRA, ident_str))
                    continue
                else:
                    tokens.append(Token(TT_CLBRA, ident_str))
                    return tokens, IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'")
                
            elif self.current_char == "{":
                ident_str = self.current_char
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char is not None and self.current_char in opcur_dlm:
                    tokens.append(Token(TT_OPCUR, ident_str))
                    continue
                else:
                    tokens.append(Token(TT_OPCUR, ident_str))
                    return tokens, IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'")
                
            elif self.current_char == "}":
                ident_str = self.current_char 
                pos_start = self.pos.copy() 
                self.advance()
                if self.current_char is None or self.current_char in clcur_dlm:
                    tokens.append(Token(TT_CLCUR, ident_str))
                    continue
                else: 
                    tokens.append(Token(TT_CLCUR, ident_str))
                    return tokens, IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'")

            elif self.current_char == '|':
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char == "|":
                    ident_str += self.current_char
                    self.advance()
                    if self.current_char is not None and self.current_char in operator_dlm:
                        tokens.append(Token(TT_OR, ident_str))
                        continue
                    else:
                        tokens.append(Token(TT_OR, ident_str))
                        return tokens, IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'")

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
                        tokens.append(Token(TT_LTE, ident_str))
                        return tokens, IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'")
                elif self.current_char is not None and self.current_char in operator_dlm:
                    tokens.append(Token(TT_LT, ident_str))
                    continue
                else:
                    tokens.append(Token(TT_LT, ident_str))
                    return tokens, IllegalCharError(pos_start, self.pos, f"Invalid delimiter after '{self.current_char}'")

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
                        tokens.append(Token(TT_GTE, ident_str))
                        return tokens, IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'")
                elif self.current_char is not None and self.current_char in operator_dlm:
                    tokens.append(Token(TT_GT, ident_str))
                    continue
                else:
                    tokens.append(Token(TT_GT, ident_str))
                    return tokens, IllegalCharError(pos_start, self.pos, f"Invalid delimiter after '{self.current_char}'")

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
                        tokens.append(Token(TT_EQ, ident_str))
                        return tokens, IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'")
                elif self.current_char is not None and self.current_char in equal_dlm:
                    tokens.append(Token(TT_IS, ident_str))
                    continue
                else:
                    tokens.append(Token(TT_IS, ident_str))
                    return tokens, IllegalCharError(pos_start, self.pos, f"Invalid delimiter after '{self.current_char}'")
            
            elif self.current_char == ":":
                ident_str = self.current_char
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char is None or self.current_char in endln_dlm:
                    tokens.append(Token(TT_COL, ident_str))
                    continue
                else:
                    tokens.append(Token(TT_COL, ident_str))
                    return tokens, IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'")
                
            elif self.current_char == ".":
                ident_str = self.current_char
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char is not None and self.current_char in ALPHA:
                    tokens.append(Token(TT_DOT, ident_str))
                    continue
                else:
                    tokens.append(Token(TT_DOT, ident_str))
                    return tokens, IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'")

            elif self.current_char == '\n':
                ident_str = self.current_char
                pos_start = self.pos.copy()
                while self.current_char == '\n':
                    self.advance()
                tokens.append(Token(TT_NL, '\\n'))

            elif self.current_char == '\t':
                ident_str = self.current_char
                pos_start = self.pos.copy()
                while self.current_char == '\t':
                    self.advance()
                tokens.append(Token(TT_TAB, '\\t'))

            elif self.current_char == ' ':
                ident_str = self.current_char
                pos_start = self.pos.copy()
                self.advance()
                while self.current_char == ' ':
                    self.advance()
                tokens.append(Token(TT_SPC, 'spc'))

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

                    if self.current_char is not None and self.current_char not in lit_dlm:
                        return tokens, IllegalCha\rError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'")
                    else:
                        return tokens, IllegalCharError(pos_start, self.pos, f"'{ident_str}' (invalid identifier)")

                if dot_count == 0: 
                    ident_str = ident_str.lstrip("0") or "0"
                    if len(ident_str) > 10: 
                        return tokens, IllegalCharError(pos_start, self.pos, f"'{ident_str}' exceeds maximum number of characters")
                    tokens.append(Token(TT_CHUNGUS, ident_str))
                else:  # Float case
                    parts = ident_str.split(".")
                    integer_part = parts[0].lstrip("0") or "0"
                    fractional_part = parts[1] if len(parts) > 1 else ""

                    if fractional_part == "":
                        return tokens, IllegalCharError(pos_start, self.pos, f"'{ident_str}' is not a valid decimal number")

                    ident_str = f"{integer_part}.{fractional_part.rstrip('0') or '0'}"

                    if len(integer_part) > 10 or len(fractional_part) > 5:
                        return tokens, IllegalCharError(pos_start, self.pos, f"'{ident_str}' exceeds maximum number of characters")
                    tokens.append(Token(TT_CHUDELUXE, ident_str))

            elif self.current_char == '"':
                 # Token for Strings

                string = ''
                pos_start = self.pos.copy()
                escape_character = False
                string += self.current_char
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

                

                if self.current_char != '"' and self.current_char is None:
                    pos_end = self.pos.copy()
                    return tokens, IllegalCharError(pos_start, pos_end, f"Missing '\"' after '{string}' forsencd literal")
                
                if self.current_char == '"':
                    string += self.current_char
                    self.advance()

                if self.current_char is not None and self.current_char not in lit_dlm:
                    return tokens, IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{string}'")

                tokens.append(Token(TT_FORSENCD, string))
                continue
    

            elif self.current_char == "'":
                string = ''
                char = ''
                pos_start = self.pos.copy()
                escape_character = False
                string += self.current_char
                self.advance()

                escape_characters = {
                    'n': '\n',
                    't': '\t'
                }

                while self.current_char != None and (self.current_char != "'" or escape_character):
                    if escape_character:
                        string += escape_characters.get(self.current_char, self.current_char)
                        escape_character = False
                    else:
                        if self.current_char == '\\':
                            escape_character = True
                        else:
                            string += self.current_char
                            char += self.current_char
                    self.advance()

                if len(char) > 1:
                    return tokens, IllegalCharError(
                        pos_start, self.pos, 
                        f"Identifier '{string + self.current_char}' exceeds maximum length of '1' character/s."
                    )
                    self.advance()

                if self.current_char != "'" and self.current_char is None:
                    pos_end = self.pos.copy()
                    return tokens, IllegalCharError(pos_start, pos_end, f"Missing '\'' after '{string}' forsen literal")
                
                if self.current_char == "'":
                    string += self.current_char
                    self.advance()

                if self.current_char is not None and self.current_char not in lit_dlm:
                    return tokens, IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{string}'")

                tokens.append(Token(TT_FORSEN, string))
                continue

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
                elif self.current_char is not None and self.current_char in operator_dlm:
                    tokens.append(Token(TT_DIV, ident_str))
                    continue
                else:
                    tokens.append(Token(TT_DIV, ident_str))
                    return tokens, IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'")
            
            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return[], IllegalCharError(pos_start, self.pos, "'" + char + "'")
                
        if self.current_char is None:
            tokens.append(Token(TT_EOF, ""))
        return tokens, None

        
    
    def make_string(self):
        string = ''
        pos_start = self.pos.copy()
        escape_character = False
        string += self.current_char
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

        if self.current_char != '"' and self.current_char is None:
            pos_end = self.pos.copy()
            return [], IllegalCharError(pos_start, pos_end, "Missing \" after forsencd literal")
        
        if self.current_char == '"':
            string += self.current_char
            self.advance()

        self.advance()

        if self.current_char is None or self.current_char not in lit_dlm:
            return [], IllegalCharError(pos_start, self.pos, f"'{self.current_char}'")

        return Token(TT_FORSENCD, string)
    
    def make_char(self):
        string = ''
        pos_start = self.pos.copy()
        escape_character = False
        self.advance()

        escape_characters = {
            'n': '\n',
            't': '\t'
        }

        while self.current_char is not None and (self.current_char != "'" or escape_character):
            if escape_character:
                string += escape_characters.get(self.current_char, self.current_char)
                escape_character = False
            else:
                if self.current_char == '\\':
                    escape_character = True
                else:
                    string += self.current_char
            self.advance()

        if self.current_char != "'":
            pos_end = self.pos.copy()
            return [], IllegalCharError(pos_start, pos_end, "Missing ' after forsen literal")

        self.advance()

        if not string:
            pos_end = self.pos.copy()
            return [], IllegalCharError(pos_start, pos_end, "forsen literal must contain at least one character")

        last_char = string[-1]

        if self.pos.idx < len(self.text) and self.text[self.pos.idx] not in lit_dlm:
            pos_end = self.pos.copy()
            return [], IllegalCharError(pos_start, self.pos, f"Invalid delimiter after character literal")

        return Token(TT_FORSEN, last_char)


    def make_newline(self): 
        self.advance()
        return Token(TT_NL)
    
def run(fn, text):
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()

    return tokens, error