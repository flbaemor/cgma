# LL(1) Parser Class
class LL1Parser:
    def __init__(self, cfg, predict_sets):
        self.cfg = cfg
        self.predict_sets = predict_sets
        self.parsing_table = self.construct_parsing_table()
        self.stack = []
        self.tokens = []

    def construct_parsing_table(self):
        ###############################################################################################################
        #kinukuha dito yung every value sa predict set ng kada production ng non terminal (left hand side ng cfg), 
        #tapos nilalagay yung value with the corresponding production sa parsing table
        #ginagamit sha para ma check kung anong production gagamitin depending sa current token
        ###############################################################################################################
        parsing_table = {} 
        for non_terminal, productions in self.cfg.items():
            parsing_table[non_terminal] = {}
            for production in productions:
                predict_key = (non_terminal, tuple(production))
                if predict_key in self.predict_sets:
                    for terminal in self.predict_sets[predict_key]:
                        parsing_table[non_terminal][terminal] = production
        #for non_terminal in parsing_table:
            #print(f"Parsing table for {non_terminal}: {parsing_table[non_terminal]}")
        return parsing_table

    def parse(self, tokens):
        self.stack = ['EOF', list(self.cfg.keys())[0]] #dulo ng stack is EOF tapos <program>
        index = 0
        error_messages = []

        while self.stack:
            top = self.stack.pop() #dulo ng stack
            token = tokens[index] 
            token_type = token.type  
            token_value = token.value  
            line = token.line

            print(f"\nStack Top: {top}, Token Type: {token_type}, Token Value: {token_value}")

            if top == token_type:
                print(f"Matched: {top}")
                index += 1 #skip sa next token
                
            elif top in self.parsing_table: # top is non terminal
                if token_type in self.parsing_table[top]: #checks if current token is nasa parsing table nung production na un
                    production = self.parsing_table[top][token_type] #expands the non terminal (ex. <program> to <global_dec> <func_dec> skibidi...)
                    print(f"Expand: {top} → {' '.join(production)}")
                    
                    if production != ['ε']:
                        self.stack.extend(reversed(production)) #adds the production to the stack
                    print(f"Updated Stack: {self.stack}")
                else:
                    expected_tokens = list(set(self.parsing_table[top].keys()))
                    
                    print(expected_tokens)
                    error_message = f"Ln {line} Syntax Error: Unexpected token '{token_value}'. Expected: {expected_tokens}"
                    #print(error_message)
                    error_messages.append(error_message)
                    return False, error_messages
            

            elif top == 'EOF': #skips newlines at the beginning and end
                while token_type == 'nl':
                    index += 1
                    token = tokens[index]
                    token_type = token.type
                    token_value = token.value
                if token_type != 'nl' and token_type != 'EOF':
                    error_message = f"Ln {line} Syntax Error: Unexpected token '{token_value}'. Expected: 'EOF'"
                    error_messages.append(error_message)
                    return False, error_messages
                    
            else:
                error_message = f"Ln {line} Syntax Error: Unexpected token '{token_value}'. Expected: '{top}'"
                #print(error_message)
                error_messages.append(error_message)
                return False, error_messages

        if token_type == 'EOF' and not self.stack:
            #print("\nSyntax analysis successful!")
            return True, []
        
        else:
            #print("Error: Tokens remaining after parsing")
            return False, error_messages