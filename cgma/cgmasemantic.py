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
        super().__init__("Value", operator, line=line)
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

class ForLoopNode(ASTNode):
    def __init__(self, initialization, condition, update, line=None):
        super().__init__("ForLoop", line=line)  
        self.add_child(initialization)
        self.add_child(condition)
        self.add_child(update)

class WhileLoopNode(ASTNode):
    def __init__(self, condition, line=None):
        super().__init__("WhileLoop", line=line)  
        self.add_child(condition)

class DoWhileLoopNode(ASTNode):
    def __init__(self, condition, line=None):
        super().__init__("DoWhileLoop", line=line)

class PrintNode(ASTNode):
    def __init__(self, args, line=None):
        super().__init__("PrintStatement", line=line) 
        for arg in args:
            self.add_child(arg)

class UnaryOpNode(ASTNode):
    def __init__(self, operator, operand):
        super().__init__("UnaryOp", operator)
        self.add_child(operand)

class SturdyDeclarationNode(ASTNode):
    def __init__(self, var_type, var_name, value, line=None):
        super().__init__("SturdyDeclaration", line=line)
        self.add_child(ASTNode("Type", var_type, line=line))
        self.add_child(ASTNode("Identifier", var_name, line=line))
        self.add_child(value)

class ReturnNode(ASTNode):
    def __init__(self, return_value=None, line=None):
        super().__init__("Return", line=line)
        if return_value:
            self.add_child(return_value)

class UpdateNode(ASTNode):
    def __init__(self, operator, operand, prefix = True, line=None):
        super().__init__("Update", line=line)
        self.prefix = prefix
        self.add_child(operand)

class SwitchNode(ASTNode):
    def __init__(self, expression, cases, default_case, line=None):
        super().__init__("Switch", line=line)
        self.add_child(expression)
        for case in cases:
            self.add_child(case)
        self.add_child(default_case)

class ContinueNode(ASTNode):
    def __init__(self, line=None):
        super().__init__("Continue", line=line)

class BreakNode(ASTNode):
    def __init__(self, line=None):
        super().__init__("Break", line=line)

class ListNode(ASTNode):
    def __init__(self, line=None, elements = None):
        super().__init__("List", line=line)
        for element in elements:
            self.add_child(element)

class TaperNode(ASTNode):
    def __init__(self, variable_name, line=None):
        super().__init__("TaperFunction", line=line)
        self.add_child(ASTNode("Identifier", variable_name, line=line))

class TSNode(ASTNode):
    def __init__(self, variable_name, line=None):
        super().__init__("TSFunction", line=line)
        self.add_child(ASTNode("Identifier", variable_name, line=line))

class AppendNode(ASTNode):
    def __init__(self, elements, line=None):
        super().__init__("Append", line=line)
        for elem in elements:
            self.add_child(elem)

class InsertNode(ASTNode):
    def __init__(self, index, elements, line=None):
        super().__init__("Insert", line=line)
        self.add_child(ASTNode("Index", index, line=line))
        for elem in elements:
            self.add_child(elem)

class RemoveNode(ASTNode):
    def __init__(self, value, index, line=None):
        super().__init__("Remove", line=line)
        self.add_child(ASTNode("Identifier", value, line=line))
        self.add_child(ASTNode("Index", index, line=line))

class CastNode(ASTNode):
    def __init__(self, target_type, expression, line=None):
        super().__init__("TypeCast", line=line)
        self.add_child(ASTNode("TargetType", target_type, line=line))
        self.add_child(expression)

class StructNode(ASTNode):
    def __init__(self, name, members, line=None):
        super().__init__("Struct", line=line)
        self.add_child(ASTNode("Identifier", name, line=line))
        for member in members:
            self.add_child(member)

class StructInstanceNode(ASTNode):
    def __init__(self, struct_name, instance_name, initial_values=None, line=None):
        super().__init__("StructInstance", line=line)
        self.add_child(ASTNode("StructType", struct_name, line=line))
        self.add_child(ASTNode("Identifier", instance_name, line=line))

        if initial_values:
            init_node = ASTNode("InitialValues", line=line)
            for key, value in initial_values.items():
                assign_node = ASTNode("Assignment", line=line)
                assign_node.add_child(ASTNode("Member", key, line=line))
                assign_node.add_child(ASTNode("Value", value, line=line))
                init_node.add_child(assign_node)
            self.add_child(init_node)

class StructMemberAssignmentNode(ASTNode):
    def __init__(self, struct_instance, member_name, value_node, line=None):
        super().__init__("StructMemberAssignment", line=line)
        self.add_child(ASTNode("StructInstance", struct_instance, line=line))
        self.add_child(ASTNode("Member", member_name, line=line))

        if isinstance(value_node, ASTNode) and value_node.node_type in {"Value", "BinaryOp"}:
            self.add_child(value_node)
            
            self.add_child(ASTNode("Value", value_node, line=line))

class StructMemberAccessNode(ASTNode):
    def __init__(self, struct_instance, member_name, member_type, line=None):
        super().__init__("StructMemberAccess", line=line)
        self.add_child(ASTNode("StructInstance", struct_instance, line=line))
        self.add_child(ASTNode("Member", member_name, line=line))
        self.member_type = member_type

###### SYMBOL TABLE ######

class SymbolTable:
    def __init__(self):
        self.variables = {}  # Stores variables
        self.functions = {}  # Stores function definitions
        self.scopes = [{}]   # Stack of scopes (for local/global tracking)
        self.structs = [{}]  # Stack of structs

    ###### VARIABLE ######
    def declare_variable(self, name, type_, value=None, is_list=False, is_struct=False, is_sturdy=False):
        scope = self.scopes[-1]

        if name in scope:
            return f"Semantic Error: Variable '{name}' already declared in this scope."

        if len(self.scopes) == 1:
            if name in self.variables:
                return f"Semantic Error: Variable '{name}' already declared."
            if name in self.functions:
                return f"Semantic Error: Variable '{name}' already declared as a function."
            
            self.variables[name] = {
                "type": type_,  
                "value": value,
                "is_list": is_list,
                "is_struct": is_struct,
                "is_sturdy": is_sturdy
            }
        else:

            scope[name] = {
                "type": type_,
                "value": value,
                "is_list": is_list,
                "is_struct": is_struct
            }



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
    
    ###### STRUCT ######
    def declare_struct(self, name, members):
        for scope in self.structs:
            if name in scope:
                return f"Semantic Error: Struct '{name}' is already declared."
        self.structs[-1][name] = {
            member.value.split()[1]: {  
                "type": member.value.split()[0],
                "default": member.children[0].value if member.children else None
            } for member in members
        }



    def lookup_struct(self, name):
        for scope in reversed(self.structs):
            if name in scope:
                return scope[name]
        return f"Semantic Error: Struct '{name}' is not defined."

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
            self.symbol_table.declare_variable(var_name, var_type)


        elif node.node_type == "Assignment":
            var_name = node.children[0].value
            
            
        elif node.node_type == "FunctionDeclaration":
            func_name = node.value
            return_type = node.children[0].value
            params = node.children[1].children
            self.symbol_table.declare_function(func_name, return_type, params)

        elif node.node_type == "FunctionCall":
            func_name = node.value

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
    symbol_table.variables = {}  # Stores variables
    symbol_table.functions = {}  # Stores function definitions
    symbol_table.scopes = [{}] 
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

        elif token.value == "nocap":
            index += 1
            if tokens[index].type == "IDENTIFIER":
                func_name = tokens[index].value
                func_type = "nocap"
                node, index = parse_function(tokens, index, func_name, func_type)
            else:
                raise SemanticError(f"Semantic Error: Invalid function declaration.", token.line)
            
            if node:
                root.add_child(node)
            

        elif token.value == "sturdy":
            node, index = parse_sturdy(tokens, index)
            if node:
                root.add_child(node)

        elif token.value == "aura":
            node, index = parse_struct(tokens, index)
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

    if func_name in symbol_table.functions:
        error = f"Semantic Error: '{func_name}' already declared."
        raise SemanticError(error, tokens[index].line)
    
    elif func_name in symbol_table.variables:
        error = f"Semantic Error: '{func_name}' already declared."
        raise SemanticError(error, tokens[index].line)

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

                if tokens[index].type == "COMMA":
                    index += 1

            else:
                error = f"Syntax Error: Invalid parameter declaration."
                raise SemanticError(error, line)
        
        else:
            index += 1
            
    symbol_table.declare_function(func_name, func_type, params_node.children)
    index += 1
    func_node = FunctionDeclarationNode(func_type, func_name, params_node)

    if tokens[index].type == "OPCUR":
        index += 1
        block_node = ASTNode("Block")
        return_found = False
        while tokens[index].type != "CLCUR":
            stmt, index = parse_statement(tokens, index, func_type)
            if stmt:
                block_node.add_child(stmt)

                if isinstance(stmt, ReturnNode):
                    return_found = True
            index += 1
        
        if func_type != "nocap" and not return_found:
            error = f"Semantic Error: Function '{func_name}' must return a value of type '{func_type}'."

        index += 1
        func_node.add_child(block_node)
        symbol_table.exit_scope()
    else:
        error = f"Syntax Error: Function body must be enclosed in curly braces."
        raise SemanticError(error, line)

    return func_node, index

def parse_variable(tokens, index, var_name, var_type):
    line = tokens[index].line
    var_nodes = []

    while True:
        global_var = symbol_table.variables.get(var_name)
        if global_var and global_var.get("is_sturdy"):
            raise SemanticError(f"Semantic Error: Variable '{var_name}' is declared as sturdy and cannot be re-declared.", line)

        is_list = False

        var_node = VariableDeclarationNode(var_type, var_name, line=line)

        if tokens[index].type == "IS":
            index += 1

            if (
                var_type == "forsen" and
                tokens[index].type == "IDENTIFIER" and
                tokens[index + 1].type == "DOT" and
                tokens[index + 2].value == "taper"
            ):
                identifier = tokens[index].value

                identifier_info = symbol_table.lookup_variable(identifier)
                if isinstance(identifier_info, str):
                    raise SemanticError(f"Semantic Error: Variable '{identifier}' used before declaration.", line)

                if identifier_info["type"] != "forsencd":
                    raise SemanticError(f"Type Error: Cannot use taper function on '{identifier}'. Must be a forsencd type identifier.", line)

                index += 3
                is_list = True
                taper_node = TaperNode(identifier, line=line)
                var_node.add_child(taper_node)


            elif tokens[index].value == "chat":
                index += 1
                if tokens[index].type == "OPPAR":
                    index += 1
                    if tokens[index].type != "CLPAR":
                        raise SemanticError(f"Semantic Error: chat() should not have parameters.", line)
                    index += 1
                    value_node = ASTNode("Input", "chat()", line=line)
                else:
                    raise SemanticError(f"Syntax Error: Expected () after chat.", line)

                var_node.add_child(value_node)

            elif tokens[index].type == "OPBRA":
                is_list = True
                value_node, index = parse_list(tokens, index, var_type)
                var_node.add_child(value_node)

            else:
                value_node, index = parse_expression_type(tokens, index, var_type)
                var_node.add_child(value_node)
   
        else:
            raise SemanticError(f"Semantic Error: Variable must be initialized. Missing '=' after '{var_name}'.", line)

        error = symbol_table.declare_variable(var_name, var_type, is_list = is_list)

        if isinstance(error, str):
            raise SemanticError(error, line)
        
        var_nodes.append(var_node)

        if tokens[index].type == "COMMA":
            index += 1
            var_name = tokens[index].value
            index += 1
        else:
            break

    if len(var_nodes) == 1:
        return var_nodes[0], index
    else:
        var_list_node = ASTNode("VariableDeclarationList")
        for node in var_nodes:
            var_list_node.add_child(node)
        return var_list_node, index


def parse_statement(tokens, index, func_type = None):
    token = tokens[index]
    line = token.line

    if token.value in {"chungus", "chudeluxe", "forsen", "forsencd", "lwk"}:
        var_type = token.value
        var_name = tokens[index + 1].value
        index += 2

        node, index = parse_variable(tokens, index, var_name, var_type)
        return node, index
    
    elif token.value == "aura" and tokens[index + 1].type == "IDENTIFIER" and tokens[index + 2].type == "OPCUR":
        node, index = parse_struct(tokens, index)
        return node, index

    elif token.value == "aura":
        node, index = parse_struct_instance(tokens, index)
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
            error = symbol_table.lookup_variable(var_name)
            if isinstance(error, str):
                raise SemanticError(error, token.line)
            
            index += 2
            node, index = parse_assignment(tokens, index, token.value, symbol_table.lookup_variable(token.value)["type"])
            return node, index    
        
        elif tokens[index+1].type in {"INC", "DEC"}:
            operand = ASTNode("Identifier", token.value, line=line)
            operator = tokens[index + 1].value
            index += 2
            return UpdateNode(operator, operand, prefix = False, line=line), index
        
        elif tokens[index + 1].type == "DOT":
            node, index = parse_struct_member_assignment(tokens, index)
            return node, index
        
        else:
            raise SemanticError(f"Semantic Error: Unexpected token '{tokens[index].value}' in statement.", line)
    
    elif tokens[index].type in {"INC", "DEC"}:
        operator = tokens[index].value
        index += 1

        if tokens[index].type == "IDENTIFIER":
            var_name = symbol_table.lookup_variable(tokens[index].value)
            if isinstance(var_name, str):
                raise SemanticError(f"Semantic Error: Variable '{var_name}' used before declaration.", line)
            
            operand = ASTNode("Identifier", tokens[index].value, line=line)
            index += 1

            return UpdateNode(operator, operand, prefix = True, line=line), index
    
    elif token.value == "aura" and tokens[index + 1].type == "IDENTIFIER" and tokens[index + 2].type == "IDENTIFIER":
        node, index = parse_struct_instance(tokens, index)
        return node, index

    elif token.value == "aura" and tokens[index + 1].type == "IDENTIFIER" and tokens[index + 2].type == "OPCUR":
        node, index = parse_struct(tokens, index)
        return node, index


    elif token.value == "yap":
        node, index = parse_print(tokens, index)
        return node, index

    elif token.value == "tuah":
        node, index = parse_if(tokens, index)
        return node, index

    elif token.value == "back":
        node, index = parse_return(tokens, index, func_type)
        return node, index 
    
    elif token.value == "plug":
        node, index = parse_for(tokens, index)
        return node, index

    elif token.value == "jit":
        node, index = parse_while(tokens, index)
        return node, index
    
    elif token.value == "lil":
        node, index = parse_do(tokens, index)
        return node, index
    
    elif token.value == "lethimcook":
        node, index = parse_switch(tokens, index)
        return node, index
    
    else:
        while tokens[index].type not in {"NL", "EOF", "COMMENT"}:
            index += 1

        return None, index


def parse_expression_type(tokens, index, var_type):
    line = tokens[index].line
    if var_type in {"chungus", "chudeluxe"}:
        return parse_expression(tokens, index)

    elif var_type == "forsencd":
        return parse_expression_forsencd(tokens, index)

    elif var_type == "forsen":
        return parse_expression_forsen(tokens, index)
    
    elif var_type == "lwk":
        return parse_expression_lwk(tokens, index)

    else:
        error = f"Type Error: Invalid type for assignment."
        raise SemanticError(error, line)

def parse_expression_forsen(tokens, index):
    line = tokens[index].line
    print("🔹 Parsing forsencd expression.")
    if tokens[index].type == "IDENTIFIER" and tokens[index + 1].type == "OPPAR":
        func_name = tokens[index].value
        func_info = symbol_table.lookup_function(func_name)
        func_return_type = func_info["return_type"]
        func_params = func_info["params"]
        
        if func_return_type not in {"forsen"}:
            error = f"Type Error: Cannot use function '{func_name}' of type {func_return_type} in this expression."
            raise SemanticError(error, line)
        index += 1
        return parse_function_call(tokens, index, func_name, func_return_type, func_params)

    elif (
        tokens[index].type == "IDENTIFIER" and
        tokens[index + 1].type == "DOT" and
        tokens[index + 2].type == "IDENTIFIER"
    ):
        struct_instance = tokens[index].type 
        member_name = tokens[index + 2].value 
        index += 3 

        instance_info = symbol_table.lookup_variable(struct_instance)
        if isinstance(instance_info, str):
            raise SemanticError(f"Semantic Error: Struct instance '{struct_instance}' is not declared.", token.line)

        struct_name = instance_info["type"]
        struct_info = symbol_table.lookup_struct(struct_name)

        if member_name not in struct_info:
            raise SemanticError(f"Semantic Error: Struct '{struct_name}' has no member '{member_name}'.", token.line)

        expected_type = struct_info[member_name]["type"]

        if expected_type not in {"forsen"}:
            raise SemanticError(f"Type Error: Cannot use '{struct_instance}.{member_name}' of type {expected_type} in this expression.", token.line)

        return StructMemberAccessNode(struct_instance, member_name, expected_type, line=token.line), index
    
    elif tokens[index].type == "IDENTIFIER":
        variable_info = symbol_table.lookup_variable(tokens[index].value)
        if isinstance(variable_info, str):
            error = f"Semantic Error: Variable '{tokens[index].value}' used before declaration."
            raise SemanticError(error, line)
        
        if variable_info["type"] != "forsen":
            error = f"Type Error: Cannot use '{tokens[index].value}' of type {variable_info['type']} in forsen expression.", line
            raise SemanticError(error, line)

        node = ASTNode("Value", tokens[index].value)
        index += 1
        return node, index

    elif tokens[index].type == "FORSEN_LIT":
        node = ASTNode("Value", tokens[index].value)
        index += 1
        return node, index

    else:
        error = f"Type Error: forsen can only be assigned with identifier of type forsen or a forsen literal."
        raise SemanticError(error, line) 

def parse_expression_forsencd(tokens, index):
    line = tokens[index].line  

    if tokens[index].type not in {"FORSENCD_LIT", "IDENTIFIER"}:
        raise SemanticError(f"Type Error: forsencd can only be assigned a FORSENCD_LIT or an identifier of type forsen/forsencd.", line)

    if tokens[index].type == "IDENTIFIER" and tokens[index + 1].type == "OPPAR":
        func_name = tokens[index].value
        func_info = symbol_table.lookup_function(func_name)

        if isinstance(func_info, str):  # Function not found
            raise SemanticError(f"Semantic Error: Function '{func_name}' is not defined.", line)

        func_return_type = func_info["return_type"]
        if func_return_type not in {"forsen", "forsencd"}:
            raise SemanticError(f"Type Error: Cannot use function '{func_name}' of type '{func_return_type}' in this expression.", line)

        node, index = parse_function_call(tokens, index, func_name, func_return_type, func_info["params"])

    elif (
        tokens[index].type == "IDENTIFIER" and
        tokens[index + 1].type == "DOT" and
        tokens[index + 2].type == "IDENTIFIER"
    ):
        struct_instance = tokens[index].value 
        member_name = tokens[index + 2].value 
        index += 3 

        instance_info = symbol_table.lookup_variable(struct_instance)
        if isinstance(instance_info, str):
            raise SemanticError(f"Semantic Error: Struct instance '{struct_instance}' is not declared.", tokens[index].line)

        struct_name = instance_info["type"]
        struct_info = symbol_table.lookup_struct(struct_name)

        if member_name not in struct_info:
            raise SemanticError(f"Semantic Error: Struct '{struct_name}' has no member '{member_name}'.", tokens[index].line)

        expected_type = struct_info[member_name]["type"]

        if expected_type not in {"forsencd", "forsen"}:
            raise SemanticError(f"Type Error: Cannot use '{struct_instance}.{member_name}' of type {expected_type} in this expression.", tokens[index].line)

        struct_node = StructMemberAccessNode(struct_instance, member_name, expected_type, line=tokens[index].line)
        return struct_node, index
    
    
    elif tokens[index].type == "IDENTIFIER":
        var_name = tokens[index].value
        var_info = symbol_table.lookup_variable(var_name)

        if isinstance(var_info, str):  # Variable not found
            raise SemanticError(f"Semantic Error: Variable '{var_name}' used before declaration.", line)

        if var_info["type"] not in {"forsen", "forsencd"}:
            raise SemanticError(f"Type Error: Cannot use '{var_name}' of type {var_info['type']} in this expression.", line)

        node = ASTNode("Value", var_name, line=line)
        index += 1  

    elif tokens[index].type == "FORSENCD_LIT":
        node = ASTNode("Value", tokens[index].value, line=line)
        index += 1 

    left_node = node

    while index < len(tokens):
        if tokens[index].type == "PLUS":
            op = tokens[index].value  # Store '+'
            index += 1  # Move past '+'

            if tokens[index].type not in {"FORSENCD_LIT", "IDENTIFIER"}:
                raise SemanticError(f"Type Error: forsencd can only be assigned a FORSENCD_LIT or an identifier of type forsen/forsencd.", line)

            if tokens[index].type == "IDENTIFIER" and tokens[index + 1].type == "OPPAR":
                func_name = tokens[index].value
                func_info = symbol_table.lookup_function(func_name)

                if isinstance(func_info, str):  # Function not found
                    raise SemanticError(f"Semantic Error: Function '{func_name}' is not defined.", line)

                func_return_type = func_info["return_type"]
                if func_return_type not in {"forsen", "forsencd"}:
                    raise SemanticError(f"Type Error: Cannot use function '{func_name}' of type '{func_return_type}' in this expression.", line)

                right_node, index = parse_function_call(tokens, index, func_name, func_return_type, func_info["params"])

            elif (
                tokens[index].type == "IDENTIFIER" and
                tokens[index + 1].type == "DOT" and
                tokens[index + 2].type == "IDENTIFIER"
            ):
                struct_instance = tokens[index].value 
                member_name = tokens[index + 2].value 
                index += 3 

                instance_info = symbol_table.lookup_variable(struct_instance)
                if isinstance(instance_info, str):
                    raise SemanticError(f"Semantic Error: Struct instance '{struct_instance}' is not declared.", tokens[index].line)

                struct_name = instance_info["type"]
                struct_info = symbol_table.lookup_struct(struct_name)

                if member_name not in struct_info:
                    raise SemanticError(f"Semantic Error: Struct '{struct_name}' has no member '{member_name}'.", tokens[index].line)

                expected_type = struct_info[member_name]["type"]

                if expected_type not in {"forsencd", "forsen"}:
                    raise SemanticError(f"Type Error: Cannot use '{struct_instance}.{member_name}' of type {expected_type} in this expression.", tokens[index].line)

                struct_node = StructMemberAccessNode(struct_instance, member_name, expected_type, line=tokens[index].line)
                return struct_node, index

            elif tokens[index].type == "IDENTIFIER":
                var_name = tokens[index].value
                var_info = symbol_table.lookup_variable(var_name)

                if isinstance(var_info, str):  # Variable not found
                    raise SemanticError(f"Semantic Error: Variable '{var_name}' used before declaration.", line)

                if var_info["type"] not in {"forsen", "forsencd"}:
                    raise SemanticError(f"Type Error: Cannot use '{var_name}' of type {var_info['type']} in this expression.", line)

                right_node = ASTNode("Value", var_name, line=line)
                index += 1 

            elif tokens[index].type == "FORSENCD_LIT":
                right_node = ASTNode("Value", tokens[index].value, line=line)
                index += 1  

            left_node = BinaryOpNode(left_node, op, right_node, line=line)

        elif tokens[index].type not in {"PLUS", "COMMA", "NL", "CLPAR", "CLBRA"}:
            raise SemanticError(f"Semantic Error: Unexpected token '{tokens[index].value}' in forsencd expression.", line)

        else:
            break

    return left_node, index 


def parse_expression(tokens, index):
    """Parses an expression with right-to-left associativity for + and -."""
    right_node, index = parse_term(tokens, index)

    if tokens[index].type in {"PLUS", "MINUS"}:
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

    if (tokens[index-1].type not in {"IDENTIFIER", "CHU_LIT", "CHUDEL_LIT", "PLUS", "MINUS", "MUL", "DIV", "MOD"} and
        token.type == "OPPAR" and
        tokens[index + 1].value in {"chungus", "chudeluxe"} and
        tokens[index + 2].type == "CLPAR"
    ):
        target_type = tokens[index + 1].value 
        index += 3
        expr_node, index = parse_factor(tokens, index)

        cast_node = CastNode(target_type, expr_node, line=token.line)
        return cast_node, index
    
    elif token.type in {"CHU_LIT", "CHUDEL_LIT"}:
        node = ASTNode("Value", token.value)
        index += 1  

        if tokens[index].type in {"INC", "DEC"}:
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

        node, index = parse_function_call(tokens, index, func_name, func_return_type, func_params)

        return node, index

    elif (
        tokens[index].type == "IDENTIFIER" and
        tokens[index + 1].type == "DOT" and
        tokens[index + 2].value == "ts"
    ):
        identifier = tokens[index].value

        identifier_info = symbol_table.lookup_variable(identifier)
        if isinstance(identifier_info, str):
            raise SemanticError(f"Semantic Error: Variable '{identifier}' used before declaration.", token.line)  

        if not identifier_info["is_list"] and identifier_info["type"] != "forsencd":
            raise SemanticError(f"Type Error: ts() can only be used on lists or strings, but '{identifier}' is of type {identifier_info['type']}.", token.line)
        
        index += 5

        ts_node, index = TSNode(identifier, line=token.line), index
        return ts_node, index

    elif (
        token.type == "IDENTIFIER" and
        tokens[index + 1].type == "DOT" and
        tokens[index + 2].type == "IDENTIFIER"
    ):
        struct_instance = token.value 
        member_name = tokens[index + 2].value 
        index += 3 

        instance_info = symbol_table.lookup_variable(struct_instance)
        if isinstance(instance_info, str):
            raise SemanticError(f"Semantic Error: Struct instance '{struct_instance}' is not declared.", token.line)

        struct_name = instance_info["type"]
        struct_info = symbol_table.lookup_struct(struct_name)

        if member_name not in struct_info:
            raise SemanticError(f"Semantic Error: Struct '{struct_name}' has no member '{member_name}'.", token.line)

        expected_type = struct_info[member_name]["type"]

        if expected_type not in {"chungus", "chudeluxe"}:
            raise SemanticError(f"Type Error: Cannot use '{struct_instance}.{member_name}' of type {expected_type} in this expression.", token.line)

        struct_node = StructMemberAccessNode(struct_instance, member_name, expected_type, line=token.line)
        return struct_node, index

    elif token.type in {"IDENTIFIER"}:
        variable_info = symbol_table.lookup_variable(token.value)
        if isinstance(variable_info, str):
            raise SemanticError(f"Semantic Error: Variable '{token.value}' used before declaration.", token.line)
        
        if variable_info["type"] not in {"chungus", "chudeluxe"}:
            error = f"Type Error: Cannot use '{token.value}' of type {variable_info['type']} in this expression."
            raise SemanticError(error, token.line)
        
        node = ASTNode("Value", token.value)
        index += 1  

        if tokens[index].type in {"INC", "DEC"}:
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
        error = f"Semantic Error: Invalid factor '{token.value}' in expression."
        raise SemanticError(error, token.line)

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
    token = tokens[index]

    if tokens[index].type in {"IDENTIFIER"} and tokens[index + 1].type == "OPPAR":
        if isinstance(symbol_table.lookup_function(token.value), str):
            error = f"Semantic Error: Function '{token.value}' used before declaration."
            raise SemanticError(error, line)
        
    elif (
        token.type == "IDENTIFIER" and
        tokens[index + 1].type == "DOT" and
        tokens[index + 2].type == "IDENTIFIER"
    ):
        struct_instance = token.value 
        member_name = tokens[index + 2].value 
        index += 3 

        instance_info = symbol_table.lookup_variable(struct_instance)
        if isinstance(instance_info, str):
            raise SemanticError(f"Semantic Error: Struct instance '{struct_instance}' is not declared.", token.line)

        struct_name = instance_info["type"]
        struct_info = symbol_table.lookup_struct(struct_name)

        if member_name not in struct_info:
            raise SemanticError(f"Semantic Error: Struct '{struct_name}' has no member '{member_name}'.", token.line)

        expected_type = struct_info[member_name]["type"]

        if expected_type not in {"lwk"}:
            raise SemanticError(f"Type Error: Cannot use '{struct_instance}.{member_name}' of type {expected_type} in this expression.", token.line)

        struct_node = StructMemberAccessNode(struct_instance, member_name, expected_type, line=token.line)
        return struct_node, index
    
    elif tokens[index].type == "IDENTIFIER":
        if isinstance(symbol_table.lookup_variable(token.value), str):
            error = f"Semantic Error: Variable '{token.value}' used before declaration."
            raise SemanticError(error, line)

    if token.type == "LWK_LIT" or (token.type == "IDENTIFIER" and tokens[index + 1].type == "OPPAR" and symbol_table.lookup_function(token.value)["return_type"] in {"lwk"}) or (token.type == "IDENTIFIER" and symbol_table.lookup_variable(token.value)["type"] in {"lwk"}):
        left_node = ASTNode("Value", tokens[index].value, line=line)
        index += 1  # Move past LWK_LIT

        if tokens[index].value in {"EQ", "NE"}:
            operator = tokens[index].value
            index += 1

            if tokens[index].type == "LWK_LIT" or (token.type == "IDENTIFIER" and tokens[index + 1].type == "OPPAR" and symbol_table.lookup_function(token.value)["return_type"] in {"lwk"}) or (token.type == "IDENTIFIER" and symbol_table.lookup_variable(token.value)["type"] in {"lwk"}):
                right_node = ASTNode("Value", tokens[index].value, line=line)
                index += 1
                return BinaryOpNode(left_node, operator, right_node, line=line), index
            
            elif tokens[index].type in {"IDENTIFIER"} and tokens[index + 1].type == "OPPAR":
                func_name = tokens[index].value
                func_info = symbol_table.lookup_function(func_name)
                func_return_type = func_info["return_type"]
                func_params = func_info["params"]
                if func_return_type not in {"lwk"}:
                    error = f"Type Error: Cannot use function '{func_name}' of type {func_return_type} in this expression."
                    raise SemanticError(error, line)
                right_node, index = parse_function_call(tokens, index, func_name, func_return_type, func_params)
                return BinaryOpNode(left_node, operator, right_node, line=line), index

            elif (
                token.type == "IDENTIFIER" and
                tokens[index + 1].type == "DOT" and
                tokens[index + 2].type == "IDENTIFIER"
            ):
                struct_instance = token.value 
                member_name = tokens[index + 2].value 
                index += 3 

                instance_info = symbol_table.lookup_variable(struct_instance)
                if isinstance(instance_info, str):
                    raise SemanticError(f"Semantic Error: Struct instance '{struct_instance}' is not declared.", token.line)

                struct_name = instance_info["type"]
                struct_info = symbol_table.lookup_struct(struct_name)

                if member_name not in struct_info:
                    raise SemanticError(f"Semantic Error: Struct '{struct_name}' has no member '{member_name}'.", token.line)

                expected_type = struct_info[member_name]["type"]

                if expected_type not in {"lwk"}:
                    raise SemanticError(f"Type Error: Cannot use '{struct_instance}.{member_name}' of type {expected_type} in this expression.", token.line)

                struct_node = StructMemberAccessNode(struct_instance, member_name, expected_type, line=token.line)
                return struct_node, index

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

    else:
        left_node, index = parse_expression(tokens, index)

        if tokens[index].type in {"LT", "GT", "LE", "GE", "EQ", "NE"}:
            operator = tokens[index].value
            index += 1
            right_node, index = parse_expression(tokens, index)

            if right_node.node_type == "Value" and right_node.value in {"true", "false"}:
               raise SemanticError(f"Type Error: Relational operators can only be used with numeric expressions, not boolean values.", line)
            
        else:
            error = f"Semantic Error: Invalid relational operator."
            raise SemanticError(error, line)

        return BinaryOpNode(left_node, operator, right_node, line=line), index

def parse_assignment(tokens, index, var_name, var_type):
    line = tokens[index].line
    global_var = symbol_table.variables.get(var_name)
    if global_var and global_var["is_sturdy"]:
        raise SemanticError(f"Semantic Error: Variable '{var_name}' is declared as sturdy.", line)
    
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
        
    elif tokens[index].value == "append":
        list_op_node, index = parse_append(tokens, index, var_name, var_type)
        return list_op_node, index
    
    elif tokens[index].value == "insert":
        list_op_node, index = parse_insert(tokens, index, var_name, var_type)
        return list_op_node, index
        
    elif tokens[index].value == "remove":
        list_op_node, index = parse_remove(tokens, index, var_name, var_type)
        return list_op_node, index 
        
    else:
        value_node, index = parse_expression_type(tokens, index, var_type)

    while tokens[index].type == "IS":
        index += 1
        next_var_name = tokens[index].value
        index += 1

        if not symbol_table.lookup_variable(next_var_name):
            raise SemanticError(f"Semantic Error: Variable '{next_var_name}' used before declaration.", line)

        value_node = AssignmentNode(next_var_name, value_node, line=line)

    assign_node = AssignmentNode(var_name, value_node, line=line)
    return assign_node, index

def parse_function_call(tokens, index, func_name, func_type, func_params):
    line = tokens[index].line
    
    index += 2  # Move past function name and '('
    print(tokens[index].type)
    args_node = ASTNode("Arguments")
    provided_args = []  
    expected_params = func_params  
    
    while tokens[index].type != "CLPAR":
        if len(provided_args) >= len(expected_params):
            raise SemanticError(f"Type Error: Too many arguments in function call '{func_name}'.", line)

        expected_type = expected_params[len(provided_args)].children[0].value 
        
        expr_node, index = parse_expression_type(tokens, index, expected_type)

        arg_node = ASTNode("Argument")
        arg_node.add_child(expr_node)
        args_node.add_child(arg_node)

        provided_args.append((arg_node, expected_type))

   
        if tokens[index].type == "COMMA":
            index += 1 

    index += 1 

    if tokens[index].type in {"INC", "DEC"}:
        raise SemanticError(f"Type Error: Unary operators cannot be applied to function calls.", line)

    if len(provided_args) != len(expected_params):
        raise SemanticError(f"Type Error: Function '{func_name}' expects {len(expected_params)} arguments, but {len(provided_args)} were provided.", line)

    for i, (arg_node, arg_type) in enumerate(provided_args):
        expected_type = expected_params[i].children[0].value  # Get expected type

        if expected_type in {"chungus", "chudeluxe"} and arg_type == "chungus":
            continue 
        
        if arg_type != expected_type:
            raise SemanticError(f"Type Error: Argument {i+1} of '{func_name}' should be '{expected_type}', but got '{arg_type}'.", line)

    return FunctionCallNode(func_name, args_node.children, line=line), index


def parse_argument(tokens, index):
    line = tokens[index].line

    if tokens[index].type == "IDENTIFIER":
        arg_name = tokens[index].value
        arg_info = symbol_table.lookup_variable(arg_name)
        if isinstance(arg_info, str):
            raise SemanticError(f"Semantic Error: Variable '{arg_name}' used before declaration.", line)
        
        arg_type = arg_info["type"]
        arg_node = ASTNode("Value", arg_name, line=line)
        index += 1

    else:
        raise SemanticError(f"Semantic Error: Invalid argument in function call.", line)

    return arg_node, arg_type, index
    
def parse_print(tokens, index):
    line = tokens[index].line
    index += 1

    if tokens[index].type != "OPPAR":
        raise SemanticError(f"Syntax Error: Expected '(' after yep statement.", line)
    index += 1

    args = []
    placeholder_count = 0

    if tokens[index].type == "FORSENCD_LIT":
        format_node, index, placeholder_count = parse_string_concatenation(tokens, index) 
        args.append(format_node)

    elif tokens[index].type == "IDENTIFIER":
        identif_name = tokens[index].value

        if tokens[index + 1].type == "OPPAR":
            func_name = identif_name
            func_info = symbol_table.lookup_function(func_name)
            if isinstance(func_info, str):
                raise SemanticError(f"Semantic Error: Function '{func_name}' is not defined.", line)
            if func_info["return_type"] in {"chungus", "chudeluxe"}:
                expr_node, index = parse_expression(tokens, index)
                args.append(expr_node)
            elif func_info["return_type"] in {"forsen"}:
                expr_node, index = parse_expression_forsen(tokens, index)
                args.append(expr_node)
            elif func_info["return_type"] in {"forsencd"}:
                expr_node, index = parse_expression_forsencd(tokens, index)
                args.append(expr_node)
            elif func_info["return_type"] in {"lwk"}:
                expr_node, index = parse_expression_lwk(tokens, index)
                args.append(expr_node)
            else:
                raise SemanticError(f"Type Error: Function '{func_name}' returns invalid type '{func_info['return_type']}'.", line)
        else:   
            arg_info = symbol_table.lookup_variable(identif_name)
            if isinstance(arg_info, str):
                raise SemanticError(f"Semantic Error: Variable '{identif_name}' used before declaration.", line)
            if arg_info["type"] in {"chungus", "chudeluxe"}:
                expr_node, index = parse_expression(tokens, index)
                args.append(expr_node)
            else:
                args.append(ASTNode("Value", identif_name, line=line))
                index += 1

    else:
        expr_node, index = parse_expression(tokens, index)
        args.append(expr_node)
    
    acutal_args = []
    while tokens[index].type == "COMMA":
        index += 1

        if tokens[index].type in {"CHU_LIT", "CHUDEL_LIT"}:
            arg_node, index = parse_expression(tokens, index)
            acutal_args.append(arg_node)

        elif tokens[index].type == "IDENTIFIER":
            arg_name = tokens[index].value
            arg_info = symbol_table.lookup_variable(arg_name)
            if arg_info["type"] in {"chungus", "chudeluxe"}:
                arg_node, index = parse_expression(tokens, index)
                acutal_args.append(arg_node)
            else:
                acutal_args.append(ASTNode("Value", arg_name, line=line))
                index += 1

        else:
            raise SemanticError(f"Syntax Error: Expected argument after ',' in yap statement.", line)

    if placeholder_count != len(acutal_args):
        raise SemanticError(f"Type Error: Expected {placeholder_count} arguments, but got {len(acutal_args)}.", line)
    
    args.extend(acutal_args)

    if tokens[index].type != "CLPAR":
        raise SemanticError(f"Syntax Error: Expected ')' after yap statement.", line)
    index += 1

    return PrintNode(args, line=line), index

def parse_string_concatenation(tokens, index):
    line = tokens[index].line
    if tokens[index].type != "FORSENCD_LIT":
        raise SemanticError(f"Semantic Error: String concatenation must start with a string literal.", line)
    
    format_string = tokens[index].value
    raw_string = format_string.replace("\\{", "").replace("\\}", "")
    print (raw_string.count("{"))
    if "{" in raw_string or "}" in raw_string:
        if raw_string.count("{") != raw_string.count("}"):
            raise SemanticError(f"Semantic Error: Invalid string literal '{format_string}' in yap().", line)
        if "{}" not in raw_string:
            raise SemanticError(f"Syntax Error: Placeholders {{}} must be adjacent within the string literal.", line)
        
    placeholder_count = raw_string.count("{}")
    left_node = ASTNode("FormattedString", tokens[index].value, line=line)
    index += 1

    while index < len(tokens) and tokens[index].type == "PLUS":
        index += 1
        if tokens[index].type != "FORSENCD_LIT":
            raise SemanticError(f"Semantic Error: Only string literals can be concatenated in yap().", line)

        format_string = tokens[index].value
        raw_string = format_string.replace("\\{", "").replace("\\}", "")
        
        if "{" in raw_string or "}" in raw_string:
            if raw_string.count("{") != raw_string.count("}"):
                raise SemanticError(f"Semantic Error: Invalid string literal '{format_string}' in yap().", line)
            if "{}" not in raw_string:
                raise SemanticError(f"Syntax Error: Placeholders {{}} must be adjacent within the string literal.", line)
        
        placeholder_count += raw_string.count("{}")
        right_node = ASTNode("FormattedString", tokens[index].value, line=line)
        index += 1

        left_node = BinaryOpNode(left_node, "+", right_node, line=line)

    return left_node, index, placeholder_count


def parse_sturdy(tokens, index):
    token = tokens[index]
    line = token.line
    index += 1 
    if tokens[index].value not in {"chungus", "chudeluxe", "forsen", "forsencd", "lwk"}:
        raise SemanticError(f"Semantic Error: Invalid sturdy variable type '{tokens[index].value}'.", line)
    
    var_type = tokens[index].value
    index += 1  

    if tokens[index].type != "IDENTIFIER":
        raise SemanticError(f"Syntax Error: Expected identifier after '{var_type}'.", line)
    
    var_name = tokens[index].value
    index += 1

    if tokens[index].type != "IS":
        raise SemanticError(f"Semantic Error: Sturdy variables must be initialized.", line)
    index += 1

    expected_literals = {
        "chungus": "CHU_LIT",
        "chudeluxe": "CHUDEL_LIT",
        "forsen": "FORSEN_LIT",
        "forsencd": "FORSENCD_LIT",
        "lwk": "LWK_LIT"
    }
    
    if tokens[index].type != expected_literals[var_type]:
        raise SemanticError(f"Type Error: '{var_name}' must be initialized with a {var_type} literal.", line)

    value_node = ASTNode("Value", tokens[index].value, line=line)
    index += 1

    if tokens[index].type not in {"NL"}:
        raise SemanticError(f"Semantic Error: Sturdy variable '{var_name}' must be assigned only a single literal.", line)

    error = symbol_table.declare_variable(var_name, var_type, value=value_node, is_list=False, is_sturdy=True)
    if isinstance(error, str):
        raise SemanticError(error, line)

    return SturdyDeclarationNode(var_type, var_name, value_node, line=line), index

def parse_if(tokens, index):
    line = tokens[index].line
    index += 1  # Move past "tuah"

    if tokens[index].type != "OPPAR":
        raise SemanticError(f"Syntax Error: Expected '(' after 'tuah'.", line)
    index += 1  # Move past '('

    condition_expr, index = parse_expression_lwk(tokens, index)  # Parse lwk expression

    if tokens[index].type != "CLPAR":
        raise SemanticError(f"Syntax Error: Expected ')' after 'tuah' condition.", line)
    index += 1  # Move past ')'

    symbol_table.enter_scope()
    
    condition_node = ASTNode("Condition", line=line)
    condition_node.add_child(condition_expr)

    if_node = IfStatementNode(condition_node, line=line)
    
    if tokens[index].type == "OPCUR":
        index += 1

        block_node = ASTNode("Block", line=line)

        while tokens[index].type != "CLCUR":
            stmt, index = parse_statement(tokens, index)
            if stmt:
                block_node.add_child(stmt)
            index += 1

        index += 1
        symbol_table.exit_scope()
        if_node.add_child(block_node)

    else:
        raise SemanticError(f"Syntax Error: Expected '{{' after 'tuah' condition.", line)

    index += 1

    while tokens[index].value == "hawk" and tokens[index + 1].value == "tuah":
        index += 2
        if tokens[index].type != "OPPAR":
            raise SemanticError(f"Syntax Error: Expected '(' after 'tuah'.", line)
        index += 1  # Move past '('

        elseif_node = ASTNode("ElseIfStatement", line=line)
        
        elseif_condition_expr, index = parse_expression_lwk(tokens, index)

        if tokens[index].type != "CLPAR":
            raise SemanticError(f"Syntax Error: Expected ')' after 'tuah' condition.", line)
        index += 1  # Move past ')'

        symbol_table.enter_scope()
        
        elseif_condition_node = ASTNode("Condition", line=line)
        elseif_condition_node.add_child(elseif_condition_expr)
        elseif_node.add_child(elseif_condition_node)
        
        if tokens[index].type == "OPCUR":
            index += 1

            elseif_block_node = ASTNode("Block", line=line)

            while tokens[index].type != "CLCUR":
                stmt, index = parse_statement(tokens, index)
                if stmt:
                    elseif_block_node.add_child(stmt)
                index += 1

            elseif_node.add_child(elseif_block_node)
            index += 1

            symbol_table.exit_scope()
            if_node.add_child(elseif_node)

        else:
            raise SemanticError(f"Syntax Error: Expected '{{' after 'tuah' condition.", line)

        index += 1

    if tokens[index].value == "hawk" and tokens[index + 1].value not in {"tuah", "{"}:
        raise SemanticError(f"Syntax Error: Unexpected token after 'hawk'", line)
    
    if tokens[index].value == "hawk":
        index += 1

        if tokens[index].type == "OPCUR":
            index += 1
            symbol_table.enter_scope()

            else_node = ASTNode("ElseStatement", line=line)
            else_block_node = ASTNode("Block", line=line)

            while tokens[index].type != "CLCUR":
                stmt, index = parse_statement(tokens, index)
                if stmt:
                    else_block_node.add_child(stmt)
                index += 1

        index += 1
        symbol_table.exit_scope()
        else_node.add_child(else_block_node)
        if_node.add_child(else_node)
    
    return if_node, index


def parse_return(tokens, index, func_type):
    line = tokens[index].line
    index += 1

    if func_type == "nocap":
        if tokens[index].type not in {"NL", "CLCUR"}:
            raise SemanticError(f"Type Error: nocap function must not return any value.", line)
        return ReturnNode(None, line=line), index

    elif tokens[index].type in {"CHU_LIT", "CHUDEL_LIT", "FORSEN_LIT", "FORSENCD_LIT", "LWK_LIT"}:
        return_expr = ASTNode("Value", tokens[index].value, line=line)
        index += 1

    elif tokens[index].type == "IDENTIFIER":
        identifier = tokens[index].value
        index += 1

        if tokens[index].type == "OPPAR":
            index -= 1
            func_info = symbol_table.lookup_function(identifier)

            if isinstance(func_info, str):  # Function not found
                raise SemanticError(f"Semantic Error: Function '{identifier}' is not defined.", line)

            return_type = func_info["return_type"]
            if return_type != func_type:
                raise SemanticError(f"Type Error: Function '{identifier}' returns '{return_type}', but expected '{func_type}'.", line)

            return_expr, index = parse_function_call(tokens, index, identifier, return_type, func_info["params"])

        else:
            var_info = symbol_table.lookup_variable(identifier)
            if isinstance(var_info, str):
                raise SemanticError(f"Semantic Error: Variable '{identifier}' used before declaration.", line)

            if var_info["type"] != func_type:
                raise SemanticError(f"Type Error: Variable '{identifier}' is of type '{var_info['type']}', expected '{func_type}'.", line)
            index -= 1 
            return_expr, index = parse_expression_type(tokens, index, func_type)

    else: 
        return_expr, index = parse_expression_type(tokens, index, func_type)

    return ReturnNode(return_expr, line=line), index


def parse_for(tokens, index):
    line = tokens[index].line
    index += 1

    if tokens[index].type != "OPPAR":
        raise SemanticError(f"Syntax Error: Expected '(' after 'plug'.", line)
    index += 1

    if tokens[index].type == "IDENTIFIER":
        identifier_name = tokens[index].value
        var_info = symbol_table.lookup_variable(identifier_name)
        if isinstance(var_info, str):
            raise SemanticError(f"Semantic Error: Variable '{identifier_name}' used before declaration.", line)
        index += 1
        if tokens[index].type != "IS":
            raise SemanticError(f"Syntax Error: Expected '=' after for loop identifier.", line)
        index += 1
        initialization, index = parse_assignment(tokens, index, identifier_name, var_info["type"])
        

    if tokens[index].type != "SEMICOL":
        raise SemanticError(f"Syntax Error: Expected ';' after for loop initialization.", line)
    index += 1

    condition, index = parse_expression_lwk(tokens, index)

    condition_node = ASTNode("Condition", line=line)
    condition_node.add_child(condition)

    if tokens[index].type != "SEMICOL":
        raise SemanticError(f"Syntax Error: Expected ';' after for loop condition.", line)
    index += 1

    update, index = parse_update(tokens, index)

    if tokens[index].type != "CLPAR":
        raise SemanticError(f"Syntax Error: Expected ')' after for loop update.", line)
    index += 1

    symbol_table.enter_scope()

    for_node = ForLoopNode(initialization, condition_node, update, line=line)

    if tokens[index].type == "OPCUR":
        index += 1

        block_node = ASTNode("Block", line=line)

        while tokens[index].type != "CLCUR":

            if tokens[index].value == "pause":
                index += 1
                cont_node = ContinueNode(line)
                block_node.add_child(cont_node)

            elif tokens[index].value == "getout":
                index += 1
                break_node = BreakNode(line)
                block_node.add_child(break_node)

            stmt, index = parse_statement(tokens, index)
            if stmt:
                block_node.add_child(stmt)
            
            index += 1

        index += 1
        symbol_table.exit_scope()

        for_node.add_child(block_node)
    
    else:
        raise SemanticError(f"Syntax Error: Expected '{{' after for loop condition.", line)
    
    return for_node, index

def parse_update(tokens, index):
    line = tokens[index].line

    if tokens[index].type == "IDENTIFIER":
        var_name = symbol_table.lookup_variable(tokens[index].value)
        if isinstance(var_name, str):
            raise SemanticError(f"Semantic Error: Variable '{var_name}' used before declaration.", line)
        operand = ASTNode("Identifier", tokens[index].value, line=line)

        index += 1

        if tokens[index].type in {"INC", "DEC"}:
            operator = tokens[index].value
            index += 1
            return UpdateNode(operator, operand, prefix = False, line=line), index
    
    elif tokens[index].type in {"INC", "DEC"}:
        operator = tokens[index].value
        index += 1

        if tokens[index].type == "IDENTIFIER":
            var_name = symbol_table.lookup_variable(tokens[index].value)
            if isinstance(var_name, str):
                raise SemanticError(f"Semantic Error: Variable '{var_name}' used before declaration.", line)
            
            operand = ASTNode("Identifier", tokens[index].value, line=line)
            index += 1

            return UpdateNode(operator, operand, prefix = True, line=line), index
        
    raise SemanticError(f"Semantic Error: Invalid update statement.", line)
    
def parse_while(tokens, index):
    line = tokens[index].line
    index += 1

    if tokens[index].type != "OPPAR":
        raise SemanticError(f"Syntax Error: Expected '(' after 'while'.", line)
    index += 1

    condition, index = parse_expression_lwk(tokens, index)

    if tokens[index].type != "CLPAR":
        raise SemanticError(f"Syntax Error: Expected ')' after 'while' condition.", line)
    index += 1

    symbol_table.enter_scope()

    condition_node = ASTNode("Condition", line=line)
    condition_node.add_child(condition)
    while_node = WhileLoopNode(condition_node, line=line)

    if tokens[index].type == "OPCUR":
        index += 1

        block_node = ASTNode("Block", line=line)

        while tokens[index].type != "CLCUR":

            if tokens[index].value == "pause":
                index += 1
                cont_node = ContinueNode(line)
                block_node.add_child(cont_node)

            elif tokens[index].value == "getout":
                index += 1
                break_node = BreakNode(line)
                block_node.add_child(break_node)

            stmt, index = parse_statement(tokens, index)
            if stmt:
                block_node.add_child(stmt)

            index += 1

        index += 1
        symbol_table.exit_scope()

        while_node.add_child(block_node)
    
    else:
        raise SemanticError(f"Syntax Error: Expected '{{' after 'while' condition.", line)
    
    return while_node, index

def parse_do(tokens, index):
    line = tokens[index].line
    index += 1

    symbol_table.enter_scope()

    if tokens[index].type != "OPCUR":
        raise SemanticError(f"Syntax Error: Expected '{{' after 'do'.", line)
    index += 1

    block_node = ASTNode("Block", line=line)

    while tokens[index].type != "CLCUR":

        if tokens[index].value == "pause":
            index += 1
            cont_node = ContinueNode(line)
            block_node.add_child(cont_node)

        elif tokens[index].value == "getout":
            index += 1
            break_node = BreakNode(line)
            block_node.add_child(break_node)


        stmt, index = parse_statement(tokens, index)
        if stmt:
            block_node.add_child(stmt)
        
        index += 1
        
        

    index += 1

    if tokens[index].value != "jit":
        raise SemanticError(f"Syntax Error: Expected 'jit' after 'do' block.", line)
    index += 1

    if tokens[index].type != "OPPAR":
        raise SemanticError(f"Syntax Error: Expected '(' after 'jit'.", line)
    index += 1

    condition, index = parse_expression_lwk(tokens, index)

    if tokens[index].type != "CLPAR":
        raise SemanticError(f"Syntax Error: Expected ')' after 'jit' condition.", line)
    index += 1

    do_node = DoWhileLoopNode(condition, line=line)

    condition_node = ASTNode("Condition", line=line)
    condition_node.add_child(condition)

    do_node.add_child(block_node)
    do_node.add_child(condition_node)

    symbol_table.exit_scope()
    return do_node, index

def parse_switch(tokens, index):
    line = tokens[index].line
    index += 1

    if tokens[index].type != "OPPAR":
        raise SemanticError(f"Syntax Error: Expected '(' after 'switch'.", line)
    index += 1

    switch_expr, index = parse_expression(tokens, index)

    if tokens[index].type != "CLPAR":
        raise SemanticError(f"Syntax Error: Expected ')' after 'switch' expression.", line)
    index += 1

    if tokens[index].type != "OPCUR":
        raise SemanticError(f"Syntax Error: Expected '{{' after 'switch' expression.", line)
    index += 1
    
    symbol_table.enter_scope()

    case_nodes = []
    default_case = None

    while tokens[index].type == "NL":
        index += 1

    while tokens[index].value == "caseoh":
        case_line = tokens[index].line
        index += 1
        line = tokens[index].line

        if tokens[index].type not in {"FORSENCD_LIT", "FORSEN_LIT", "LWK_LIT", "CHU_LIT", "CHUDEL_LIT"}:
            raise SemanticError(f"Semantic Error: Expected a valid literal value after 'caseoh'.", line)
        
        case_value = ASTNode("CaseValue", tokens[index].value, line=case_line)
        index += 1

        if tokens[index].type != "COLON":
            raise SemanticError(f"Syntax Error: Expected ':' after 'caseoh' value.", line)
        index += 1

        case_block = ASTNode("Block", line=case_line)

        while tokens[index].value != "getout":
            line = tokens[index].line
            stmt, index = parse_statement(tokens, index)
            if stmt:
                case_block.add_child(stmt)
            index += 1

        index += 1

        print(tokens[index].value)
        while tokens[index].type == "NL":
            index += 1

        case_node = ASTNode("Case", line=case_line)
        case_node.add_child(case_value)
        case_node.add_child(case_block)
        case_nodes.append(case_node)
    
    
    line = tokens[index].line


    if tokens[index].value != "npc":
        raise SemanticError(f"Semantic Error: Expected 'npc' after switch cases.", line)

    if tokens[index].value == "npc":
        line = tokens[index].line
        index += 1
             
        if tokens[index].type != "COLON":
            raise SemanticError(f"Syntax Error: Expected ':' after 'npc'.", line)
        index += 1
        
        default_block = ASTNode("Block", line=line)

        while tokens[index].value != "getout":
            stmt, index = parse_statement(tokens, index)
            if stmt:
                default_block.add_child(stmt)
            index += 1

        if tokens[index].value == "getout":
            index += 1
            
        while tokens[index].type == "NL":
            index += 1

        default_case = ASTNode("DefaultCase", line=line)
        default_case.add_child(default_block)
        
    if tokens[index].type != "CLCUR":
        raise SemanticError(f"Syntax Error: Expected '}}' after switch statement.", line)
        
    index += 1

    symbol_table.exit_scope()

    return SwitchNode(switch_expr, case_nodes, default_case, line=line), index

def parse_list(tokens, index, expected_type):
    line = tokens[index].line
    if tokens[index].type != "OPBRA":
        raise SemanticError(f"Semantic Error: Expected '[' for list declaration.", line)
    index += 1
    
    elements = []

    if tokens[index].type == "CLBRA":
        index += 1
        return ListNode(elements=[], line=line), index
    
    while tokens[index].type != "CLBRA":
        expr, index = parse_expression_type(tokens, index, expected_type)
        elements.append(expr)

        if tokens[index].type == "COMMA":
            index += 1
    
    if tokens[index].type != "CLBRA":
        raise SemanticError(f"Syntax Error: Expected ']' after list elements.", line)

    index += 1

    return ListNode(elements = elements, line = line), index

def parse_append(tokens, index, var_name, expected_type):

    line = tokens[index].line
    if symbol_table.lookup_variable(var_name)["is_list"] == False:
        raise SemanticError(f"Semantic Error: Variable '{var_name}' is not a list.", line)
    
    if tokens[index].value != "append":
        raise SemanticError(f"Semantic Error: Expected 'append'.", line)
    
    index += 1
    if tokens[index].type != "OPPAR":
        raise SemanticError(f"Syntax Error: Expected '(' after 'append'.", line)
    index += 1

    elements = []
    while tokens[index].type != "CLPAR":
        elem, index = parse_expression_type(tokens, index, expected_type)
        elements.append(elem)

        if tokens[index].type == "COMMA":
            index += 1

    if tokens[index].type != "CLPAR":
        raise SemanticError(f"Syntax Error: Expected ')' after append arguments.", line)
    index += 1  # Move past `)`

    return AppendNode(elements, line=line), index

def parse_insert(tokens, index, var_name, expected_type):
    line = tokens[index].line
    if symbol_table.lookup_variable(var_name)["is_list"] == False:
        raise SemanticError(f"Semantic Error: Variable '{var_name}' is not a list.", line)
    
    if tokens[index].value != "insert":
        raise SemanticError(f"Semantic Error: Expected 'insert'.", line)

    index += 1
    if tokens[index].type != "OPPAR":
        raise SemanticError(f"Syntax Error: Expected '(' after 'insert'.", line)
    index += 1

    if tokens[index].type != "CHU_LIT":
        raise SemanticError(f"Semantic Error: Expected chungus literal as index in 'insert'.", line)
    index_value = tokens[index].value
    index += 1

    if tokens[index].type != "COMMA":
        raise SemanticError(f"Syntax Error: Expected ',' after index in 'insert'.", line)
    index += 1  # Move past `,`

    elements = []

    while tokens[index].type != "CLPAR":
        elem, index = parse_expression_type(tokens, index, expected_type)
        elements.append(elem)

        if tokens[index].type == "COMMA":
            index += 1

    if tokens[index].type != "CLPAR":
        raise SemanticError(f"Syntax Error: Expected ')' after insert arguments.", line)
    index += 1

    return InsertNode(index_value, elements, line=line), index

def parse_remove(tokens, index, var_name, expected_type):
    line = tokens[index].line
    if symbol_table.lookup_variable(var_name)["is_list"] == False:
        raise SemanticError(f"Semantic Error: Variable '{var_name}' is not a list.", line)
    
    if tokens[index].value != "remove":
        raise SemanticError(f"Semantic Error: Expected 'remove'.", line)

    index += 1
    if tokens[index].type != "OPPAR":
        raise SemanticError(f"Syntax Error: Expected '(' after 'remove'.", line)
    index += 1

    if tokens[index].type == "CHU_LIT":
        value = tokens[index].value
        index += 1
        
    else:
        raise SemanticError(f"Semantic Error: Expected chungus literal or identifier as argument to 'remove'.", line)

    if tokens[index].type != "CLPAR":
        raise SemanticError(f"Syntax Error: Expected ')' after remove argument.", line)
    index += 1  # Move past `)`

    return RemoveNode(var_name, value, line=line), index

def parse_struct(tokens, index):
    line = tokens[index].line
    index += 1 

    if tokens[index].type != "IDENTIFIER":
        raise SemanticError(f"Semantic Error: Expected struct name after 'aura'.", line)

    struct_name = tokens[index].value
    index += 1

    if tokens[index].type != "OPCUR":  # Expect `{`
        raise SemanticError(f"Syntax Error: Expected '{{' to start struct body.", line)
    index += 1

    while tokens[index].type == "NL":
        index += 1

    members = []
    while tokens[index].type != "CLCUR":  # Until `}`
        line = tokens[index].line
        print(tokens[index].value)
        if tokens[index].value not in {"chungus", "chudeluxe", "forsen", "forsencd", "lwk"}:
            raise SemanticError(f"Semantic Error: Expected valid data type in struct declaration.", line)
        
        member_type = tokens[index].value
        index += 1

        if tokens[index].type != "IDENTIFIER":
            raise SemanticError(f"Semantic Error: Expected member variable name after data type.", line)

        member_name = tokens[index].value
        index += 1

        default_value = None

        if tokens[index].type == "IS":
            index += 1
            default_node, index = parse_expression_type(tokens, index, member_type)
            default_value = default_node.value

        member_node = ASTNode("Member", f"{member_type} {member_name}", line=line)

        if default_value:
            member_node.add_child(ASTNode("DefaultValue", default_value, line=line))

        members.append(member_node)

        
        if tokens[index].type == "NL":
            index += 1
        else:
            raise SemanticError(f"Syntax Error: Expected newline after struct member '{member_name}'.", line)

    index += 1  # Move past `}`

    symbol_table.declare_struct(struct_name, members)

    return StructNode(struct_name, members, line=line), index

def parse_struct_instance(tokens, index):
    line = tokens[index].line

    if tokens[index].value == "aura":
        index += 1 

    if tokens[index].type != "IDENTIFIER":
        raise SemanticError(f"Semantic Error: Expected struct name after 'aura'.", line)

    struct_name = tokens[index].value
    index += 1

    struct_info = symbol_table.lookup_struct(struct_name)
    if isinstance(struct_info, str):
        raise SemanticError(f"Semantic Error: Struct '{struct_name}' is not defined.", line)

 
    struct_instances = []
    while tokens[index].type == "IDENTIFIER":
        instance_name = tokens[index].value
        index += 1

       
        symbol_table.declare_variable(instance_name, struct_name, is_struct=True)

        struct_instances.append(StructInstanceNode(struct_name, instance_name, line=line))

        if tokens[index].type == "COMMA":
            index += 1
        else:
            break

    if len(struct_instances) == 1:
        return struct_instances[0], index
    else:
        struct_list_node = ASTNode("StructInstanceList")
        for instance in struct_instances:
            struct_list_node.add_child(instance)
        return struct_list_node, index

def parse_struct_member_assignment(tokens, index):
    line = tokens[index].line

    if tokens[index].type != "IDENTIFIER":
        raise SemanticError(f"Semantic Error: Expected struct instance name.", line)

    struct_instance = tokens[index].value  # e.g., `Rojo`
    index += 1

    if tokens[index].type != "DOT":
        raise SemanticError(f"Syntax Error: Expected '.' after struct instance '{struct_instance}'.", line)
    index += 1

    if tokens[index].type != "IDENTIFIER":
        raise SemanticError(f"Syntax Error: Expected struct member name after '.'.", line)

    member_name = tokens[index].value  # e.g., `num`
    index += 1

    if tokens[index].type != "IS":
        raise SemanticError(f"Syntax Error: Expected '=' in struct member assignment.", line)
    index += 1

    instance_info = symbol_table.lookup_variable(struct_instance)
    if isinstance(instance_info, str):
        raise SemanticError(f"Semantic Error: Struct instance '{struct_instance}' is not declared.", line)

    struct_name = instance_info["type"]
    struct_info = symbol_table.lookup_struct(struct_name)

    if member_name not in struct_info:
        raise SemanticError(f"Semantic Error: Struct '{struct_name}' has no member '{member_name}'.", line)

    expected_type = struct_info[member_name]["type"]


    value_node, index = parse_expression_type(tokens, index, expected_type)

    if isinstance(value_node, ASTNode) and value_node.node_type == "Value":
        final_value = value_node 
    else:
        final_value = value_node  

    return StructMemberAssignmentNode(struct_instance, member_name, final_value, line=line), index
