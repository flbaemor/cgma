# LL(1) Parser Class
class LL1Parser:
    def __init__(self, cfg, predict_sets, first_sets):
        self.cfg = cfg
        self.predict_sets = predict_sets
        self.parsing_table = self.construct_parsing_table()
        self.stack = []
        self.tokens = []
        self.first_sets = first_sets

    def construct_parsing_table(self):
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
        self.stack = ['EOF', list(self.cfg.keys())[0]]
        index = 0
        error_messages = []
        expected_tokens = set()

        while self.stack:
            top = self.stack[-1]
            token = tokens[index] 
            token_type = token.type  
            token_value = token.value  
            line = token.line
            
            #print(f"\nStack Top: {top}, Token Type: {token_type}, Token Value: {token_value}")

            if top == token_type:
                #print(f"Matched: {top}")
                self.stack.pop()
                index += 1
                
            elif top in self.parsing_table: 
                if token_type in self.parsing_table[top]: 
                    production = self.parsing_table[top][token_type] 
                    #print(f"Expand: {top} → {' '.join(production)}")
                    self.stack.pop()
                    if production != ['ε']:
                        self.stack.extend(reversed(production))
                    #print(f"Updated Stack: {self.stack}")

                elif 'ε' in self.parsing_table[top]:
                    expected_tokens |= set(self.first_sets[top]) - set(['ε'])
                    self.stack.pop()
                    continue
                    
                else:
                    expected_tokens |= set(self.first_sets[top]) - set(['ε'])
                    error_message = f"Ln {line} Syntax Error: Unexpected token '{token_value}'. Expected: {expected_tokens}"
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
                expected_tokens.add(top)
                if token_type == 'EOF':
                    token_value = 'EOF'
                error_message = f"Ln {line} Syntax Error: Unexpected token '{token_value}'. Expected: {expected_tokens}"
                #print(error_message)
                error_messages.append(error_message)
                return False, error_messages

        if token_type == 'EOF' and not self.stack:
            #print("\nSyntax analysis successful!")
            return True, []
        
        else:
            #print("Error: Tokens remaining after parsing")
            return False, error_messages