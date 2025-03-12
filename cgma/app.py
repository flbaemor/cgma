from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from cgmalexer import run as lexer_run
from cgmaparser import LL1Parser
from cfg import cfg, predict_sets
from cgmasemantic import SemanticAnalyzer
import os

from cgmasemantic import build_ast
from cgmasemantic import SemanticError
from cgmasemantic import symbol_table
from cgmasemantic import SymbolTable

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
def semantic_analysis():
    print("\n🚀 DEBUG: semantic_analysis() called!\n")  # ✅ Confirms request is called once

    data = request.json
    source_code = data.get('source_code', '')

    global symbol_table
    symbol_table = SymbolTable()

    tokens, errors = lexer_run('<stdin>', source_code)
    if errors:
        return jsonify({'success': False, 'errors': [error.as_string() for error in errors]})

    parser = LL1Parser(cfg, predict_sets)
    success, ast_root = parser.parse(tokens)

    if not success:
        return jsonify({'success': False, 'errors': ['Syntax errors found']})

    try:
        ast_root = build_ast(tokens)  
        print("\n🚀 DEBUG: build_ast() finished!\n")  # ✅ AST completed
        ast_root.print_tree()

        semantic_analyzer = SemanticAnalyzer(symbol_table)  
        print("\n🚀 DEBUG: Running analyze()...\n")  # ✅ Check when analyze() starts
        semantic_analyzer.analyze(ast_root)  

        print("\n🚀 DEBUG: analyze() FINISHED!\n")  # ✅ Should print once
        return jsonify({'success': True, 'message': 'Semantic analysis completed successfully'})

    except SemanticError as e:
        return jsonify({'success': False, 'errors': [str(e)]})

if __name__ == '__main__':
    app.run(debug=False)