from cgmaparsery import LL1Parser
from cfg import cfg, predict_sets
from cgmalexer import run as lexer_run
import json

def handler(event, context): 
    body = json.loads(event['body'])
    source_code = body.get('source_code', '')
    tokens, errors = lexer_run('<stdin>', source_code)

    if errors:
        return {
            'statusCode': 200,
            'body': json.dumps({'success': False, 'errors': [error.as_string() for error in errors]})
        }

    parser = LL1Parser(cfg, predict_sets)
    success, parse_errors = parser.parse(tokens)

    return {
        'statusCode': 200,
        'body': json.dumps({'success': success, 'errors': parse_errors})
    }
