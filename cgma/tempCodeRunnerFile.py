@app.route('/api/semantic', methods=['POST'])
def semantic_analysis():
    data = request.json
    source_code = data.get('source_code', '')
    tokens, errors = lexer_run('<stdin>', source_code)
    if errors:
        return jsonify({'success': False, 'errors': [error.as_string() for error in errors]})
    
    
    parser = LL1Parser(cfg, predict_sets)
    success, ast_root = parser.parse(tokens)
    
    if not success:
        return jsonify({'success': False, 'errors': ['Syntax errors found']})
    
    global symbol_table
    symbol_table = SymbolTable()

    try:
        ast_root = build_ast(tokens)
        ast_root.print_tree()

        semantic_analyzer = SemanticAnalyzer(symbol_table)
        semantic_analyzer.analyze(ast_root)
    
        return jsonify({'success': True, 'message': 'Semantic analysis completed successfully'})
    
    except SemanticError as e:
        return jsonify({'success': False, 'errors': [str(e)]})
    

if __name__ == '__main__':
    app.run(debug=True)