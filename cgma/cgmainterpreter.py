from cgmasemantic import ProgramNode, VariableDeclarationNode, AssignmentNode, BinaryOpNode, FunctionDeclarationNode, FunctionCallNode, IfStatementNode, ForLoopNode, WhileLoopNode, PrintNode, ListAccessNode

class SemanticError(Exception):
    def __init__(self, message,  line):
        super().__init__(message)
        self.message = f"Ln {line} {message}"

    def __str__(self):
        return self.message


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
        elif node.node_type == "Value":
            value = self._parse_literal(node.value)
            return value
        elif node.node_type == "FormattedString":
            return self.visit_formatted_string(node)
        else:
            raise Exception(f"Unknown AST node type: {node.node_type}")

    def visit_program(self, node):
        for child in node.children:
            self.interpret(child)

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

        if isinstance(value, str) and value in self.symbol_table.variables:
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
        if parameters_node and len(parameters_node.children) > 0:
            for param in parameters_node.children: 
                if not isinstance(param, parameters_node):
                    raise Exception(f"Invalid parameter: {param.value}")

        self.current_function = node
        self.visit_block(node.children[2])
        return_value = None

        if return_type != 'nocap':
            return_value = self.get_return_value()

        return return_value


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
                if isinstance(value, str) and value in self.symbol_table.variables:
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

