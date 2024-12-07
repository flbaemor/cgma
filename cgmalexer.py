#CONSTANTS

ALPHA_LOWER = 'abcdefghijklmnopqrstuvwxyz'
ALPHA_UPPER = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
ALPHA = ALPHA_LOWER + ALPHA_UPPER
ZERO = '0'
DIGITS = '123456789'
NUM = ZERO + DIGITS
ALPHANUM = ALPHA + NUM
PUNCTUATIONS = '!@#$%^&*()-_=+[]}{\|:;’”,<>.?/ '
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

#ERROR

class Error:
    def __init__(self, error_name, details):
        self.error_name = error_name
        self.details = details

    def as_string(self):
        result = f'{self.error_name}: {self.details}'
        return result
    
class IllegalCharError(Error):
    def __init__(self, details):
        super().__init__('Illegal Character', details)

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

class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

    def __repr__(self):
        if self.value: return f'{self.type}:{self.value}'  
        return f'{self.type}'
    

#LEXER

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = -1
        self.current_char = None
        self.advance()

    def advance(self):
        self.pos +=1
        self.current_char = self.text[self.pos] if self.pos<len(self.text) else None

    def make_tokens(self):
        tokens = []
        
        while self.current_char != None:
            if self. current_char in ' \t':
                self.advance()
            elif self.current_char in NUM:
                tokens.append(self.make_number())
            elif self.current_char == '+':
                tokens.append(Token(TT_PLUS))
                self.advance()
            elif self.current_char == '-':
                tokens.append(Token(TT_MINUS))
                self.advance()
            elif self.current_char == '*':
                tokens.append(Token(TT_MUL))
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token(TT_DIV))
                self.advance()
            elif self.current_char == '%':
                tokens.append(Token(TT_MOD))
                self.advance()
            elif self.current_char == '=':
                tokens.append(Token(TT_IS))
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token(TT_OPPAR))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(TT_CLPAR))
                self.advance()
            elif self.current_char in ALPHA:
                ident_str = ''
                ident_count = 0
                pos_start = self.pos.copy()

                if self.current_char == 'c':
                    ident_str += self.current_char
                    ident_count+=1
                    self.advance()
                    if self.current_char == 'h':
                        ident_str += self.current_char
                        ident_count+=1
                        self.advance()
                        if self.current_char == 'u':
                            ident_str += self.current_char
                            ident_count+=1
                            self.advance()
                            if self.current_char == 'n':
                                ident_str += self.current_char
                                ident_count+=1
                                self.advance()
                                if self.current_char == 'g':
                                    ident_str += self.current_char
                                    ident_count+=1
                                    self.advance()
                                    if self.current_char == 'u':
                                        ident_str += self.current_char
                                        ident_count+=1
                                        self.advance()
                                        if self.current_char == 's':
                                            ident_str += self.current_char
                                            ident_count+=1
                                            self.advance()
        
            else:
                char = self.current_char
                self.advance()
                return[], IllegalCharError("'" + char + "'")

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
        
def run(text):
    lexer = Lexer(text)
    tokens, error = lexer.make_tokens()

    return tokens, error