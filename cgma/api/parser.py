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
        self.stack = ['EOF', list(self.cfg.keys())[0]]  # Start symbol
        index = 0
        line = 1
        errors = []

        while self.stack:
            top = self.stack.pop()
            token = tokens[index]
            token_type = token.type
            token_value = token.value

            # Skip whitespace
            while token_type in {'SPC', 'NL', 'TAB', 'COMMENT'}:
                if token_type == 'NL':
                    line += 1
                index += 1
                token = tokens[index]
                token_type = token.type
                token_value = token.value

            if top == token_type or top == token_value:
                index += 1  # Match found, move to next token
            elif top in self.parsing_table and token_type in self.parsing_table[top]:
                production = self.parsing_table[top][token_type]
                if production != ['λ']:  # Ignore epsilon
                    self.stack.extend(reversed(production))
            else:
                errors.append(f"Ln {line} Syntax Error: Unexpected token '{token_value}'. Expected: '{top}'")
                return False, errors

        return (True, []) if token_type == 'EOF' and not self.stack else (False, ["Syntax Error: Incomplete parsing"])

@app.route('/api/parser', methods=['POST'])
def parser_handler():
    data = request.json
    source_code = data.get('source_code', '')
    lexer = Lexer('<stdin>', source_code)
    tokens, errors = lexer.make_tokens()

    if errors:
        return jsonify({'success': False, 'errors': [error.as_string() for error in errors]})

    parser = LL1Parser(cfg, predict_sets)
    success, parse_errors = parser.parse(tokens)

    return jsonify({'success': success, 'errors': parse_errors})

# Required for Vercel
handler = app
