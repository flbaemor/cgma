from cgmaparsery import LL1Parser
from cfg import cfg, predict_sets
from cgmalexer import run as lexer_run
import json

def handler(event, context):
    body = json.loads(event['body'])
    source_code = body['source_code']

    # Run Lexer
    tokens, errors = lexer_run('<stdin>', source_code)

    # If lexer found errors, return them immediately
    if errors:
        return {
            'statusCode': 200,
            'body': json.dumps({'success': False, 'errors': [error.as_string() for error in errors]})
        }

    # Run Parser
    parser = LL1Parser(cfg, predict_sets)
    success, parse_errors = parser.parse(tokens)

    # Return parsing errors if any
    if not success:
        return {
            'statusCode': 200,
            'body': json.dumps({'success': False, 'errors': parse_errors})
        }

    return {
        'statusCode': 200,
        'body': json.dumps({'success': True, 'errors': []})
    }