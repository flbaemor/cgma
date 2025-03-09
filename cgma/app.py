from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from cgmalexer import run as lexer_run
from cgmaparser import LL1Parser
from cgmaparser import SemanticAnalyzer
from cfg import cfg, predict_sets
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return send_from_directory(os.path.dirname(__file__), 'index.html')

@app.route('/style.css')
def style():
    return send_from_directory(os.path.dirname(__file__), 'style.css')

@app.route('/main.js')
def script():
    return send_from_directory(os.path.dirname(__file__), 'main.js')

@app.route('/api/lex', methods=['POST'])
def lex():
    data = request.json
    source_code = data.get('source_code', '')
    tokens, errors = lexer_run('<stdin>', source_code)
    return jsonify({'tokens': [{'type': token.type, 'value': token.value} for token in tokens], 'errors': [error.as_string() for error in errors]})

@app.route('/api/parse', methods=['POST'])
def parse():
    data = request.json
    source_code = data.get('source_code', '')
    tokens, errors = lexer_run('<stdin>', source_code)
    if errors:
        return jsonify({'success': False, 'errors': [error.as_string() for error in errors]})

    parser = LL1Parser(cfg, predict_sets)
    success, parse_errors = parser.parse(tokens)
    if not success:
        return jsonify({'success': False, 'errors': parse_errors})
    return jsonify({'success': True, 'errors': []})

@app.route('/api/semantic', methods=['POST'])
def semantic():
    data = request.json
    source_code = data.get('source_code', '')

    tokens, errors = lexer_run('<stdin>', source_code)
    if errors:
        return jsonify({'success': False, 'errors': [error.as_string() for error in errors]})

    
    parser = LL1Parser(cfg, predict_sets)
    success, parse_errors = parser.parse(tokens)
    if not success:
        return jsonify({'success': False, 'errors': parse_errors})

    semantic_analyzer = SemanticAnalyzer()
    semantic_errors = semantic_analyzer.analyze(tokens)
    if semantic_errors:
        return jsonify({'success': False, 'errors': semantic_errors})

    return jsonify({'success': True, 'errors': []})

if __name__ == '__main__':
    app.run(debug=True)