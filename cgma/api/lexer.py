from flask import Flask, request, jsonify
from cgmalexer import run as lexer_run

app = Flask(__name__)

@app.route('/api/lexer', methods=['POST'])
def lexer_handler():
    body = request.get_json()
    source_code = body.get('source_code', '')

    tokens, errors = lexer_run('<stdin>', source_code)

    response = {
        'tokens': [{'type': token.type, 'value': token.value} for token in tokens],
        'errors': [error.as_string() for error in errors]
    }

    return jsonify(response)

# Vercel expects 'app' as the entry point
handler = app
