from flask import Flask, request, jsonify
from flask_cors import CORS
from cgmalexer import Lexer
from cfg import cfg, predict_sets

app = Flask(__name__)
CORS(app)

class LL1Parser:
    def __init__(self, cfg, predict_sets):
        self.cfg = cfg
        self.predict_sets = predict_sets
        self.parsing_table = self.construct_parsing_table()
        self.stack = []
        self.tokens = []
        self.current_token_index = 0

    def construct_parsing_table(self):
        """Builds the LL(1) parsing table based on predict sets."""
        parsing_table = {}
        for non_terminal, productions in self.cfg.items():
            parsing_table[non_terminal] = {}
            for production in productions:
                predict_key = (non_terminal, tuple(production))
                if predict_key in self.predict_sets:
                    for terminal in self.predict_sets[predict_key]:
                        parsing_table[non_terminal][terminal] = production
        return parsing_table

    def get_next_token(self):
        """Advances to the next token."""
        if self.current_token_index < len(self.tokens):
            token = self.tokens[self.current_token_index]
            self.current_token_index += 1
            return token
        return None

    def parse(self, tokens):
        self.stack = ['EOF', list(self.cfg.keys())[0]]  # Start symbol on stack
        index = 0
        line = 1
        error_messages = []
        
        while self.stack:
            top = self.stack.pop()
            token = tokens[index]
            token_type = token.type  # Token type from lexer
            token_value = token.value  # Token value from lexer

            # Skip whitespace and newlines
            while token_type in {'SPC', 'NL', 'TAB', 'COMMENT'}:
                if token_type == 'NL':
                    line += 1
                elif token_type == 'COMMENT' and '\n' in token_value:
                    line += 1
                index += 1
                token = tokens[index]
                token_type = token.type
                token_value = token.value

            if token_value == 'chungus' and index + 1 < len(tokens) and tokens[index + 1].value == 'skibidi':
                token_value = 'chungus skibidi'
                token_type = 'chungus skibidi'

            # Normalize identifiers
            if token_type in {"IDENTIFIER", "CHUNGUS_LIT", "CHUDELUXE_LIT", "FORSEN_LIT", "FORSENCD_LIT"}:
                pass  # Keep their token_type
            elif token_value in {'true', 'false'}:
                token_type = 'LWK_LIT'
            elif token_value in self.parsing_table.get(top, {}):  
                token_type = token_value  # Match literal tokens directly

            print(f"\nStack Top: {top}, Token Type: {token_type}, Token Value: {token_value}")

            if token_type == 'TT_NL':
                line += 1
            
            # If top of stack matches the current token (terminal match)
            if top == token_type or top == token_value:
                print(f"Matched: {top}")
                if top == 'chungus skibidi':
                    index += 2
                else:
                    index += 1  # Move to the next token
            
            # If top of stack is a non-terminal and exists in the parsing table
            elif top in self.parsing_table:
                if token_type in self.parsing_table[top]:
                    production = self.parsing_table[top][token_type]
                    print(f"Expand: {top} → {' '.join(production)}")
                    
                    if production != ['λ']:  # Ignore epsilon (λ)
                        self.stack.extend(reversed(production))  # Push in reverse order
                    print(f"Updated Stack: {self.stack}")
                else:
                    expected_tokens = list(self.parsing_table[top].keys())
                    error_message = f"Ln {line} Syntax Error: Unexpected token '{token_value}'. Expected one of: {expected_tokens}"
                    print(error_message)
                    error_messages.append(error_message)
                    return False, error_messages
            
            # If stack top is a terminal but does not match token, error
            else:
                error_message = f"Ln {line} Syntax Error: Unexpected token '{token_value}'. Expected: '{top}'"
                print(error_message)
                error_messages.append(error_message)
                return False, error_messages
        
        # Ensure successful parsing if EOF is reached and stack is empty
        if token_type == 'EOF' and not self.stack:
            print("Parsing successful!")
            return True, []
        else:
            print("Error: Tokens remaining after parsing")
            return False, ["Error: Tokens remaining after parsing"]

@app.route('/api/parse', methods=['POST'])
def parse():
    data = request.json
    source_code = data.get('source_code', '')
    lexer = Lexer('<stdin>', source_code)
    tokens, errors = lexer.make_tokens()

    if errors:
        return jsonify({'success': False, 'errors': [error.as_string() for error in errors]})

    parser = LL1Parser(cfg, predict_sets)
    success, parse_errors = parser.parse(tokens)

    return jsonify({'success': success, 'errors': parse_errors})


if __name__ == '__main__':
    handler = app