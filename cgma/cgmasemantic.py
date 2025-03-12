from cgmalexer import Lexer  
from cfg import cfg, predict_sets  
from cgmaparser import LL1Parser
from flask import Flask, request, jsonify  
from flask_cors import CORS 

##### ERROR ######
class SemanticError(Exception):
    def __init__(self, message,  line):
        super().__init__(message)
        self.message = f"Ln {line} {message}"

    def __str__(self):
        return self.message

##### AST NODES #####
class ASTNode:
    def __init__(self, node_type, value=None, line=None):
        self.node_type = node_type  # Type of node (e.g., 'VariableDeclaration', 'BinaryOp')
        self.value = value  # Optional: variable name, operator, etc.
        self.children = []  # List of child nodes
        self.parent = None  # Reference to parent node (optional)
        self.line = line

    def add_child(self, child):
        child.parent = self
        self.children.append(child)

    def print_tree(self, level=0):
        """Pretty-print the AST."""
        indent = ' ' * (level * 3)
        print(f"{indent}╚═{self.node_type}: {self.value if self.value else ''}")
        for child in self.children:
            child.print_tree(level + 1)
        

class ProgramNode(ASTNode):
    def __init__(self, line=None):
        super().__init__("Program", line=line)

class VariableDeclarationNode(ASTNode):
    def __init__(self, var_type, var_name, value=None, line=None):
        super().__init__("VariableDeclaration", line=line)
        self.add_child(ASTNode("Type", var_type, line=line))
        self.add_child(ASTNode("Identifier", var_name, line=line))
        if value:
            self.add_child(value)

class AssignmentNode(ASTNode):
    def __init__(self, var_name, value, line=None):
        super().__init__("Assignment", line=line)
        self.add_child(ASTNode("Identifier", var_name, line=line))
        self.add_child(value)

class BinaryOpNode(ASTNode):
    def __init__(self, left, operator, right, line=None):
        super().__init__("BinaryOp", operator, line=line)
        self.add_child(left)
        self.add_child(right)

class FunctionDeclarationNode(ASTNode):
    def __init__(self, return_type, name, params, line=None):
        super().__init__("FunctionDeclaration", name, line=line)
        self.add_child(ASTNode("ReturnType", return_type, line=line))
        self.add_child(params)

class FunctionCallNode(ASTNode):
    def __init__(self, name, args, line=None):
        super().__init__("FunctionCall", name, line=line)
        for arg in args:
            self.add_child(arg)

class IfStatementNode(ASTNode):
    def __init__(self, condition, line=None):
        super().__init__("IfStatement", line=line)
        self.add_child(condition)
        self.body = ASTNode("Block", line=line)
        self.add_child(self.body)
        self.else_if_blocks = []
        self.else_block = None

    def add_else_if(self, condition, line=None):
        else_if_node = ASTNode("ElseIfStatement", line=line)
        else_if_node.add_child(condition)
        else_if_node.body = ASTNode("Block", line=line)
        else_if_node.add_child(else_if_node.body)
        self.else_if_blocks.append(else_if_node)
        self.add_child(else_if_node)

    def add_else(self, line=None):
        self.else_block = ASTNode("ElseStatement", line=line)
        self.else_block.body = ASTNode("Block", line=line)
        self.else_block.add_child(self.else_block.body)
        self.add_child(self.else_block)

class ForLoopNode(ASTNode):
    def __init__(self, initialization, condition, update, line=None):
        super().__init__("ForLoop", line=line)  # ✅ Pass line
        self.add_child(initialization)
        self.add_child(condition)
        self.add_child(update)
        self.body = ASTNode("Block", line=line)
        self.add_child(self.body)

class WhileLoopNode(ASTNode):
    def __init__(self, condition, line=None):
        super().__init__("WhileLoop", line=line)  # ✅ Pass line
        self.add_child(condition)
        self.body = ASTNode("Block", line=line)
        self.add_child(self.body)

class DoWhileLoopNode(ASTNode):
    def __init__(self, condition, line=None):
        super().__init__("DoWhileLoop", line=line)  # ✅ Pass line
        self.body = ASTNode("Block", line=line)
        self.add_child(self.body)
        self.add_child(condition)

class PrintStatementNode(ASTNode):
    def __init__(self, expression, line=None):
        super().__init__("PrintStatement", line=line)  # ✅ Pass line
        self.add_child(expression)

class UnaryOpNode(ASTNode):
    def __init__(self, operator, operand):
        super().__init__("UnaryOp", operator)
        self.add_child(operand)

###### SYMBOL TABLE ######

class SymbolTable:
    def __init__(self):
        self.variables = {}  # Stores variables
        self.functions = {}  # Stores function definitions
        self.scopes = [{}]   # Stack of scopes (for local/global tracking)

    ###### VARIABLE ######
    def declare_variable(self, name, type_, value=None):
        scope = self.scopes[-1]
        if name in scope:
            return f"Semantic Error: Variable '{name}' already declared in this scope."

        if len(self.scopes) == 1:
            self.variables[name] = {"type": type_, "value": value}

        else:
            scope[name] = {"type": type_, "value": value}


    def lookup_variable(self, name):
        # Search from innermost scope to global
        for i, scope in enumerate(reversed(self.scopes)):
            if name in scope:
                return scope[name]

        # Check global variables
        if name in self.variables:
            return self.variables[name]

        return f"Semantic Error: Variable '{name}' used before declaration."


    ###### FUNCTION ######
    def declare_function(self, name, return_type, params):
        if name in self.functions:
            return f"Semantic Error: Function '{name}' already declared."
        self.functions[name] = {"return_type": return_type, "params": params}

    def lookup_function(self, name):
        if name in self.functions:
            return self.functions[name]
        return f"Semantic Error: Function '{name}' is not defined."

    ###### SCOPE ######
    def enter_scope(self):
        print("🔹 Entering new scope.")
        self.scopes.append({})
        print("🔹 Current scope:", self.scopes[-1])
        

    def exit_scope(self):
        print("🔹 Exiting scope.")
        if len(self.scopes) > 1:
            self.scopes.pop()
        print("🔹 Current scope:", self.scopes[-1])

    def debug_scopes(self):
        print("\n====== SYMBOL TABLE DEBUG ======")
        print("🔹 Local Scopes (Stacked from Global to Inner Scope):")
        for i, scope in enumerate(self.scopes):
            print(f"  Scope {i}: {scope}")
        print("================================\n")
        

    
##### SEMANTIC ANALYZER #####
class SemanticAnalyzer:
    def __init__(self, symbol_table):
        self.symbol_table = symbol_table
        self.visited_nodes = set()

    def analyze(self, node):
        if node in self.visited_nodes:
            return
        
        self.visited_nodes.add(node)

        """Recursively analyze AST nodes."""
        if node.node_type == "VariableDeclaration":
            var_type = node.children[0].value
            var_name = node.children[1].value
            line = node.line
            error = self.symbol_table.declare_variable(var_name, var_type)
            if error:
                raise SemanticError(error, line)

        elif node.node_type == "Assignment":
            var_name = node.children[0].value
            error = self.symbol_table.lookup_variable(var_name)
            line = node.line
            if isinstance(error, str):
                raise SemanticError(error, line)

        elif node.node_type == "FunctionDeclaration":
            func_name = node.value
            return_type = node.children[0].value
            params = node.children[1].children
            self.symbol_table.declare_function(func_name, return_type, params)

        elif node.node_type == "FunctionCall":
            func_name = node.value
            line = node.line
            if not self.symbol_table.lookup_function(func_name):
                error = f"Semantic Error: Function '{func_name}' is not defined."
                raise SemanticError(error, line)

        for child in node.children:
            self.analyze(child)

symbol_table = SymbolTable()
semantic_analyzer = SemanticAnalyzer(symbol_table)

#######################
###### BUILD AST ######
#######################

def build_ast(tokens):
    """Constructs an AST from the token list after LL(1) parsing."""
    root = ProgramNode()
    index = 0
    
    while index < len(tokens):
        token = tokens[index]

        if token.type == "NL":
            index += 1
            continue
        
        if token.value in {"chungus", "chudeluxe", "forsen", "forsencd", "lwk"}:
            node, index = parse_functionOrVariable(tokens, index)

            if node:
                root.add_child(node)

        elif token.type == "IDENTIFIER" and tokens[index + 1].type == "IS":
            index += 2
            print(f"✅ Adding assignment node for {token.value}")
            node, index = parse_assignment(tokens, index, token.value, symbol_table.lookup_variable(token.value)["type"])
            if node:
                root.add_child(node)

        else:
            node = ASTNode(token.type, token.value, token.line)
            root.add_child(node)
            index += 1
    
    return root

def parse_functionOrVariable(tokens, index):
    id_type = tokens[index].value
    line = tokens[index].line

    if tokens[index + 1].type == "IDENTIFIER" or tokens[index + 1].value == "skibidi":
        id_name = tokens[index + 1].value
        index += 2

        if tokens[index].type == "OPPAR":
            node, index = parse_function(tokens, index, id_name, id_type)
        
        elif tokens[index].type == "IS":
            node, index = parse_variable(tokens, index, id_name, id_type) 
        
        else:
            error = f"Syntax Error: Invalid function or variable declaration."
            raise SemanticError(error, line)
        
        node.line = line
        return node, index
    
    return None, index

def parse_function(tokens, index, func_name, func_type):
    index += 1
    params_node = ASTNode("Parameters")
    line = tokens[index].line
    symbol_table.enter_scope()
    while tokens[index].type != "CLPAR":
        if tokens[index].value in {"chungus", "chudeluxe", "forsen", "forsencd", "lwk"}:
            param_type = tokens[index].value
            index += 1
            if tokens[index].type == "IDENTIFIER":
                param_name = tokens[index].value
                param_node = ASTNode("Parameter")
                param_node.add_child(ASTNode("Type", param_type))
                param_node.add_child(ASTNode("Identifier", param_name))
                params_node.add_child(param_node)
                error = symbol_table.declare_variable(param_name, param_type)
                if error:
                    raise SemanticError(error, line)
                index += 1
 
            else:
                error = f"Syntax Error: Invalid parameter declaration."
                raise SemanticError(error, line)
            
        elif tokens[index].type != "COMMA":
            error = f"Syntax Error: Expected ',' in parameter list."
            raise SemanticError(error, line)
        
        else:
            index += 1
    symbol_table.declare_function(func_name, func_type, params_node.children)
    index += 1
    func_node = FunctionDeclarationNode(func_type, func_name, params_node)

    if tokens[index].type == "OPCUR":
        index += 1
        block_node = ASTNode("Block")
        while tokens[index].type != "CLCUR":
            stmt, index = parse_statement(tokens, index)
            if stmt:
                block_node.add_child(stmt)
            index += 1
        index += 1
        func_node.add_child(block_node)
        symbol_table.exit_scope()
    else:
        error = f"Syntax Error: Function body must be enclosed in curly braces."
        raise SemanticError(error, line)

    return func_node, index

def parse_variable(tokens, index, var_name, var_type):
    var_node_list = ASTNode("VariableDeclarationList")
    line = tokens[index].line
    while True:
        var_node = VariableDeclarationNode(var_type, var_name, line=line)
        error = symbol_table.declare_variable(var_name, var_type)

        if error:
            raise SemanticError(error, line)

        if tokens[index].type == "IS":
            index += 1
            if tokens[index].value == "chat":
                index += 1
                if tokens[index].type == "OPPAR":
                    index += 1
                    if tokens[index].type != "CLPAR":
                        error = f"Syntax Error: chat() should not have parameters."
                        raise SemanticError(error, line)
                    index += 1
                    value_node = ASTNode("Input", "chat()", line=line)
                else:
                    error = f"Syntax Error: Expected () after chat."
                    raise SemanticError(error, line)
            else:
                value_node, index = parse_expression_type(tokens, index, var_type)

            var_node.add_child(value_node)

        else:
            error = f"Syntax Error: Variable must be initialized."
            raise SemanticError(error, line)

        var_node_list.add_child(var_node)

        if tokens[index].type == "COMMA":
            index += 1
            var_name = tokens[index].value
            index += 1
        else:
            break
    return var_node_list, index


def parse_statement(tokens, index):
    token = tokens[index]

    if token.value in {"chungus", "chudeluxe", "forsen", "forsencd", "lwk"}:
        var_type = token.value
        var_name = tokens[index + 1].value
        index += 2

        node, index = parse_variable(tokens, index, var_name, var_type)
        return node, index
    
    elif token.type == "IDENTIFIER":
        if tokens[index + 1].type == "OPPAR":
            func_name = token.value
            error = symbol_table.lookup_function(func_name)
            if isinstance(error, str):
                error = symbol_table.lookup_function(func_name)
                raise SemanticError(error, token.line)
            func_type = symbol_table.lookup_function(func_name)["return_type"]
            func_params = symbol_table.lookup_function(func_name)["params"]
            func_call_node, index = parse_function_call(tokens, index, func_name, func_type, func_params)
            return func_call_node, index

        elif tokens[index + 1].type == "IS":
            var_name = token.value
            if isinstance(symbol_table.lookup_variable(var_name), str):
                error = symbol_table.lookup_variable(var_name)
                raise SemanticError(error, token.line)
            
            var_type = symbol_table.lookup_variable(var_name)["type"]
            index += 2
            node, index = parse_assignment(tokens, index, var_name, var_type)
            return node, index    
        else:
            error = f"Syntax Error: Invalid statement."
            raise SemanticError(error, token.line)
    else:
        return None, index

def parse_expression_type(tokens, index, var_type):
    line = tokens[index].line
    if var_type in {"chungus", "chudeluxe"}:
        return parse_expression(tokens, index)

    elif var_type == "forsencd":
        return parse_expression_forsencd(tokens, index)

    elif var_type == "forsen":
        if tokens[index].type not in {"FORSEN_LIT", "IDENTIFIER"}:
            error = f"Type Error: forsen can only be assigned a FORSEN_LIT."
            raise SemanticError(error, line)
        node = ASTNode("Value", tokens[index].value)
        return node, index + 1  
    
    elif var_type == "lwk":
        return parse_expression_lwk(tokens, index)

    else:
        error = f"Type Error: Invalid type for assignment."
        raise SemanticError(error, line)

def parse_expression_lwk(tokens, index):
    line = tokens[index].line
    
    left_node, index = parse_relational(tokens, index)

    while tokens[index].type in {"AND", "OR"}:
        operator = tokens[index].value
        index += 1  # Move past the operator
        right_node, index = parse_relational(tokens, index)  # Parse the right-hand side
        left_node = BinaryOpNode(left_node, operator, right_node, line=line)  # Build AST node
    
    return left_node, index

def parse_relational(tokens, index):
    line = tokens[index].line

    if tokens[index].type == "LWK_LIT":
        left_node = ASTNode("Value", tokens[index].value, line=line)
        index += 1  # Move past LWK_LIT
        
        if tokens[index].value in {"EQ", "NE"}:
            operator = tokens[index].value
            index += 1

            if tokens[index].type == "LWK_LIT":
                right_node = ASTNode("Value", tokens[index].value, line=line)
                index += 1
                return BinaryOpNode(left_node, operator, right_node, line=line), index
            
            elif tokens[index].type == "IDENTIFIER":
                variable_info = symbol_table.lookup_variable(tokens[index].value)
                if isinstance(variable_info, str):
                    error = f"Semantic Error: Variable '{tokens[index].value}' used before declaration."
                    raise SemanticError(error, line)
                if variable_info["type"] != "lwk":
                    error = f"Type Error: Cannot use '{tokens[index].value}' of type {variable_info['type']} in lwk expression.", line
                    raise SemanticError(error, line)
                
                right_node = ASTNode("Value", tokens[index].value, line=line)
                index += 1
                return BinaryOpNode(left_node, operator, right_node, line=line), index
        
            else:
                error = f"Type Error: Expected LWK_LIT after relational operator."
                raise SemanticError(error, line)

        return left_node, index
    
    elif tokens[index].type == "IDENTIFIER":
        variable_name = tokens[index].value
        left_node = ASTNode("Value", tokens[index].value, line=line)
        index += 1

        variable_info = symbol_table.lookup_variable(variable_name)
        if isinstance(variable_info, str):
            error = f"Semantic Error: Variable '{tokens[index].value}' used before declaration."
            raise SemanticError(error, line)
        
        if variable_info["type"] != "lwk":
            error = f"Type Error: Cannot use '{tokens[index].value}' of type {variable_info['type']} in lwk expression.", line
            raise SemanticError(error, line)
        
        if tokens[index].value in {"EQ", "NE"}:
            operator = tokens[index].value
            index += 1

            if tokens[index].type == "LWK_LIT":
                right_node = ASTNode("Value", tokens[index].value, line=line)
                index += 1
                return BinaryOpNode(left_node, operator, right_node, line=line), index
            
            elif tokens[index].type == "IDENTIFIER":
                variable_info = symbol_table.lookup_variable(tokens[index].value)

                if isinstance(variable_info, str):
                    error = f"Semantic Error: Variable '{tokens[index].value}' used before declaration."
                    raise SemanticError(error, line)
                
                if variable_info["type"] != "lwk":
                    error = f"Type Error: Cannot use '{tokens[index].value}' of type {variable_info['type']} in lwk expression.", line
                    raise SemanticError(error, line)
                
                right_node = ASTNode("Value", tokens[index].value, line=line)
                index += 1
                return BinaryOpNode(left_node, operator, right_node, line=line), index
        
            else:
                error = f"Type Error: Expected lwk lit or lwk type identifier after relational operator."
                raise SemanticError(error, line)

        return left_node, index

    else:
        left_node, index = parse_expression(tokens, index)

        if tokens[index].type in {"LT", "GT", "LE", "GE", "EQ", "NE"}:
            operator = tokens[index].value
            index += 1
            right_node, index = parse_expression(tokens, index)

            if right_node.node_type == "Value" and right_node.value in {"true", "false"}:
               raise SemanticError(f"Type Error: Relational operators can only be used with numeric expressions, not boolean values.", line)
            
        else:
            error = f"Syntax Error: Invalid relational operator."
            raise SemanticError(error, line)

        return BinaryOpNode(left_node, operator, right_node, line=line), index

def parse_expression_forsencd(tokens, index):
    line = tokens[index].line

    if tokens[index].type not in {"FORSENCD_LIT", "IDENTIFIER"}:
        error = f"Type Error: forsencd can only be assigned a FORSENCD_LIT or an identifier of type forsen/forsencd."
        raise SemanticError(error, line)
    
    elif tokens[index].type in {"IDENTIFIER"} and tokens[index + 1].type == "OPPAR":
        func_name = tokens[index].value
        func_info = symbol_table.lookup_function(func_name)
        func_return_type = func_info["return_type"]
        func_params = func_info["params"]
        if func_return_type not in {"forsen", "forsencd"}:
            error = f"Type Error: Cannot use function '{func_name}' of type {func_return_type} in this expression."
            raise SemanticError(error, line)
        return parse_function_call(tokens, index, func_name, func_return_type, func_params)

    elif tokens[index].type == "IDENTIFIER":
        variable_info = symbol_table.lookup_variable(tokens[index].value)

        if isinstance(variable_info, str):
            error = f"Semantic Error: Variable '{tokens[index].value}' used before declaration."
            raise SemanticError(error, line)
        
        if variable_info["type"] not in {"forsen", "forsencd"}:
            error = f"Type Error: Variable '{tokens[index].value}' is not of type forsen/forsencd."
            raise SemanticError(error, line)
    
    left_node = ASTNode("Value", tokens[index].value)
    index += 1

    if tokens[index].type not in {"PLUS"}:
        error = f"Syntax Error: Invalid operator in forsencd expression."
        raise SemanticError(error, line)

    while tokens[index].type in {"PLUS"}:
        op = tokens[index].value
        index += 1

        # Ensure valid type for right operand
        if tokens[index].type not in {"FORSENCD_LIT", "IDENTIFIER", "FORSEN_LIT"}:
            raise SemanticError(f"Type Error: forsencd can only use + with forsencd literals, forsen literals, or identifiers of type forsencd/forsen.", line)

        if tokens[index].type == "IDENTIFIER":
            variable_info = symbol_table.lookup_variable(tokens[index].value)
            if isinstance(variable_info, str):  # Undefined variable
                raise SemanticError(f"Semantic Error: Variable '{tokens[index].value}' used before declaration.", line)

            if variable_info["type"] not in {"forsencd", "forsen"}:
                raise SemanticError(f"Type Error: Cannot use '{tokens[index].value}' of type {variable_info['type']} in forsencd expression.", line)

        right_node = ASTNode("Value", tokens[index].value)
        index += 1  # Move past right operand

        left_node = BinaryOpNode(left_node, op, right_node)  # Create BinaryOp node

    return left_node, index

def parse_expression(tokens, index):
    """Parses an expression with right-to-left associativity for + and -."""
    right_node, index = parse_term(tokens, index)

    while tokens[index].type in {"PLUS", "MINUS"}:
        op = tokens[index].value
        index += 1
        left_node, index = parse_term(tokens, index)
        right_node = BinaryOpNode(left_node, op, right_node)

    return right_node, index

def parse_term(tokens, index):
    """Parses multiplication, division, and modulus with right-to-left associativity."""
    right_node, index = parse_unary(tokens, index)

    while tokens[index].type in {"MUL", "DIV", "MOD"}:
        op = tokens[index].value
        index += 1
        left_node, index = parse_unary(tokens, index)
        right_node = BinaryOpNode(left_node, op, right_node)

    return right_node, index

def parse_unary(tokens, index):
    """Parses unary operators (++x, --x, !x, -x) with right-to-left associativity."""
    if tokens[index].type in {"INC", "DEC", "NOT", "NEGAT"}:
        op = tokens[index].value
        index += 1
        operand, index = parse_unary(tokens, index)
        return UnaryOpNode(op, operand), index

    return parse_factor(tokens, index)

def parse_factor(tokens, index):
    """Parses literals, identifiers, parenthesized expressions, and postfix operators."""
    token = tokens[index]

    if token.type in {"CHU_LIT", "CHUDEL_LIT"}:
        node = ASTNode("Value", token.value)
        index += 1  

        while tokens[index].type in {"INC", "DEC"}:
            op = tokens[index].value
            index += 1
            node = UnaryOpNode(op, node)

        return node, index
    
    elif token.type in {"IDENTIFIER"} and tokens[index + 1].type == "OPPAR":
        func_name = token.value
        func_info = symbol_table.lookup_function(func_name)
        func_return_type = func_info["return_type"]
        func_params = func_info["params"]
        if func_return_type not in {"chungus", "chudeluxe"}:
            error = f"Type Error: Cannot use function '{func_name}' of type {func_return_type} in this expression."
            raise SemanticError(error, token.line)

        node = parse_function_call(tokens, index, func_name, func_return_type, func_params)

        while tokens[index].type in {"INC", "DEC"}:
            op = tokens[index].value
            index += 1
            node = UnaryOpNode(op, node)

        return node, index

    elif token.type in {"IDENTIFIER"}:
        variable_info = symbol_table.lookup_variable(token.value)
        if isinstance(variable_info, str):
            raise SemanticError(f"Semantic Error: Variable '{token.value}' used before declaration.", token.line)
        
        if variable_info["type"] not in {"chungus", "chudeluxe"}:
            error = f"Type Error: Cannot use '{token.value}' of type {variable_info['type']} in this expression."
            raise SemanticError(error, token.line)
        
        node = ASTNode("Value", token.value)
        index += 1  

        while tokens[index].type in {"INC", "DEC"}:
            op = tokens[index].value
            index += 1
            node = UnaryOpNode(op, node)

        return node, index

    elif token.type == "OPPAR":
        index += 1  
        node, index = parse_expression(tokens, index)  
        if tokens[index].type == "CLPAR":
            index += 1  
        return node, index  

    else:
        error = f"Syntax Error: Invalid factor '{token.value}' in expression."
        raise SemanticError(error, token.line)

def parse_assignment(tokens, index, var_name, var_type):
    line = tokens[index].line
    if tokens[index-1].type == "IS":
            if tokens[index].value == "chat":
                index += 1
                if tokens[index].type == "OPPAR":
                    index += 1
                    if tokens[index].type != "CLPAR":
                        error = f"Syntax Error: chat() should not have parameters."
                        raise SemanticError(error, line)
                    index += 1
                    value_node = ASTNode("Input", "chat()", line=line)
                else:
                    error = f"Syntax Error: Expected() after chat."
                    raise SemanticError(error, line)
            else:
                value_node, index = parse_expression_type(tokens, index, var_type)
    assign_node = AssignmentNode(var_name, value_node, line=line)
    return assign_node, index

def parse_function_call(tokens, index, func_name, func_type, func_params):
    line = tokens[index].line
    index += 2  # Move past function name and '('

    args_node = ASTNode("Arguments")
    provided_args = []  # Store parsed argument nodes

    expected_params = func_params

    while tokens[index].type != "CLPAR":
        if tokens[index].type == "IDENTIFIER":
            arg_name = tokens[index].value
            var_info = symbol_table.lookup_variable(arg_name)
            if isinstance(var_info, str):
                raise SemanticError(f"Semantic Error: Variable '{arg_name}' used before declaration.", line)
            
            arg_type = var_info["type"]
            arg_node = ASTNode("Value", arg_name, line=line)

            args_node.add_child(arg_node)
            provided_args.append((arg_node, arg_type))
            index += 1

        else:
            raise SemanticError(f"Syntax Error: Invalid argument in function call.", line)
        
        if tokens[index].type == "COMMA":
            index += 1

    index += 1  # skip ')'

    #  correct number of arguments
    if len(provided_args) != len(expected_params):
        raise SemanticError(f"Type Error: Function '{func_name}' expects {len(expected_params)} arguments, but {len(provided_args)} were provided.", line)

    # ✅ Ensure argument types match expected parameter types
    for i, (arg_node, arg_type) in enumerate(provided_args):
        expected_type = expected_params[i].children[0].value

        if arg_type != expected_type:
            raise SemanticError(f"Type Error: Argument {i+1} of '{func_name}' should be '{expected_type}', but got '{arg_type}'.", line)
        
    #  argument types match expected parameter types

    return FunctionCallNode(func_name, args_node.children, line=line), index

def parse_argument(tokens, index):
    line = tokens[index].line

    # ✅ If argument is a boolean literal (true/false)
    if tokens[index].type == "IDENTIFIER":
        arg_name = tokens[index].value
        arg_info = symbol_table.lookup_variable(arg_name)
        if isinstance(arg_info, str):
            raise SemanticError(f"Semantic Error: Variable '{arg_name}' used before declaration.", line)
        
        arg_type = arg_info["type"]
        arg_node = ASTNode("Value", arg_name, line=line)
        index += 1

    else:
        raise SemanticError(f"Syntax Error: Invalid argument in function call.", line)

    return arg_node, arg_type, index

