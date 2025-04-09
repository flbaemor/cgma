from cgmasemantic import ProgramNode, VariableDeclarationNode, AssignmentNode, BinaryOpNode, FunctionDeclarationNode, FunctionCallNode, IfStatementNode, ForLoopNode, WhileLoopNode, PrintNode, UnaryOpNode, SturdyDeclarationNode, ReturnNode,  SwitchNode, ContinueNode, BreakNode, ListNode, TaperNode, TSNode, AppendNode, InsertNode, RemoveNode, CastNode, ListAccessNode, DoWhileLoopNode

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
        self.loop_stack = []
        self.break_flag = False
        self.continue_flag = False

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
        elif isinstance(node, ListNode):
            return self.visit_list(node)
        elif isinstance(node, ListAccessNode):
            return self.visit_list_access(node)
        elif isinstance(node, ReturnNode):
            return self.visit_return(node)
        elif isinstance(node, FunctionCallNode):
            return self.visit_function_call(node)
        elif isinstance(node, AppendNode):
            return self.visit_append(node)
        elif isinstance(node, InsertNode):
            return self.visit_insert(node)
        elif isinstance(node, RemoveNode):
            return self.visit_remove(node)
        elif isinstance(node, UnaryOpNode):
            return self.visit_unaryop(node)
        elif isinstance(node, SturdyDeclarationNode):
            return self.visit_sturdy_declaration(node)
        elif isinstance(node, CastNode):
            return self.visit_cast(node)
        elif isinstance(node, TaperNode):
            return self.visit_taper(node)
        elif isinstance(node, TSNode):
            return self.visit_ts(node)
        elif isinstance(node, IfStatementNode):
            return self.visit_if_statement(node)
        elif isinstance(node, ForLoopNode):
            return self.visit_for_loop(node)
        elif isinstance(node, WhileLoopNode):
            return self.visit_while_loop(node)
        elif isinstance(node, DoWhileLoopNode):
            return self.visit_do_while_loop(node)
        elif isinstance(node, BreakNode):
            return self.visit_break(node)
        elif isinstance(node, ContinueNode):
            return self.visit_continue(node)
        elif isinstance(node, SwitchNode):
            return self.visit_switch(node)
        elif node.node_type == "Input":
            return self.visit_input(node)
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
        is_list = False
        
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
                
                is_list = True

            else:
                value = self.interpret(value_node)
                if isinstance(value_node, TaperNode):
                    is_list = True
                if var_type == "chungus" and isinstance(value, float):
                    value = int(value)

        print(f"\nDeclaring variable '{var_name}' of type '{var_type}' with initial value: {value}")
        self.symbol_table.declare_variable(var_name, var_type, value, is_list=is_list)

    def visit_sturdy_declaration(self, node):
        var_type = node.children[0].value
        var_name = node.children[1].value
        value_node = node.children[2]
        value = self.interpret(value_node)
        self.symbol_table.declare_variable(var_name, var_type, value, is_list=False, is_struct=False,  is_sturdy=True)

    def visit_assignment(self, node):
        target_node = node.children[0]
        value_node = node.children[1]

        if value_node.node_type == "List":
            value = []
            for val in value_node.children:
                item = self.interpret(val)
                value.append(item)
        else:
            value = self.interpret(value_node)
            if isinstance(value_node, AppendNode) or isinstance(value_node, InsertNode) or isinstance(value_node, RemoveNode):
                return

        if target_node.node_type == "ListAccess":
            list_name = target_node.children[0].value
            index_node = target_node.children[1]
            index = self.interpret(index_node.children[0])

            if not isinstance(index, int):
                raise InterpreterError(f"Semantic Error: List index must be an integer. Got '{index}'", node.line)

            list_entry = self.symbol_table.lookup_variable(list_name)
            if isinstance(list_entry, str):
                raise InterpreterError(list_entry, node.line)

            list_value = list_entry["value"]
            if not isinstance(list_value, list):
                raise InterpreterError(f"Semantic Error: Variable '{list_name}' is not a list.", node.line)

            if index < 0 or index >= len(list_value):
                raise InterpreterError(f"Semantic Error: Index '{index}' out of bounds for list '{list_name}'.", node.line)

            print(f"\nUpdating list '{list_name}' at index {index} with value: {value}")
            list_value[index] = value

        else:
            var_name = target_node.value
            var_info = self.symbol_table.lookup_variable(var_name)
            if isinstance(var_info, str):
                raise InterpreterError(var_info, node.line)

            var_type = var_info["type"]
            if var_type == "chungus" and isinstance(value, float):
                value = int(value)

            self.symbol_table.set_variable(var_name, value)
            print(f"\nUpdating variable '{var_name}' of type '{var_type}' with value: {value}")


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
        value = value.replace(r'\\', '\\')
        value = value.replace(r'\n', '\n')
        value = value.replace(r'\t', '\t')
        value = value.replace(r'\"', '"')
        value = value.replace(r'\{', '{')
        value = value.replace(r'\}', '}')
        value = value.replace(r'\/', '/')
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
                f"Semantic Error: Function '{function_name}' expects {len(expected_params)} argument(s), got {len(args)}.",
                node.line
            )
        
        self.symbol_table.enter_scope()
        self.symbol_table.current_func_name = function_name

        try:
            for i, param in enumerate(expected_params):
                param_name = param["name"]
                param_type = param["type"]
                arg_value = args[i]

                self.symbol_table.declare_variable(param_name, param_type, arg_value)

            try:
                self.visit_block(function_node.children[2])
            except ReturnValue as ret:
                return ret.value

            return None

        finally:
            self.symbol_table.exit_scope()
            self.symbol_table.current_func_name = None


    def visit_append(self, node):
        list_name = node.parent.children[0].value
        list_info = self.symbol_table.lookup_variable(list_name)

        for child in node.children:
            value = self.interpret(child)
            list_info["value"].append(value)
            print(f"\nAppending value '{value}' to list '{list_name}'")

        
    def visit_insert(self, node):
        list_name = node.parent.children[0].value
        list_info = self.symbol_table.lookup_variable(list_name)

        index = self.interpret(node.children[0].children[0])

        if not isinstance(index, int):
            raise InterpreterError("Semantic Error: Insert index must be an integer", node.line)

        if index < 0 or index > len(list_info["value"]):
            raise InterpreterError(f"Semantic Error: Index {index} out of range for insert", node.line)

        for child in node.children[1:]:
            value = self.interpret(child)
            list_info["value"].insert(index, value)
            index += 1
            print(f"Inserted {value} at index {index} in list '{list_name}': {list_info['value']}")


    def visit_remove(self, node):
        list_name = node.children[0].value
        index_node = node.children[1].children[0]

        list_info = self.symbol_table.lookup_variable(list_name)
        if isinstance(list_info, str):
            raise InterpreterError(list_info, node.line)

        index = self.interpret(index_node)

        if not isinstance(index, int):
            raise InterpreterError("Semantic Error: Remove index must be an integer", node.line)

        if index < 0 or index >= len(list_info["value"]):
            raise InterpreterError(f"Semantic Error: Index {index} out of bounds for remove", node.line)

        removed = list_info["value"].pop(index)
        print(f"Removed value {removed} from list '{list_name}': {list_info['value']}")

    def visit_unaryop(self, node):
        operand_node = node.children[0]
        operand_name = operand_node.value
        var_info = self.symbol_table.lookup_variable(operand_name)

        if isinstance(var_info, str):
            raise InterpreterError(var_info, node.line)

        if node.value == "++":
            if node.position == "pre":
                new_value = var_info["value"] + 1
                self.symbol_table.set_variable(operand_name, new_value)
                return new_value
            else:  # post
                original = var_info["value"]
                new_value = original + 1
                self.symbol_table.set_variable(operand_name, new_value)
                return original

        elif node.value == "--":
            if node.position == "pre":
                new_value = var_info["value"] - 1
                self.symbol_table.set_variable(operand_name, new_value)
                return new_value
            else:
                original = var_info["value"]
                new_value = original - 1
                self.symbol_table.set_variable(operand_name, new_value)
                return original

        raise InterpreterError(f"Unknown unary operator {node.value}", node.line)
    
    def visit_cast(self, node):
        value = self.interpret(node.children[1])
        cast_type = node.children[0].value

        if cast_type == "chungus":
            return int(value)
        elif cast_type == "chudeluxe":
            return float(value)
        else:
            raise InterpreterError(f"Unknown cast type: {cast_type}", node.line)

    def visit_taper(self, node):
        var_name = node.children[0].value
        var_info = self.symbol_table.lookup_variable(var_name)
        
        if var_info["type"] == "forsencd":
            var_info["value"] = list(var_info["value"])
            var_info["is_list"] = True
            print(f"Tapered string '{var_name}' into list: {var_info['value']}")

        return var_info["value"]

    def visit_ts(self, node):
        var_name = node.children[0].value
        var_info = self.symbol_table.lookup_variable(var_name)

        if var_info["is_list"]:
            result = len(var_info["value"])
            print(f"Tapered list '{var_name}' to its length: {result}")
        
        elif var_info["type"] == "forsencd":
            result = len(var_info["value"])
            print(f"Tapered string '{var_name}' to its length: {result}")
        
        return result

    def visit_if_statement(self, node):
        condition_result = self.interpret(node.children[0].children[0])

        if not isinstance(condition_result, bool):
            raise InterpreterError(f"Semantic Error: Condition must be a boolean. Got '{condition_result}'", node.line)
        
        if condition_result:
            self.visit_block(node.children[1])
        
        else:
            current_node = 2
            while current_node < len(node.children):
                
                elif_node = node.children[current_node]

                if elif_node.node_type == "ElseIfStatement":
                    elif_condition_result = self.interpret(elif_node.children[0].children[0])

                    if not isinstance(elif_condition_result, bool):
                        raise InterpreterError(f"Semantic Error: Condition must be a boolean. Got '{condition_result}'", node.line)
                    
                    if elif_condition_result:
                        print(f"Executing ElseIf block: {elif_node.line}")
                        self.visit_block(elif_node.children[1])
                        return
                    
                elif elif_node.node_type == "ElseStatement":
                    print(f"Executing Else block: {elif_node.line}")
                    self.visit_block(elif_node.children[0])
                    return

                current_node += 1

        return None
    
    def visit_for_loop(self, node):
        self.enter_loop('for')
        instantiate_node = node.children[0]
        MAX_LOOP_ITERATIONS = 10000
        LOOP_COUNTER = 0

        if isinstance(instantiate_node, VariableDeclarationNode):
            var_type = instantiate_node.children[0].value
            var_name = instantiate_node.children[1].value
            initial_value_node = self.interpret(instantiate_node.children[2])
            self.symbol_table.declare_variable(var_name, var_type, initial_value_node)
        
        elif isinstance(instantiate_node, AssignmentNode):
            var_name = instantiate_node.children[0].value
            initial_value_node = self.interpret(instantiate_node.children[1])
            self.symbol_table.set_variable(var_name, initial_value_node)


        condition_node = node.children[1].children[0]
        condition_result = self.interpret(condition_node)

        if not isinstance(condition_result, bool):
            raise InterpreterError(f"Semantic Error: Condition must be a boolean. Got '{condition_result}'", node.line)

        while condition_result:
            LOOP_COUNTER += 1
            if LOOP_COUNTER > MAX_LOOP_ITERATIONS:
                raise InterpreterError("Runtime Error: Infinite loop detected!", node.line)

            block_node = node.children[3]
            self.visit_block(block_node)

            if self.break_triggered():
                break
            
            update_statements = node.children[2].children
            for update_expr in update_statements:
                self.interpret(update_expr)
            
            condition_result = self.interpret(condition_node)

        self.exit_loop()

    def visit_while_loop(self, node):
        self.enter_loop('while')
        MAX_LOOP_ITERATIONS = 10000
        LOOP_COUNTER = 0
        condition_node = node.children[0].children[0]
        condition_result = self.interpret(condition_node)

        if not isinstance(condition_result, bool):
            raise InterpreterError(f"Semantic Error: Condition must be a boolean. Got '{condition_result}'", node.line)

        while condition_result:
            LOOP_COUNTER += 1
            if LOOP_COUNTER > MAX_LOOP_ITERATIONS:
                raise InterpreterError("Runtime Error: Infinite loop detected!", node.line)
            
            
            block_node = node.children[1]
            self.visit_block(block_node)

            if self.break_triggered():
                break

            condition_result = self.interpret(condition_node)

        self.exit_loop()

    def visit_do_while_loop(self, node):
        self.enter_loop('do-while')
        MAX_LOOP_ITERATIONS = 10000
        LOOP_COUNTER = 0
        condition_node = node.children[1].children[0]
        block_node = node.children[0]

        while True:
            self.visit_block(block_node)
            LOOP_COUNTER += 1
            if LOOP_COUNTER > MAX_LOOP_ITERATIONS:
                raise InterpreterError("Runtime Error: Infinite loop detected!", node.line)
            
            if self.break_triggered():
                break
            

            condition_result = self.interpret(condition_node)
            
            if not isinstance(condition_result, bool):
                raise InterpreterError(f"Semantic Error: Condition must be a boolean. Got '{condition_result}'", node.line)

            if not condition_result:
                break

        self.exit_loop()
    
    def visit_break(self, node):
        if self.loop_stack:
            self.trigger_break()
        else:
            raise InterpreterError("Runtime Error: Break statement used outside of a loop", node.line)
        
    def trigger_break(self):
        self.break_flag = True

    def break_triggered(self):
        return self.break_flag

    def enter_loop(self, loop_type):
        self.loop_stack.append(loop_type)
        self.break_flag = False
        self.continue_flag = False

    def exit_loop(self):
        if self.loop_stack:
            self.loop_stack.pop()
            self.break_flag = False
            self.continue_flag = False

    def visit_continue(self, node):
        if self.loop_stack:
            self.trigger_continue()
        else:
            raise InterpreterError("Runtime Error: Continue statement used outside of a loop", node.line)
        
    def continue_triggered(self):
        return self.continue_flag
    
    def trigger_continue(self):
        self.continue_flag = True


    def visit_switch(self, node):
        self.enter_loop('switch')
        switch_expr_node = node.children[0]
        switch_value = self.interpret(switch_expr_node)

        matched_case = False
        break_found = False
        default_case = None

        for case_node in node.children[1:]:
            label_type = case_node.node_type
            if label_type == "Case":
                case_value_node = case_node.children[0]
                block_node = case_node.children[1]
                case_value = self.interpret(case_value_node)

                if switch_value == case_value or matched_case:
                    matched_case = True
                    self.visit_block(block_node)
                    if self.break_triggered():
                        break_found = True
                        break
            
            elif label_type == "Default":
                default_case = case_node.children[0]
        
        if not matched_case and not break_found and default_case:
            self.visit_block(default_case)

        self.exit_loop()

    def visit_input(self, node):
        var_name

        