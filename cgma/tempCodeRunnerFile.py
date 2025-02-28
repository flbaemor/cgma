@app.route('/api/lex', methods=['POST'])
def lex():
    data = request.json
    source_code = data.get('source_code', '')
    tokens, errors = lexer_run('<stdin>', source_code)
    return jsonify({'tokens': [{'type': token.type, 'value': token.value} for token in tokens], 'errors': [error.as_string() for error in errors]})