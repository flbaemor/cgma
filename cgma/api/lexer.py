from cgmalexer import run as lexer_run
import json

def lambda_handler(event, context):
    body = json.loads(event['body'])
    source_code = body['source_code']
    tokens, errors = lexer_run('<stdin>', source_code)

    response = {
        'tokens': [{'type': token.type, 'value': token.value} for token in tokens],
        'errors': [error.as_string() for error in errors]
    }

    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }
