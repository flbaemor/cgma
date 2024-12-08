import cgmalexer

while True:
    text = input('cgma > ')
    result, error = cgmalexer.run('<file>', text)

    if error: print(error.as_string())
    else: print(result)