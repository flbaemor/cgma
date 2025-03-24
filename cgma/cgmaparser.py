from flask import Flask, request, jsonify
from flask_cors import CORS
from cgmalexer import Lexer
from cfg import cfg, predict_sets

app = Flask(__name__)
CORS(app)

# LL(1) Parser Class
class LL1Parser:
    def __init__(self, cfg, predict_sets):
        self.cfg = cfg
        self.predict_sets = predict_sets
        self.parsing_table = self.construct_parsing_table()
        self.stack = []
        self.tokens = []
        self.current_token_index = 0

    def construct_parsing_table(self):
        parsing_table = {}
        for non_terminal, productions in self.cfg.items():
            parsing_table[non_terminal] = {}
            for production in productions:
                predict_key = (non_terminal, tuple(production))
                if predict_key in self.predict_sets:
                    for terminal in self.predict_sets[predict_key]:
                        parsing_table[non_terminal][terminal] = production
        return parsing_table

    def parse(self, tokens):
        self.stack = ['EOF', list(self.cfg.keys())[0]]  # Initialize stack
        index = 0
        error_messages = []

        while self.stack:
            top = self.stack.pop()
            token = tokens[index]
            token_type = token.type  
            token_value = token.value  
            line = token.line

            while token_type in {'SPC', 'TAB', 'COMMENT'}:
                index += 1
                token = tokens[index]
                token_type = token.type
                token_value = token.value

            if token_type in {"IDENTIFIER", "CHU_LIT", "CHUDEL_LIT", "FORSEN_LIT", "FORSENCD_LIT"}:
                pass

            elif token_value in self.parsing_table.get(top, {}):
                token_type = token_value 

            #print(f"\nStack Top: {top}, Token Type: {token_type}, Token Value: {token_value}")


            if top == token_type or top == token_value:
                #print(f"Matched: {top}")
                index += 1  
            elif top in self.parsing_table:
                if token_type in self.parsing_table[top]:
                    production = self.parsing_table[top][token_type]
                    #print(f"Expand: {top} → {' '.join(production)}")
                    if production != ['ε']:
                        self.stack.extend(reversed(production))
                    #print(f"Updated Stack: {self.stack}")
                else:
                    expected_tokens = list(set(self.parsing_table[top].keys()) - {'$', 'ε'})
                    error_message = f"Ln {line} Syntax Error: Unexpected token '{token_value}'. Expected one of: {expected_tokens}"
                    #print(error_message)
                    error_messages.append(error_message)
                    return False, error_messages
            else:
                error_message = f"Ln {line} Syntax Error: Unexpected token '{token_value}'. Expected: '{top}'"
                #print(error_message)
                error_messages.append(error_message)
                return False, error_messages

        if token_type == 'EOF' and not self.stack:
            #print("\nSyntax analysis successful!")
            return True, []
        else:
            #print("Error: Tokens remaining after parsing")
            return False, ["Error: Tokens remaining after parsing"]
