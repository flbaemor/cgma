from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from cgmalexer import run as lexer_run
from cgmaparser import LL1Parser
from cfg import cfg, predict_sets, first_sets
import os

from cgmasemantic import build_ast
from cgmasemantic import SemanticError


from cgmainterpreter import Interpreter
from cgmainterpreter import InterpreterError

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app)

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
    tokens, errors = lexer_run(source_code)
    return jsonify({'tokens': [{'type': token.type, 'value': token.value} for token in tokens], 'errors': [error.as_string() for error in errors]})


@app.route('/api/parse', methods=['POST'])
def parse():
    data = request.json
    source_code = data.get('source_code', '')
    tokens, errors = lexer_run(source_code)
    if errors:
        errors = [error.as_string() for error in errors]
        return jsonify({'success': False, 'errors': errors})

    parser = LL1Parser(cfg, predict_sets, first_sets)
    success, parse_errors = parser.parse(tokens)
    parse_errors = [e.replace('neg', '-') for e in parse_errors]
    if not success:
        return jsonify({'success': False, 'errors': parse_errors})
    return jsonify({'success': True, 'errors': []})


@app.route('/api/semantic', methods=['POST'])
def semantic_analysis():
    data = request.json
    source_code = data.get('source_code', '')
    tokens, errors = lexer_run(source_code)
    if errors:
        return jsonify({'success': False, 'errors': [error.as_string() for error in errors]})

    parser = LL1Parser(cfg, predict_sets, first_sets)
    success, parse_errors = parser.parse(tokens)
    if not success:
        return jsonify({'success': False, 'errors': parse_errors})

    try:
        semantic_tokens = [token for token in tokens if getattr(token, 'type', token) not in {"nl", "\n"}]
        ast_root = build_ast(semantic_tokens)
        ast_root.print_tree()
        return jsonify({'success': True, 'message': 'Semantic analysis completed successfully'})

    except SemanticError as e:
        return jsonify({'success': False, 'errors': [str(e)]})



@app.route('/api/output', methods=['POST'])
def output():
    data = request.json
    source_code = data.get('source_code', '')

    # Lexical analysis
    tokens, errors = lexer_run(source_code)
    if errors:
        return jsonify({'success': False, 'errors': [error.as_string() for error in errors]})

    # Syntax parsing
    parser = LL1Parser(cfg, predict_sets, first_sets)
    success, parse_errors = parser.parse(tokens)
    if not success:
        return jsonify({'success': False, 'errors': parse_errors})

    try:
        # Semantic analysis
        semantic_tokens = [token for token in tokens if getattr(token, 'type', token) not in {"nl", "\n"}]
        ast_root = build_ast(semantic_tokens)
        global runner
        runner = Interpreter(socketio=socketio)
        runner.interpret(ast_root)

        return jsonify({'success': True})

    except InterpreterError as e:
        return jsonify({
            "success": False,
            "errors": [str(e)]
        })


@socketio.on('input_required')
def handle_input_required(data):
    """When the frontend requests input, send the prompt to the client."""
    var_name = data.get('variable')
    prompt = f"Input for {var_name}: "
    
    # Emit the prompt to the frontend
    emit('input_required', {'prompt': prompt, 'variable': var_name})

@socketio.on('capture_input')
def handle_capture_input(data):
    var_name = data.get('var_name')
    user_input = data.get('input')

    if var_name and user_input is not None:
        runner.provide_input(var_name, user_input)  # Pass the input to the interpreter
        emit('input_received', {'var_name': var_name, 'input': user_input})  # Acknowledge input received

if __name__ == '__main__':
    socketio.run(app, debug=True)   