from flask import Flask, request, jsonify
from cgmaparsery import LL1Parser
from cfg import cfg, predict_sets
from cgmalexer import run as lexer_run

app = Flask(__name__)

@app.route('/api/parser', methods=['POST'])
def parser_handler():
    body = request.get_json()
    source_code = body.get('source_code', '')

    tokens, errors = lexer_run('<stdin>', source_code)

    if errors:
        return jsonify({'success': False, 'errors': [error.as_string() for error in errors]})

    parser = LL1Parser(cfg, predict_sets)
    success, parse_errors = parser.parse(tokens)

    return jsonify({'success': success, 'errors': parse_errors})

# Vercel expects 'app' as the entry point
handler = app
