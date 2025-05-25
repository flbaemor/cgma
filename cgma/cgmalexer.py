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
OPER = ARITH_OPER + RELAT_OPER + NOT_OPER

#DELIMITERS

clbra_dlm = ' =\n)\t,;' + OPER
clcur_dlm = ' \n)}\t,' + ALPHANUM
clpar_dlm = ' \n}{)&|}\t.,(];' + OPER + ALPHANUM
com_dlm   = ' ('
comma_dlm = ' "\t-!\'(' + ALPHANUM
convert_dlm = ' )\t,\n' + OPER
comnt_dlm = ' \n\t' + ASCII
endln_dlm = ' \n\t'
esc_dlm =   ' "\t'+ ASCII
equal_dlm = ' [(-"+\t!\'' + ALPHANUM
hawk_dlm =  ' \n{\t'
identif_dlm = ' \n)(&|;[],.\t{' + OPER
lit_dlm =   ' ,):\n;\t/+-%*]' + OPER
lwk_dlm =   ' \n&|=)\t],:;!' + RELAT_OPER
minus_dlm = ' -()\t' + ALPHANUM
npc_dlm =   ' :\t'
not_dlm =   ' =(\t' + ALPHA
opbra_dlm = ' "]\t!\'+-' + ALPHANUM
opcur_dlm = ' \n\t}' + ALPHANUM
operator_dlm = ' (\t!' + ALPHANUM
arith_operator_dlm = ' (\t' + ALPHANUM
oppar_dlm = ' )("-\t!\'+-' + ALPHANUM
plus_dlm =  ' ("+)\t' + ALPHANUM
relat_dlm = ' ("\t!' + ALPHANUM
scolon_dlm = ' +-\t' + ALPHANUM
spc_dlm =   ' \t'
unary_dlm = ' )\t\n,' + OPER

#TOKENS

TT_RW_APPEND        = 'append'
TT_RW_BACK          = 'back'
TT_RW_CASEOH        = 'caseoh'
TT_RW_CHAT          = 'chat'
TT_RW_CHUNGUS       = 'chungus'
TT_RW_CHUDELUXE     = 'chudeluxe'
TT_RW_FALSE         = 'false'
TT_RW_FEIN          = 'fein'
TT_RW_FORSEN        = 'forsen'
TT_RW_FORSENCD      = 'forsencd'
TT_RW_GETOUT        = 'getout'
TT_RW_GNG           = 'gng'
TT_RW_HAWK          = 'hawk'
TT_RW_HAWKTUAH      = 'hawktuah'
TT_RW_INSERT        = 'insert'
TT_RW_JIT           = 'jit'
TT_RW_LETHIMCOOK    = 'lethimcook'
TT_RW_LIL           = 'lil'
TT_RW_LWK           = 'lwk'
TT_RW_NOCAP         = 'nocap'
TT_RW_NPC           = 'npc'
TT_RW_PAUSE         = 'pause'
TT_RW_PLUG          = 'plug'
TT_RW_REMOVE        = 'remove'
TT_RW_SKIBIDI       = 'skibidi'
TT_RW_STURDY        = 'sturdy'
TT_RW_TRUE          = 'true'
TT_RW_TUAH          = 'tuah'
TT_RW_TAPER         = 'taper'
TT_RW_TS            = 'ts'
TT_RW_YAP           = 'yap'


TT_CHUNGUS      = 'chungus_lit'     # Whole Numbers '3'
TT_CHUDELUXE    = 'chudeluxe_lit'   # Decimal Numbers '3.14'
TT_FORSEN       = 'forsen_lit'  # Char 
TT_FORSENCD     = 'forsencd_lit' # Strings
TT_LWK          = 'lwk_lit'     # Boolean 'true' or 'false'

TT_PLUS         = '+'    # '+'
TT_MINUS        = '- '   # '-'
TT_MUL          = '*'     # '*'
TT_DIV          = '/'     # '/'
TT_MOD          = '%'     # '%'
TT_IS           = '='      # '='
TT_NEGAT        = '-'   # '-'

TT_EQ           = '=='      # '=='  
TT_NEQ          = '!='     # '!='
TT_INC          = '++'     # '++'
TT_DEC          = '--'     # '--'

TT_NOT          = '!'     # '!'
TT_AND          = '&&'     # '&&'
TT_OR           = '||'      # '||'
TT_LT           = '<'      # '<'
TT_GT           = '>'      # '>'
TT_LTE          = '<='     # '<='
TT_GTE          = '>='     # '>='

TT_OPPAR        = '('   # '('
TT_CLPAR        = ')'   # ')'
TT_OPBRA        = '['   # '['
TT_CLBRA        = ']'   # ']'
TT_OPCUR        = '{'   # '{'
TT_CLCUR        = '}'   # '}'
TT_SEMICOL      = ';' # ';'
TT_COL          = ':'   # ':'
TT_COMMA        = ','   # ','
TT_DOT          = '.'     # '.'
TT_DBLQT        = '"'   # '"'
TT_QT           = "'"   # "'"

TT_SPC          = ' '     # ' '
TT_NL           = 'nl'      # New Line
TT_TAB          = '\t'     # Tab
TT_EOF          = 'EOF'     # End of File

TT_KEYWORD      = 'keyword' # Keywords
TT_IDENTIFIER   = 'identifier' # Identifiers

TT_ESCAPESEQUENCE = 'escapesequence' # Escape Sequence
TT_COMMENT      = 'comment' # Comments


class Position:
    def __init__(self, index, ln):
        self.index = index
        self.ln = ln

    def advance(self, current_char): #Advance to the next character
        self.index += 1

        if current_char == '\n':
            self.ln +=1

        return self
    
    def copy(self): #Returnss the current position(index, line) of the character
        return Position(self.index, self.ln)
        
#ERROR
class LexicalError:
    def __init__(self, pos, details):
        self.pos = pos
        self.details = details

    def as_string(self): #Returns the error message in string format
        self.details = self.details.replace('\n', '\\n')
        return f"Ln {self.pos.ln} Lexical Error: {self.details}"
    

#TOKEN
class Token:
    def __init__(self, type_, value=None, line=1): 
        self.type = type_
        self.value = value
        self.line = line

#LEXER
class Lexer:
    def __init__(self, source_code): 
        self.source_code = source_code
        self.pos = Position(-1, 1)
        self.current_char = None
        self.advance()

    def advance(self): #Advance to the next character
        self.pos.advance(self.current_char)
        self.current_char = self.source_code[self.pos.index] if self.pos.index<len(self.source_code) else None

    def make_tokens(self):
        tokens = [] #List of tokens
        line = 1
        errors = []
        while self.current_char != None:
            if self.current_char in ALPHA:
                ident_str = ''
                pos = self.pos.copy()
                #Letter A
                if self.current_char == "a":
                    ident_str += self.current_char
                    self.advance()
                    if self.current_char == "p":
                        ident_str += self.current_char
                        self.advance()
                        if self.current_char == "p":
                            ident_str += self.current_char
                            self.advance()
                            if self.current_char == "e":
                                ident_str += self.current_char
                                self.advance()
                                if  self.current_char == "n":
                                    ident_str += self.current_char
                                    self.advance()
                                    if self.current_char == "d":
                                        ident_str += self.current_char
                                        self.advance()
                                        if self.current_char is not None and self.current_char in com_dlm:
                                            tokens.append(Token(TT_RW_APPEND, ident_str, line)) #Adds the token to the list of tokens
                                            continue
                                        elif self.current_char is not None and self.current_char not in com_dlm and self.current_char not in ALPHANUM:
                                            errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'")) #Adds the error to the list of errors
                                            continue
                                            
                #Letter B
                if self.current_char == "b":
                    ident_str += self.current_char
                    
                    self.advance()
                    if self.current_char == "a":
                        ident_str += self.current_char
                        
                        self.advance()
                        if self.current_char == "c":
                            ident_str += self.current_char
                            
                            self.advance()
                            if self.current_char == "k":
                                ident_str += self.current_char
                                
                                self.advance()
                                if self.current_char is None or self.current_char in endln_dlm:
                                    tokens.append(Token(TT_RW_BACK, ident_str, line))
                                    continue
                                elif self.current_char is not None and self.current_char not in endln_dlm and self.current_char not in ALPHANUM:
                                    errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                                    continue

                #Letter C
                if self.current_char == "c":
                    ident_str += self.current_char
                    
                    self.advance()
                    if self.current_char == "a":
                        ident_str += self.current_char
                        
                        self.advance()
                        if self.current_char == "s":
                            ident_str += self.current_char
                            
                            self.advance()
                            if self.current_char == "e":
                                ident_str += self.current_char
                                
                                self.advance()
                                if self.current_char == "o":
                                    ident_str += self.current_char
                                    
                                    self.advance()
                                    if self.current_char == "h":
                                        ident_str += self.current_char
                                        
                                        self.advance()
                                        if self.current_char is None or self.current_char in spc_dlm:
                                            tokens.append(Token(TT_RW_CASEOH, ident_str, line))
                                            continue
                                        elif self.current_char is not None and self.current_char not in spc_dlm and self.current_char not in ALPHANUM:
                                            errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                                            continue
                    elif self.current_char == "h":
                        ident_str += self.current_char
                        
                        self.advance()
                        if self.current_char == "a":
                            ident_str += self.current_char
                            
                            self.advance()
                            if self.current_char == "t":
                                ident_str += self.current_char
                                
                                self.advance()
                                if self.current_char is not None and self.current_char in com_dlm:
                                    tokens.append(Token(TT_RW_CHAT, ident_str, line))
                                    continue
                                elif self.current_char is not None and self.current_char not in com_dlm and self.current_char not in ALPHANUM:
                                    errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                                    continue
                        if self.current_char == "u":
                            ident_str += self.current_char
                            
                            self.advance()
                            if self.current_char == "d":
                                ident_str += self.current_char
                                
                                self.advance()
                                if self.current_char == "e":
                                    ident_str += self.current_char
                                    
                                    self.advance()
                                    if self.current_char == "l":
                                        ident_str += self.current_char
                                        
                                        self.advance()
                                        if self.current_char == "u":
                                            ident_str += self.current_char
                                            
                                            self.advance()
                                            if self.current_char == "x":
                                                ident_str += self.current_char
                                                
                                                self.advance()
                                                if self.current_char == "e":
                                                    ident_str += self.current_char
                                                    
                                                    self.advance()
                                                    if self.current_char is None or self.current_char in convert_dlm:
                                                        tokens.append(Token(TT_RW_CHUDELUXE, ident_str, line))
                                                        continue
                                                    elif self.current_char is not None and self.current_char not in convert_dlm and self.current_char not in ALPHANUM:
                                                        errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                                                        continue

                            elif self.current_char == "n":
                                ident_str += self.current_char
                                
                                self.advance()
                                if self.current_char == "g":
                                    ident_str += self.current_char
                                    
                                    self.advance() 
                                    if self.current_char == "u":
                                        ident_str += self.current_char
                                        
                                        self.advance()      
                                        if self.current_char == "s":
                                            ident_str += self.current_char
                                            
                                            self.advance()
                                            if self.current_char is None or self.current_char in convert_dlm:
                                                tokens.append(Token(TT_RW_CHUNGUS, ident_str, line))
                                                continue
                                            elif self.current_char is not None and self.current_char not in convert_dlm and self.current_char not in ALPHANUM:
                                                errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                                                continue

                # Letter F
                if self.current_char == "f":
                    ident_str += self.current_char
                    
                    self.advance()
                    if self.current_char == "a":
                        ident_str += self.current_char
                        
                        self.advance()
                        if self.current_char == "l":
                            ident_str += self.current_char
                            
                            self.advance()
                            if self.current_char == "s":
                                ident_str += self.current_char
                                
                                self.advance()
                                if self.current_char == "e":
                                    ident_str += self.current_char
                                    
                                    self.advance()
                                    if self.current_char is None or self.current_char in lwk_dlm:
                                        tokens.append(Token(TT_LWK, ident_str, line))
                                        continue
                                    elif self.current_char is not None and self.current_char not in lwk_dlm and self.current_char not in ALPHANUM:
                                        errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                                        continue

                    if self.current_char == "e":
                        ident_str += self.current_char
                        
                        self.advance()
                        if self.current_char == "i":
                            ident_str += self.current_char
                            
                            self.advance()
                            if self.current_char == "n":
                                ident_str += self.current_char
                                
                                self.advance()
                                if self.current_char is None or self.current_char in spc_dlm:
                                    tokens.append(Token(TT_RW_FEIN, ident_str, line))
                                    continue
                                elif self.current_char is not None and self.current_char not in spc_dlm and self.current_char not in ALPHANUM:
                                    errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                                    continue

                    if self.current_char == "o":
                        ident_str += self.current_char
                        
                        self.advance()
                        if self.current_char == "r":
                            ident_str += self.current_char
                            
                            self.advance()
                            if self.current_char == "s":
                                ident_str += self.current_char
                                
                                self.advance()
                                if self.current_char == "e":
                                    ident_str += self.current_char
                                    
                                    self.advance()
                                    if self.current_char == "n":
                                        ident_str += self.current_char
                                        
                                        self.advance()
                                        if self.current_char == "c":
                                            ident_str += self.current_char
                                            
                                            self.advance()
                                            if self.current_char == "d":
                                                ident_str += self.current_char
                                                
                                                self.advance()
                                                if self.current_char is None or self.current_char in spc_dlm:
                                                    tokens.append(Token(TT_RW_FORSENCD, ident_str, line))
                                                    continue
                                                elif self.current_char is not None and self.current_char not in spc_dlm and self.current_char not in ALPHANUM:
                                                    errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                                                    continue

                                        if self.current_char is None or self.current_char in spc_dlm:
                                            tokens.append(Token(TT_RW_FORSEN, ident_str, line))
                                            continue
                                        elif self.current_char is not None and self.current_char not in spc_dlm and self.current_char not in ALPHANUM:
                                            errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                                            continue
                                            

                # Letter G
                if self.current_char == "g":
                    ident_str += self.current_char
                    
                    self.advance()
                    if self.current_char == "e":
                        ident_str += self.current_char
                        
                        self.advance()
                        if self.current_char == "t":
                            ident_str += self.current_char
                            
                            self.advance()
                            if self.current_char == "o":
                                ident_str += self.current_char
                                
                                self.advance()
                                if self.current_char == "u":
                                    ident_str += self.current_char
                                    
                                    self.advance()
                                    if self.current_char == "t":
                                        ident_str += self.current_char
                                        
                                        self.advance()
                                        if self.current_char is None or self.current_char in endln_dlm:
                                            tokens.append(Token(TT_RW_GETOUT, ident_str, line))
                                            continue
                                        elif self.current_char is not None and self.current_char not in endln_dlm and self.current_char not in ALPHANUM:
                                            errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                                            continue

                # Letter H
                if self.current_char == "h":
                    ident_str += self.current_char
                    
                    self.advance()
                    if self.current_char == "a":
                        ident_str += self.current_char
                        
                        self.advance()
                        if self.current_char == "w":
                            ident_str += self.current_char
                            
                            self.advance()
                            if self.current_char == "k":
                                ident_str += self.current_char
                                
                                self.advance()
                                if self.current_char == "t":
                                    ident_str += self.current_char
                                    
                                    self.advance()
                                    if self.current_char == "u":
                                        ident_str += self.current_char
                                        
                                        self.advance()
                                        if self.current_char == "a":
                                            ident_str += self.current_char
                                            
                                            self.advance()
                                            if self.current_char == "h":
                                                ident_str += self.current_char
                                                
                                                self.advance()
                                                if self.current_char is not None and self.current_char in com_dlm:
                                                    tokens.append(Token(TT_RW_HAWKTUAH, ident_str, line))
                                                    continue
                                                elif self.current_char is not None and self.current_char not in com_dlm and self.current_char not in ALPHANUM:
                                                    errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                                                    continue
                                elif self.current_char is not None and self.current_char in hawk_dlm:
                                    tokens.append(Token(TT_RW_HAWK, ident_str, line))
                                    continue
                                elif self.current_char is not None and self.current_char not in hawk_dlm and self.current_char not in ALPHANUM:
                                    errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                                    continue

                                
                # Letter I
                if self.current_char == "i":
                    ident_str += self.current_char
                    
                    self.advance()
                    if self.current_char == "n":
                        ident_str += self.current_char
                        
                        self.advance()
                        if self.current_char == "s":
                            ident_str += self.current_char
                            
                            self.advance()
                            if self.current_char == "e":
                                ident_str += self.current_char
                                
                                self.advance()
                                if self.current_char == "r":
                                    ident_str += self.current_char
                                    
                                    self.advance()
                                    if self.current_char == "t":
                                        ident_str += self.current_char
                                        
                                        self.advance()
                                        if self.current_char is not None and self.current_char in com_dlm:
                                            tokens.append(Token(TT_RW_INSERT, ident_str, line))
                                            continue
                                        elif self.current_char is not None and self.current_char not in com_dlm and self.current_char not in ALPHANUM:
                                            errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                                            continue

                # Letter J
                if self.current_char == "j":
                    ident_str += self.current_char
                    
                    self.advance()
                    if self.current_char == "i":
                        ident_str += self.current_char
                        
                        self.advance()
                        if self.current_char == "t":
                            ident_str += self.current_char
                            
                            self.advance()
                            if self.current_char is None or self.current_char in com_dlm:
                                tokens.append(Token(TT_RW_JIT, ident_str, line))
                                continue
                            elif self.current_char is not None and self.current_char not in com_dlm and self.current_char not in ALPHANUM:
                                errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                                continue

                # Letter L
                if self.current_char == "l":
                    ident_str += self.current_char
                    
                    self.advance()
                    if self.current_char == "e":
                        ident_str += self.current_char
                        
                        self.advance()
                        if self.current_char == "t":
                            ident_str += self.current_char
                            
                            self.advance()
                            if self.current_char == "h":
                                ident_str += self.current_char
                                
                                self.advance()
                                if self.current_char == "i":
                                    ident_str += self.current_char
                                    
                                    self.advance()
                                    if self.current_char == "m":
                                        ident_str += self.current_char
                                        
                                        self.advance()
                                        if self.current_char == "c":
                                            ident_str += self.current_char
                                            
                                            self.advance()
                                            if self.current_char == "o":
                                                ident_str += self.current_char
                                                
                                                self.advance()
                                                if self.current_char == "o":
                                                    ident_str += self.current_char
                                                    
                                                    self.advance()
                                                    if self.current_char == "k":
                                                        ident_str += self.current_char
                                                        
                                                        self.advance()
                                                        if self.current_char is not None and self.current_char in com_dlm:
                                                            tokens.append(Token(TT_RW_LETHIMCOOK, ident_str, line))
                                                            continue
                                                        elif self.current_char is not None and self.current_char not in com_dlm and self.current_char not in ALPHANUM:
                                                            errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                                                            continue

                    if self.current_char == "i":
                        ident_str += self.current_char
                        
                        self.advance()
                        if self.current_char == "l":
                            ident_str += self.current_char
                            
                            self.advance()
                            if self.current_char is None or self.current_char in hawk_dlm:
                                tokens.append(Token(TT_RW_LIL, ident_str, line))
                                continue
                            elif self.current_char is not None and self.current_char not in hawk_dlm and self.current_char not in ALPHANUM:
                                errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                                continue
                        
                    if self.current_char == "w":
                        ident_str += self.current_char
                        
                        self.advance()
                        if self.current_char == "k":
                            ident_str += self.current_char
                            
                            self.advance()
                            if self.current_char is None or self.current_char in spc_dlm:
                                tokens.append(Token(TT_RW_LWK, ident_str, line))
                                continue
                            elif self.current_char is not None and self.current_char not in spc_dlm and self.current_char not in ALPHANUM:
                                errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                                continue

                # Letter N
                if self.current_char == "n":
                    ident_str += self.current_char
                    
                    self.advance()
                    if self.current_char == "o":
                        ident_str += self.current_char
                        
                        self.advance()
                        if self.current_char == "c":
                            ident_str += self.current_char
                            
                            self.advance()
                            if self.current_char == "a":
                                ident_str += self.current_char
                                
                                self.advance()
                                if self.current_char == "p":
                                    ident_str += self.current_char
                                    
                                    self.advance()
                                    if self.current_char is None or self.current_char in spc_dlm:
                                        tokens.append(Token(TT_RW_NOCAP, ident_str, line))
                                        continue
                                    elif self.current_char is not None and self.current_char not in spc_dlm and self.current_char not in ALPHANUM:
                                        errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                                        continue

                    if self.current_char == "p":
                        ident_str += self.current_char
                        
                        self.advance()
                        if self.current_char == "c":
                            ident_str += self.current_char
                            
                            self.advance()
                            if self.current_char is None or self.current_char in npc_dlm:
                                tokens.append(Token(TT_RW_NPC, ident_str, line))
                                continue
                            elif self.current_char is not None and self.current_char not in npc_dlm and self.current_char not in ALPHANUM:
                                errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                                continue
                        
                # Letter P
                if self.current_char == "p":
                    ident_str += self.current_char
                    
                    self.advance()
                    if self.current_char == "a":
                        ident_str += self.current_char
                        
                        self.advance()
                        if self.current_char == "u":
                            ident_str += self.current_char
                            
                            self.advance()
                            if self.current_char == "s":
                                ident_str += self.current_char
                                
                                self.advance()
                                if self.current_char == "e":
                                    ident_str += self.current_char
                                    
                                    self.advance()
                                    if self.current_char is None or self.current_char in endln_dlm:
                                        tokens.append(Token(TT_RW_PAUSE, ident_str, line))
                                        continue
                                    elif self.current_char is not None and self.current_char not in endln_dlm and self.current_char not in ALPHANUM:
                                        errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                                        continue

                    if self.current_char == "l":
                            ident_str += self.current_char
                            
                            self.advance()
                            if self.current_char == "u":
                                ident_str += self.current_char
                                
                                self.advance()
                                if self.current_char == "g":
                                    ident_str += self.current_char
                                    
                                    self.advance()
                                    if self.current_char is not None and self.current_char in com_dlm:
                                        tokens.append(Token(TT_RW_PLUG, ident_str, line))
                                        continue
                                    elif self.current_char is not None and self.current_char not in com_dlm and self.current_char not in ALPHANUM:
                                        errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                                        continue


                # Letter R
                if self.current_char == "r":
                    ident_str += self.current_char
                    
                    self.advance()
                    if self.current_char == "e":
                        ident_str += self.current_char
                        
                        self.advance()
                        if self.current_char == "m":
                            ident_str += self.current_char
                            
                            self.advance()
                            if self.current_char == "o":
                                ident_str += self.current_char
                                
                                self.advance()
                                if self.current_char == "v":
                                    ident_str += self.current_char
                                    
                                    self.advance()
                                    if self.current_char == "e":
                                        ident_str += self.current_char
                                        
                                        self.advance()
                                        if self.current_char is not None and self.current_char in com_dlm:
                                            tokens.append(Token(TT_RW_REMOVE, ident_str, line))
                                            continue
                                        elif self.current_char is not None and self.current_char not in com_dlm and self.current_char not in ALPHANUM:
                                            errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                                            continue

                # Letter S
                if self.current_char == "s":
                    ident_str += self.current_char
                    
                    self.advance()
                    if self.current_char == "k":
                        ident_str += self.current_char
                        
                        self.advance()
                        if self.current_char == "i":
                            ident_str += self.current_char
                            
                            self.advance()
                            if self.current_char == "b":
                                ident_str += self.current_char
                                
                                self.advance()
                                if self.current_char == "i":
                                    ident_str += self.current_char
                                    
                                    self.advance()
                                    if self.current_char == "d":
                                        ident_str += self.current_char
                                        
                                        self.advance()
                                        if self.current_char == "i":
                                            ident_str += self.current_char
                                            
                                            self.advance()
                                            if self.current_char is not None and self.current_char in hawk_dlm:
                                                tokens.append(Token(TT_RW_SKIBIDI, ident_str, line))
                                                continue
                                            elif self.current_char is not None and self.current_char not in hawk_dlm and self.current_char not in ALPHANUM:
                                                errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                                                continue

                    if self.current_char == "t":
                        ident_str += self.current_char
                        
                        self.advance()
                        if self.current_char == "u":
                            ident_str += self.current_char
                            
                            self.advance()
                            if self.current_char == "r":
                                ident_str += self.current_char
                                
                                self.advance()
                                if self.current_char == "d":
                                    ident_str += self.current_char
                                    
                                    self.advance()
                                    if self.current_char == "y":
                                        ident_str += self.current_char
                                        
                                        self.advance()
                                        if self.current_char is None or self.current_char in spc_dlm:
                                            tokens.append(Token(TT_RW_STURDY, ident_str, line))
                                            continue
                                        elif self.current_char is not None and self.current_char not in spc_dlm and self.current_char not in ALPHANUM:
                                            errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                                            continue


                # Letter T
                if self.current_char == "t":
                    ident_str += self.current_char
                    
                    self.advance()
                    if self.current_char == "a":
                        ident_str += self.current_char
                        
                        self.advance()
                        if self.current_char == "p":
                            ident_str += self.current_char
                            
                            self.advance()
                            if self.current_char == "e":
                                ident_str += self.current_char
                                
                                self.advance()
                                if self.current_char == "r":
                                    ident_str += self.current_char
                                    
                                    self.advance()
                                    if self.current_char is None or self.current_char in com_dlm:
                                        tokens.append(Token(TT_RW_TAPER, ident_str, line))
                                        continue
                                    elif self.current_char is not None and self.current_char not in com_dlm and self.current_char not in ALPHANUM:
                                        errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                                        continue

                    if self.current_char == "r":
                        ident_str += self.current_char
                        
                        self.advance()
                        if self.current_char == "u":
                            ident_str += self.current_char
                            
                            self.advance()
                            if self.current_char == "e":
                                ident_str += self.current_char
                                
                                self.advance()
                                if self.current_char is None or self.current_char in lwk_dlm:
                                    tokens.append(Token(TT_LWK, ident_str, line))
                                    continue
                                elif self.current_char is not None and self.current_char not in lwk_dlm and self.current_char not in ALPHANUM:
                                    errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                                    continue

                    if self.current_char == 's':
                        ident_str += self.current_char
                        
                        self.advance()
                        if self.current_char is None or self.current_char in com_dlm:
                            tokens.append(Token(TT_RW_TS, ident_str, line))
                            continue
                        elif self.current_char is not None and self.current_char not in com_dlm and self.current_char not in ALPHANUM:
                            errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                            continue

                    if self.current_char == "u":
                        ident_str += self.current_char
                        
                        self.advance()
                        if self.current_char == "a":
                            ident_str += self.current_char
                            
                            self.advance()
                            if self.current_char == "h":
                                ident_str += self.current_char
                                
                                self.advance()
                                if self.current_char is None or self.current_char in com_dlm:
                                    tokens.append(Token(TT_RW_TUAH, ident_str, line))
                                    continue
                                elif self.current_char is not None and self.current_char not in com_dlm and self.current_char not in ALPHANUM:
                                    errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                                    continue

                # Letter Y
                if self.current_char == "y":
                    ident_str += self.current_char
                    
                    self.advance()
                    if self.current_char == "a":
                        ident_str += self.current_char
                        
                        self.advance()
                        if self.current_char == "p":
                            ident_str += self.current_char
                            
                            self.advance()
                            if self.current_char is not None and self.current_char in com_dlm:
                                tokens.append(Token(TT_RW_YAP, ident_str, line))
                                continue
                            elif self.current_char is not None and self.current_char not in com_dlm and self.current_char not in ALPHANUM:
                                errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                                continue

                #Identifier            
                maxIdentifierLength = 20
                while self.current_char is not None and self.current_char in ALPHANUM + "_":
                    if len(ident_str) + 1 > maxIdentifierLength:
                        errors.append(LexicalError(pos, f"Identifier '{ident_str}' exceeds maximum length of {maxIdentifierLength} characters."))
                        break
                    ident_str += self.current_char
                    self.advance()

                if len(ident_str) <= maxIdentifierLength:
                    if self.current_char is None or self.current_char in identif_dlm:
                        tokens.append(Token(TT_IDENTIFIER, ident_str, line))
                        continue

                    elif self.current_char is not None and self.current_char not in identif_dlm and self.current_char not in ALPHANUM:
                        errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                        continue

                else:
                    continue

            
            elif self.current_char == "-":
                ident_str = self.current_char
                pos = self.pos.copy()
                self.advance()
                if self.current_char in ALPHANUM or self.current_char == "(":
                    tokens.append(Token(TT_NEGAT, ident_str, line))
                    continue
                elif self.current_char == "-":
                    ident_str += self.current_char
                    self.advance()
                    if self.current_char is None or self.current_char in unary_dlm:
                        tokens.append(Token(TT_DEC, ident_str, line))
                        continue
                    else:
                        errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                        self.advance()
                        continue
                elif self.current_char is not None and self.current_char in minus_dlm:
                    tokens.append(Token(TT_MINUS, ident_str, line))
                    continue
                else:
                    errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                    continue
            
            elif self.current_char == "!":
                ident_str = self.current_char
                pos = self.pos.copy()
                self.advance()
                if self.current_char == "=":
                    ident_str += self.current_char
                    self.advance()
                    if self.current_char is not None and self.current_char in relat_dlm:
                        tokens.append(Token(TT_NEQ, ident_str, line))
                        continue
                    else:
                        errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                        continue
                elif self.current_char is not None and self.current_char in not_dlm:
                    tokens.append(Token(TT_NOT, ident_str, line))
                    continue
                else:
                    errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                    continue

                
            
            elif self.current_char == "%":
                ident_str = self.current_char
                pos = self.pos.copy()
                self.advance()
                if self.current_char is not None and self.current_char in arith_operator_dlm:
                    tokens.append(Token(TT_MOD, ident_str, line))
                    continue
                else:
                    errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                    continue
    
            elif self.current_char == "&":
                ident_str = self.current_char
                pos = self.pos.copy()
                self.advance()
                if self.current_char == "&":
                    ident_str += self.current_char
                    self.advance()
                    if self.current_char is not None and self.current_char in operator_dlm:
                        tokens.append(Token(TT_AND, ident_str, line))
                        continue
                    else:
                        errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                        continue
                else:
                    errors.append(LexicalError(pos, f"Invalid character '{ident_str}'"))
                    self.advance()
                    continue
                    
            elif self.current_char == "(":
                ident_str = self.current_char
                pos = self.pos.copy()
                self.advance()
                if self.current_char is not None and self.current_char in oppar_dlm:
                    tokens.append(Token(TT_OPPAR, ident_str, line))
                    continue
                else:
                    errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                    continue
                
            elif self.current_char == ")":
                ident_str = self.current_char
                pos = self.pos.copy()
                self.advance()
                if self.current_char is None or self.current_char in clpar_dlm:
                    tokens.append(Token(TT_CLPAR, ident_str, line))
                    continue
                else:
                    errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                    continue
                
            elif self.current_char == "*":
                ident_str = self.current_char
                pos = self.pos.copy()
                self.advance()
                if self.current_char is None or self.current_char in arith_operator_dlm:
                    tokens.append(Token(TT_MUL, ident_str, line))
                    continue
                else:
                    errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                    continue
                
            elif self.current_char == ",":
                ident_str = self.current_char
                pos = self.pos.copy()
                self.advance()
                if self.current_char is not None and self.current_char in comma_dlm:
                    tokens.append(Token(TT_COMMA, ident_str, line))
                    continue
                else:
                    errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                    continue
            
            elif self.current_char == "\\":
                ident_str = self.current_char
                pos = self.pos.copy()
                self.advance()
                if self.current_char == "\"":
                    ident_str += self.current_char
                    self.advance()
                    if self.current_char is None or self.current_char in esc_dlm:
                        tokens.append(Token(TT_ESCAPESEQUENCE, ident_str, line))
                        continue
                    else:
                        errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                        continue
                elif self.current_char == "/":
                    ident_str += self.current_char
                    self.advance()
                    if self.current_char is None or self.current_char in esc_dlm:
                        tokens.append(Token(TT_ESCAPESEQUENCE, ident_str, line))
                        continue
                    else:
                        errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                        continue
                elif self.current_char == "{":
                    ident_str += self.current_char
                    self.advance()
                    if self.current_char is None or self.current_char in esc_dlm:
                        tokens.append(Token(TT_ESCAPESEQUENCE, ident_str, line))
                        continue
                    else:
                        errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                        continue
                elif self.current_char == "}":
                    ident_str += self.current_char
                    self.advance()
                    if self.current_char is None or self.current_char in esc_dlm:
                        tokens.append(Token(TT_ESCAPESEQUENCE, ident_str, line))
                        continue
                    else:
                        errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                        continue
                elif self.current_char == "n":
                    ident_str += self.current_char
                    self.advance()
                    if self.current_char is None or self.current_char in esc_dlm:
                        tokens.append(Token(TT_ESCAPESEQUENCE, ident_str, line))
                        continue
                    else:
                        errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                        continue
                elif self.current_char == "t":
                    ident_str += self.current_char
                    self.advance()
                    if self.current_char is None or self.current_char in esc_dlm:
                        tokens.append(Token(TT_ESCAPESEQUENCE, ident_str, line))
                        continue
                    else:
                        errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                        continue
                else:
                    errors.append(LexicalError(pos, f"Invalid character '{ident_str}'"))
                    self.advance()
                    continue    
                
            elif self.current_char == ";":
                ident_str = self.current_char
                pos = self.pos.copy()
                self.advance()
                if self.current_char is not None and self.current_char in scolon_dlm:
                    tokens.append(Token(TT_SEMICOL, ident_str, line))
                    continue
                else:
                    errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                    continue
                
            elif self.current_char == "[":
                ident_str = self.current_char
                pos = self.pos.copy()
                self.advance()
                if self.current_char is not None and self.current_char in opbra_dlm:
                    tokens.append(Token(TT_OPBRA, ident_str, line))
                    continue
                else:
                    errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                    continue
                
            elif self.current_char == "]":
                ident_str = self.current_char
                pos = self.pos.copy()
                self.advance()
                if self.current_char is None or self.current_char in clbra_dlm:
                    tokens.append(Token(TT_CLBRA, ident_str, line))
                    continue
                else:
                    errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                    continue
                
            elif self.current_char == "{":
                ident_str = self.current_char
                pos = self.pos.copy()
                self.advance()
                if self.current_char is not None and self.current_char in opcur_dlm:
                    tokens.append(Token(TT_OPCUR, ident_str, line))
                    continue
                else:
                    errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                    continue
                
            elif self.current_char == "}":
                ident_str = self.current_char 
                pos = self.pos.copy() 
                self.advance()
                if self.current_char is None or self.current_char in clcur_dlm:
                    tokens.append(Token(TT_CLCUR, ident_str, line))
                    continue
                else: 
                    errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                    continue

            elif self.current_char == "|":
                ident_str = self.current_char
                pos = self.pos.copy()
                self.advance()
                if self.current_char == "|":
                    ident_str += self.current_char
                    self.advance()
                    if self.current_char is not None and self.current_char in operator_dlm:
                        tokens.append(Token(TT_OR, ident_str, line))
                        continue
                    else:
                        errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                        continue
                else:
                    errors.append(LexicalError(pos, f"Invalid character '{ident_str}'"))
                    self.advance()
                    continue
            
            elif self.current_char == "+":
                ident_str = self.current_char
                pos = self.pos.copy()
                self.advance()
                if self.current_char == "+":
                    ident_str += self.current_char
                    self.advance()
                    if self.current_char is None or self.current_char in unary_dlm:
                        tokens.append(Token(TT_INC, ident_str, line))
                        continue
                    else:
                        errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                        continue
                elif self.current_char is not None and self.current_char in plus_dlm:
                    tokens.append(Token(TT_PLUS, ident_str, line))
                    continue
                else:
                    errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                    continue

            elif self.current_char == "<":
                ident_str = self.current_char
                pos = self.pos.copy()
                self.advance()
                if self.current_char == "=":
                    ident_str += self.current_char
                    self.advance()
                    if self.current_char is not None and self.current_char in arith_operator_dlm:
                        tokens.append(Token(TT_LTE, ident_str, line))
                        continue
                    else:
                        errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                        continue
                elif self.current_char is not None and self.current_char in arith_operator_dlm:
                    tokens.append(Token(TT_LT, ident_str, line))
                    continue
                else:
                    errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                    continue
            
            elif self.current_char == "=":
                ident_str = self.current_char
                pos = self.pos.copy()
                self.advance()
                if self.current_char == "=":
                    ident_str += self.current_char
                    self.advance()
                    if self.current_char is not None and self.current_char in relat_dlm:
                        tokens.append(Token(TT_EQ, ident_str, line))
                        continue
                    else:
                        errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                        continue
                elif self.current_char is not None and self.current_char in equal_dlm:
                    tokens.append(Token(TT_IS, ident_str, line))
                    continue
                else:
                    errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                    continue

            elif self.current_char == ">":
                ident_str = self.current_char
                pos = self.pos.copy()
                self.advance()
                if self.current_char == "=":
                    ident_str += self.current_char
                    self.advance()
                    if self.current_char is not None and self.current_char in arith_operator_dlm:
                        tokens.append(Token(TT_GTE, ident_str, line))
                        continue
                    else:
                        errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                        continue
                elif self.current_char is not None and self.current_char in arith_operator_dlm:
                    tokens.append(Token(TT_GT, ident_str, line))
                    continue
                else:
                    errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                    continue


            elif self.current_char == '\n':
                pos = self.pos.copy()
                if tokens and tokens[-1].type != TT_NL:
                    tokens.append(Token(TT_NL, "\\n", line))

                while self.current_char == '\t' or self.current_char == ' ' or self.current_char == '\n':
                    if self.current_char == '\t' or self.current_char == ' ':
                        self.advance()
                    else:
                        line += 1
                        self.advance()

                continue
                
            elif self.current_char == '\t':
                ident_str = self.current_char
                pos = self.pos.copy()
                while self.current_char == '\t':
                    self.advance()
                
            elif self.current_char == ' ':
                ident_str = self.current_char
                pos = self.pos.copy()
                self.advance()
                while self.current_char == ' ':
                    self.advance()

            elif self.current_char == "/":
                ident_str = self.current_char
                pos = self.pos.copy()
                self.advance()
                if self.current_char == "/":
                    ident_str += self.current_char
                    self.advance()
                    while self.current_char is not None and self.current_char != "\n":
                        ident_str += self.current_char
                        self.advance()
                    #tokens.append(Token(TT_COMMENT, ident_str, line))
                    continue
                elif self.current_char == "*":
                    ident_str += self.current_char
                    self.advance()
                    while self.current_char is not None:
                        if self.current_char == "*" and self.source_code[self.pos.index + 1] == "/":
                            ident_str += "*/"
                            self.advance()
                            self.advance()
                            break
                        else:
                            ident_str += self.current_char
                            if self.current_char == "\n":
                                line += 1
                            self.advance()
                    #tokens.append(Token(TT_COMMENT, ident_str, line))
                    if self.current_char is None:
                        errors.append(LexicalError(pos, f"Missing closing '*/' after '{ident_str}'"))
                        continue
                    continue    
                elif self.current_char is not None and self.current_char in arith_operator_dlm:
                    tokens.append(Token(TT_DIV, ident_str, line))
                    continue
                else:
                    errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{string}'"))
                    continue
            
            elif self.current_char == ".":
                ident_str = self.current_char
                pos = self.pos.copy()
                self.advance()
                if self.current_char is not None and self.current_char in ALPHA:
                    tokens.append(Token(TT_DOT, ident_str, line))
                    continue

                elif self.current_char is not None and self.current_char in NUM:
                    fractional_part = ""
                    while self.current_char in NUM:
                        if len(fractional_part + self.current_char) > 5:
                            errors.append(LexicalError(pos, f"'{ident_str}' exceeds maximum number of decimal places"))
                            break

                        fractional_part += self.current_char
                        self.advance()

                        
                    ident_str = f"0.{fractional_part}"
                    tokens.append(Token(TT_CHUDELUXE, ident_str, line))
                    continue
                else:
                    errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                    self.advance()
                    continue
            
            elif self.current_char == ":":
                ident_str = self.current_char
                pos = self.pos.copy()
                self.advance()
                if self.current_char is None or self.current_char in endln_dlm:
                    tokens.append(Token(TT_COL, ident_str, line))
                    continue
                else:
                    errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                    continue

            elif self.current_char in NUM:

                dot_count = 0
                ident_str = ""
                pos = self.pos.copy()
                digitCount = 0

                while self.current_char is not None and self.current_char in NUM + ".":
                    if self.current_char == ".":
                        digitCount = 10
                        if dot_count == 1:
                            break
                        dot_count += 1

                    digitCount += 1
                    if digitCount > 16:
                        break
                    ident_str += self.current_char
                    if digitCount <= 16:
                        self.advance()

                if dot_count == 0: 
                    ident_str = ident_str.lstrip("0") or "0"
                    if digitCount > 16: 
                        errors.append(LexicalError(pos, f"'{ident_str}' exceeds maximum number of characters"))
                        continue
                    
                    if self.current_char is None or self.current_char in lit_dlm:
                        tokens.append(Token(TT_CHUNGUS, ident_str, line))
                        continue
                    else:
                        errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                        continue
                    
                    
                else:  # Float case
                    parts = ident_str.split(".")
                    integer_part = parts[0].lstrip("0") or "0"
                    fractional_part = parts[1].rstrip("0") or "0"
                    ident_str = f"{integer_part}.{fractional_part}"

                    if digitCount > 16:
                        errors.append(LexicalError(pos, f"'{ident_str}' exceeds maximum number of characters"))
                        continue

                    if self.current_char is None or self.current_char in lit_dlm:
                        tokens.append(Token(TT_CHUDELUXE, ident_str, line))
                        continue
                    else:
                        errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                        continue

            elif self.current_char == '"':
                string = ''
                pos = self.pos.copy()
                escape_character = False
                string += self.current_char
                self.advance()

                escape_characters = {
                    'n': '\n',
                    't': '\t',
                    '{': '\\{',
                    '}': '\\}'
                }

                while self.current_char is not None and (self.current_char != '"' or escape_character):
                    if escape_character:
                        string += escape_characters.get(self.current_char, self.current_char)
                        escape_character = False
                    else:
                        if self.current_char == '\\':
                            escape_character = True
                        elif self.current_char == '\n':
                            break
                        else:
                            string += self.current_char
                    self.advance()

                if self.current_char == '"':
                    string += self.current_char
                    self.advance()

                else:
                    errors.append(LexicalError(pos, f"Missing closing '\"' after '{string}'"))
                    continue

                if self.current_char is not None and self.current_char not in lit_dlm:
                    errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after string literal '{string}'"))
                    continue
            
                string = string.replace('\n', '\\n')
                tokens.append(Token(TT_FORSENCD, string, line))
                continue
    
            elif self.current_char == "'":
                string = ''
                char = ''
                pos = self.pos.copy()
                string += self.current_char
                self.advance()

                while self.current_char is not None and self.current_char != "'":
                    if self.current_char == '\n':
                        break
                    elif self.current_char == '\\':
                        break
                    else:
                        string += self.current_char
                        char += self.current_char
                    self.advance()

                if self.current_char == "'":
                    string += self.current_char
                    self.advance()
                    
                else:
                    errors.append(LexicalError(pos, f"Missing closing '\'' after '{string}'"))
                    continue

                if len(char) > 1:
                    errors.append(LexicalError(pos, f"Character literal '{string}' exceeds maximum length of 1 character."))
                    continue

                if self.current_char is not None and self.current_char not in lit_dlm:
                    errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{string}'"))
                    continue

                tokens.append(Token(TT_FORSEN, string, line))
                continue

            else:
                pos = self.pos.copy()
                char = self.current_char
                self.advance()
                errors.append(LexicalError(pos, f"Invalid character '" + char + "'"))
                self.advance()
                continue
                
        if self.current_char is None:
            tokens.append(Token(TT_EOF, "", line))
        return tokens, errors

    
def run(source_code):
    lexer = Lexer(source_code)
    tokens, error = lexer.make_tokens()
    return tokens, error