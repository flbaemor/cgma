from cgmasemantic import ProgramNode, VariableDeclarationNode, AssignmentNode, BinaryOpNode, FunctionDeclarationNode, FunctionCallNode, IfStatementNode, ForLoopNode, WhileLoopNode, PrintNode, UnaryOpNode, SturdyDeclarationNode, ReturnNode, UpdateNode, SwitchNode, ContinueNode, BreakNode, ListNode, TaperNode, TSNode, AppendNode, InsertNode, RemoveNode, CastNode, ListAccessNode

class SemanticError(Exception):
    def __init__(self, message,  line):
        super().__init__(message)
        self.message = f"Ln {line} {message}"

    def __str__(self):
        return self.message

class ReturnValue(Exception):
    def __init__(self, value):
        self.value = value

class InterpreterError(Exception):
    def __init__(self, message, line):
        super().__init__(f"[Line {line}] {message}")
        self.message = f"Ln {line} {message}"
    
    def __str__(self):
        return self.message

class Interpreter:
    def __init__(self, symbol_table):
        self.symbol_table = symbol_table
        self.output = []

    def interpret(self, node):
        if isinstance(node, ProgramNode):
            return self.visit_program(node)
        elif isinstance(node, VariableDeclarationNode):
            return self.visit_variable_declaration(node)
        elif isinstance(node, AssignmentNode):
            return self.visit_assignment(node)
        elif isinstance(node, BinaryOpNode):
            return self.visit_binary_op(node)
        elif isinstance(node, FunctionDeclarationNode):
            return self.visit_function_declaration(node)
        elif isinstance(node, PrintNode):
            return self.visit_print(node)
        elif isinstance(node, ListAccessNode):
            return self.visit_list_access(node)
        elif isinstance(node, ReturnNode):
            return self.visit_return(node)
        elif isinstance(node, FunctionCallNode):
            return self.visit_function_call(node)
        elif node.node_type == "Value":
            value = self._parse_literal(node.value)
            return value
        elif node.node_type == "FormattedString":
            return self.visit_formatted_string(node)
        elif node.node_type == "VariableDeclarationList":
            for child in node.children:
                self.visit_variable_declaration(child)
        elif node.node_type == "AssignmentList":
            for child in node.children:
                self.visit_assignment(child)
        else:
            raise Exception(f"Unknown AST node type: {node.node_type}")

    def visit_program(self, node):
        for child in node.children:
            self.interpret(child)

        main_call = FunctionCallNode("skibidi", [], node.line)
        return self.interpret(main_call)

    def visit_variable_declaration(self, node):
        var_type = node.children[0].value
        var_name = node.children[1].value
        value_node = node.children[2]
        
        if value_node:
            if value_node.node_type == "List":
                value = []
                for val in value_node.children:
                    item = self.interpret(val)
                    if var_type == "chungus":
                        if isinstance(item, float):
                            item = int(item)
                    elif var_type == "chudeluxe":
                        item = float(item)
                    value.append(item)

            else:
                value = self.interpret(value_node)
                if var_type == "chungus" and isinstance(value, float):
                    value = int(value)

        print(f"\nDeclaring variable '{var_name}' of type '{var_type}' with initial value: {value}")
        self.symbol_table.declare_variable(var_name, var_type, value)

    def visit_assignment(self, node):
        var_name = node.children[0].value
        var_type = self.symbol_table.lookup_variable(var_name)["type"]
        value_node = node.children[1]
        value = self.interpret(value_node)
        if var_type == "chungus":
            if isinstance(value, float):
                value = int(value)
        print(f"\nAssigning variable '{var_name}' of type '{var_type}' with value: {value}")
        self.symbol_table.lookup_variable(var_name)["value"] = value


    def visit_binary_op(self, node):
        left = self.interpret(node.children[0])
        right = self.interpret(node.children[1])
        operator = node.value

        left = self._parse_literal(left)
        right = self._parse_literal(right)

        if operator == '+' and (isinstance(left, str) or isinstance(right, str)):
            result = str(left) + str(right)
            return result

        try:
            if operator == '+':
                return left + right
            elif operator == '-':
                return left - right
            elif operator == '*':
                return left * right
            elif operator == '/':
                return left / right
            elif operator == '%':
                return left % right
            elif operator == '==':
                return left == right
            elif operator == '!=':
                return left != right
            elif operator == '<':
                return left < right
            elif operator == '<=':
                return left <= right
            elif operator == '>':
                return left > right
            elif operator == '>=':
                return left >= right
            elif operator == '&&':
                return bool(left) and bool(right)
            elif operator == '||':
                return bool(left) or bool(right)
            elif operator == '!':
                return not bool(left)
            elif operator == 'neg':
                return -left
            else:
                raise Exception(f"Unknown operator: {operator}")
        except Exception as e:
            raise Exception(f"Error applying operator '{operator}': {e}")

    def _parse_literal(self, value):

        if isinstance(value, str) and not isinstance(self.symbol_table.lookup_variable(value), str):
            value = self.symbol_table.lookup_variable(value)["value"]

        if isinstance(value, (int, float, bool)):
            return value

        if not isinstance(value, str):
            return value

        value = value.strip()

        if value.startswith('"') and value.endswith('"'):
            return value[1:-1]

        if value == 'true':
            return True
        if value == 'false':
            return False

        try:
            if '.' in value:
                return float(value)
            return int(value)
        except ValueError:
            return value 
    

    def visit_function_declaration(self, node):
        return_type = node.children[0].value 
        parameters_node = node.children[1]
        func_name = node.value

        params = []
        if parameters_node and len(parameters_node.children) > 0:
            for param in parameters_node.children:
                if not hasattr(param, 'node_type') or param.node_type != 'Parameter':
                    raise Exception(f"Invalid parameter: {param.value}")
                param_type = param.children[0].value
                param_name = param.children[1].value
                params.append({"name": param_name, "type": param_type})

        self.symbol_table.declare_function(func_name, return_type, params, node)

        return None

    def visit_block(self, block_node):
        for statement in block_node.children:
            self.interpret(statement)

    def yap(self, num):
        self.output.append(str(num))

    def visit_print(self, node):
        if not node.children:
            return

        first = node.children[0]

        evaluated_first = self.interpret(first)

        if isinstance(evaluated_first, str) and '{}' in evaluated_first:
            values = []
            for arg in node.children[1:]:
                value = self.interpret(arg)
                if isinstance(value, str) and not isinstance(self.symbol_table.lookup_variable(value), str):
                    value = self.symbol_table.lookup_variable(value)["value"]
                values.append(value)

            try:
                output_str = evaluated_first.format(*values)
            except Exception as e:
                raise Exception(f"Format error in yap(): '{evaluated_first}' with {values}: {e}")

            self.yap(output_str)
            return

        self.yap(str(evaluated_first))

    def visit_formatted_string(self, node):
        value = node.value
        if value.startswith('"') and value.endswith('"'):
            value = value[1:-1]

        # Escape sequences
        value = value.replace(r'\\', '\\')  # handle double backslash first
        value = value.replace(r'\n', '\n')
        value = value.replace(r'\t', '\t')
        value = value.replace(r'\"', '"')
        value = value.replace(r'\{', '{')
        value = value.replace(r'\}', '}')

        return value


    def visit_list_access(self, node):
        list_name = node.children[0].value
        index_node = node.children[1]

        list_entry = self.symbol_table.lookup_variable(list_name)
        list_value = list_entry["value"]

        index = self.interpret(index_node.children[0])

        if not isinstance(index, int):
            raise InterpreterError(f"Semantic Error: List index must be an integer. Got '{index}'", node.line)

        if index < 0 or index >= len(list_value):
            raise InterpreterError(f"Semantic Error: Index '{index}' out of bounds for list '{list_name}'.", node.line)

        return list_value[index]
    

    def visit_return(self, node):
        value = self.interpret(node.children[0]) if node.children else None
        raise ReturnValue(value)
    

    def visit_function_call(self, node):
        function_name = node.value
        args = [self.interpret(arg.children[0]) for arg in node.children]

        func_info = self.symbol_table.lookup_function(function_name)
        if isinstance(func_info, str):
            raise InterpreterError(func_info, node.line)

        return_type = func_info["return_type"]
        expected_params = func_info["params"]
        function_node = func_info["node"]

        if len(expected_params) != len(args):
            raise InterpreterError(
                f"Function '{function_name}' expects {len(expected_params)} argument(s), got {len(args)}.",
                node.line
            )

        self.symbol_table.scopes.append({})
        self.symbol_table.current_func_name = function_name

        try:
            for i, param in enumerate(expected_params):
                param_name = param["name"]
                param_type = param["type"]
                arg_value = args[i]

                self.symbol_table.declare_variable(param_name, param_type, arg_value)

            try:
                self.visit_block(function_node.children[2])  # Assuming block is always at index 2
            except ReturnValue as ret:
                return ret.value

            return None

        finally:
            self.symbol_table.scopes.pop()
            self.symbol_table.current_func_name = None



