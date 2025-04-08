from cgmasemantic import ProgramNode, VariableDeclarationNode, AssignmentNode, BinaryOpNode, FunctionDeclarationNode, FunctionCallNode, IfStatementNode, ForLoopNode, WhileLoopNode, PrintNode

class InterpreterError(Exception):
    def __init__(self, message, line):
        super().__init__(f"[Line {line}] {message}")
        self.line = line

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
        elif isinstance(node, FunctionCallNode):
            return self.visit_function_call(node)
        elif isinstance(node, IfStatementNode):
            return self.visit_if_statement(node)
        elif isinstance(node, ForLoopNode):
            return self.visit_for_loop(node)
        elif isinstance(node, WhileLoopNode):
            return self.visit_while_loop(node)
        elif isinstance(node, PrintNode):
            return self.visit_print(node)
        elif node.node_type == "Value":
            return node.value
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
            value = self.interpret(value_node)
        
        if var_type == "chungus":
            if isinstance(value, float):
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

        if left in self.symbol_table.variables:
            print(f"\nDEBUG: left: {left}")
            left = self.symbol_table.lookup_variable(left)["value"]

        if right in self.symbol_table.variables:
            right = self.symbol_table.lookup_variable(right)["value"]

        if isinstance(left, str) and left.startswith('"') and left.endswith('"'):
            left = str(left)
        elif left == 'true' or right == 'true':
            left = True
        elif left == 'false' or right == 'false':
            left = False
        elif isinstance (left, str) and left.isdigit():
            left = float(left)

        if isinstance(right,str) and right.startswith('"') and right.endswith('"'):
            right = str(right)
        elif right == 'true' or right == 'true':
            right = True
        elif right == 'false' or right == 'false':
            right = False
        elif isinstance (right, str) and right.isdigit():
            right = float(right)

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
            return left and right
        elif operator == '||':
            return left or right
        elif operator == '!':
            return not left
        elif operator == 'neg':
            return -left
        else:
            raise Exception(f"Unknown operator: {operator}")

        
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


    def visit_print(self, node):
        # Assuming the first child is a format string
        formatted_string = str(node.children[0].value)
        values = []
        
        for child in node.children:
            if isinstance(child, BinaryOpNode):
                value = self.interpret(child)
            else:
                if isinstance(child, str):
                    value = self.symbol_table.lookup_variable(child)["value"]
                else:
                    value = self.interpret(child)
            values.append(value)

        output_str = formatted_string.format(*values)
        
        self.yap(output_str)
        