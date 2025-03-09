class Semantic

class SymbolTable:
    def __init__(self):
        self.table = {}

    def define(self, name, value=None, type=None):
        if isinstance(value, SymbolTable):
            self.table[name] = value
        else:
            self.table[name] = {'value': value, 'type': type}

    def lookup(self, name):
        return self.table.get(name, None)

    def assign(self, name, value):
        if name in self.table:
            self.table[name]['value'] = value
        else:
            raise Exception(f"Semantic Error: '{name}' is not declared.")

class SemanticAnalyzer:
    def __init__(self):
        self.global_variables = SymbolTable()  # Global variable symbol table
        self.functions = SymbolTable()  # Stores function names and return types
        self.function_scopes = SymbolTable()  # Stores symbol tables for each function
        self.errors = []
        self.current_function = None 

    def lookup_identifier(self, identifier, line):
        declared_symbol = None

        # Check global variables
        if isinstance(self.global_variables, SymbolTable):
            declared_symbol = self.global_variables.lookup(identifier)

        # Check functions
        if declared_symbol is None and isinstance(self.functions, SymbolTable):
            declared_symbol = self.functions.lookup(identifier)

        # Check local function scope
        if declared_symbol is None and self.current_function:
            function_table = self.function_scopes.lookup(self.current_function)
            if isinstance(function_table, SymbolTable):
                declared_symbol = function_table.lookup(identifier)

        # If identifier is still not found, report an error
        if declared_symbol is None:
            self.errors.append(f"Ln {line} Semantic Error: Undeclared identifier '{identifier}' used in assignment.")

        return declared_symbol

    def analyze(self, tokens):
        i = 0
        line = 1
        while i < len(tokens):
            token = tokens[i]
            
            if token.type == "NL":
                line += 1
            elif token.type == "COMMENT" and '\n' in token.value:
                line += 1

            # Function & Variable Declaration
            if token.value in {"chungus", "chudeluxe", "forsen", "forsencd", "lwk", "nocap", "aura", "gng"}:
                if i + 1 < len(tokens) and tokens[i + 1].type == "IDENTIFIER" or tokens[i + 1].value == "skibidi":
                    identifier_name = tokens[i + 1].value
                    
                    # Check if identifier is already declared
                    if self.functions.lookup(identifier_name) or self.global_variables.lookup(identifier_name):
                        self.errors.append(f"Ln {line} Semantic Error: '{identifier_name}' is already declared globally.")
                    elif self.current_function:
                        function_scope = self.function_scopes.lookup(self.current_function)
                        if isinstance(function_scope, SymbolTable):
                            if function_scope.lookup(identifier_name):
                                self.errors.append(f"Ln {line} Semantic Error: '{identifier_name}' is already declared in function '{self.current_function}'.")
                    else:
                        if i + 2 < len(tokens) and tokens[i + 2].type == "OPPAR":
                            # Function declaration
                            self.functions.define(identifier_name, type=token.value)
                            self.function_scopes.define(identifier_name, SymbolTable())
                            self.current_function = identifier_name

                        else:
                            # Variable declaration
                            if i + 2 < len(tokens) and tokens[i + 2].type == "IS":
                                assignment_tokens = []
                                j = i + 3
                                
                                while j < len(tokens) and tokens[j].type not in {"SEMICOL", "COMMA", "NL"}:
                                    assignment_tokens.append(tokens[j])
                                    j += 1

                                if token.value in {"chungus", "chudeluxe"}:
                                    for t in assignment_tokens:
                                        if t.type == "IDENTIFIER":
                                            declared_symbol = self.lookup_identifier(t.value, line)
                                            if declared_symbol:
                                                if declared_type not in {"chungus", "chudeluxe"}:
                                                    self.errors.append(f"Ln {line} Semantic Error: Identifier '{t.value}' has incompatible type '{declared_type}'.")
                                                    break

                                        elif t.type not in {"CHU_LIT", "CHUDEL_LIT", "PLUS", "MINUS", "MUL", "DIV", "MOD", "INC", "DEC", "OPPAR", "CLPAR", "NEGAT"}:
                                            self.errors.append(f"Ln {line} Semantic Error: Invalid value assigned to '{identifier_name}'. Expected a number or expression.")
                                            break

                                elif token.value in {"forsen"}:
                                    for t in assignment_tokens:
                                        if t.type not in {"FORSEN_LIT"}:
                                            self.errors.append(f"Ln {line} Semantic Error: Invalid value assigned to '{identifier_name}'.")
                                            break

                                elif token.value in {"forsencd"}:
                                    for t in assignment_tokens:
                                        if t.type == "IDENTIFIER":
                                            declared_symbol = self.lookup_identifier(t.value, line)
                                            if declared_symbol:
                                                if declared_type not in {"forsencd", "forsen"}:
                                                    self.errors.append(f"Ln {line} Semantic Error: Identifier '{t.value}' has incompatible type '{declared_type}'.")
                                                    break

                                        elif t.type not in {"FORSENCD_LIT", "PLUS"}:
                                            self.errors.append(f"Ln {line} Semantic Error: Invalid value assigned to '{identifier_name}'.")
                                            break

                                elif token.value in {"lwk"}:
                                    for t in assignment_tokens:
                                        if t.type not in {"LWK_LIT"}:
                                            self.errors.append(f"Ln {line} Semantic Error: Invalid value assigned to '{identifier_name}'.")
                                            break
                                

                                assigned_value = "".join(t.value for t in assignment_tokens)                
                            
                            else:
                                assigned_value = None

                            if self.current_function:
                                # Variable inside a function
                                self.function_scopes[self.current_function].define(identifier_name, assigned_value, token.value)
                            else:
                                # Global variable
                                self.global_variables.define(identifier_name, assigned_value, token.value)
                i += 2

            # Handling Variable Usage
            if token.type == "IDENTIFIER":
                declared_symbol = None

                # Check if identifier exists in global variables
                if isinstance(self.global_variables, SymbolTable):
                    declared_symbol = self.global_variables.lookup(token.value)

                # Check if it's a function
                if declared_symbol is None and isinstance(self.functions, SymbolTable):
                    declared_symbol = self.functions.lookup(token.value)

                # Check if identifier exists in the current function's local scope
                if declared_symbol is None and self.current_function:
                    function_table = self.function_scopes.lookup(self.current_function)
                    if isinstance(function_table, SymbolTable):
                        declared_symbol = function_table.lookup(token.value)

                # If identifier is still not found, report an error
                if declared_symbol is None:
                    self.errors.append(f"Ln {line} Semantic Error: Undeclared identifier '{token.value}' used in assignment.")
                    break

                # Retrieve declared type safely
                declared_type = declared_symbol['type']

            # Check for function scope end
            if token.type == "CLCUR" and self.current_function:
                self.current_function = None

            i += 1

        # Output
        
        print("\nFunctions:")
        for func_name, data in self.functions.table.items():
            print(f"{data['type']}: {func_name}")

        print("\nGlobal Variables:")
        for identifier_name, data in self.global_variables.table.items():
            print(f"{data['type']}: {identifier_name} = {data['value']}")

        print("\nStored Variables in Functions:")
        for func_name, func_table in self.function_scopes.table.items():
            print(f"\nFunction '{func_name}':")
            if isinstance(func_table, SymbolTable):
                for var_name, data in func_table.table.items():
                    print(f"  {data['type']}: {var_name} = {data['value']}")

        return self.errors