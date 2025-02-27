from collections import defaultdict

def compute_first(cfg):
    first = defaultdict(set)  # Stores First sets
    epsilon = "λ"  # Represents epsilon (empty string)
    
    # Step 1: Initialize FIRST for terminals
    for lhs, productions in cfg.items():
        for prod in productions:
            if prod[0] not in cfg:  # If the first symbol is a terminal
                first[lhs].add(prod[0])
            if prod[0] == epsilon:  # If epsilon is a production
                first[lhs].add(epsilon)
    
    # Step 2: Compute FIRST iteratively until no changes occur
    changed = True
    while changed:
        changed = False
        for lhs, productions in cfg.items():
            for prod in productions:
                before = len(first[lhs])  # Track changes
                
                for symbol in prod:
                    if symbol in cfg:  # If non-terminal
                        first[lhs] |= (first[symbol] - {epsilon})  # Add FIRST(symbol) excluding ε
                        
                        if epsilon not in first[symbol]:  
                            break  # Stop if ε is not in FIRST(symbol)
                    else:  # If terminal, add it and stop
                        first[lhs].add(symbol)
                        break
                    
                else:  # If all symbols had ε, add ε to FIRST(lhs)
                    first[lhs].add(epsilon)

                if len(first[lhs]) > before:
                    changed = True  # Continue loop if changes occurred
    
    return first

def compute_follow(cfg, first):
    follow = defaultdict(set)
    epsilon = "λ"
    start_symbol = next(iter(cfg))  # Get the start symbol
    follow[start_symbol].add("$")  # Rule 1: Add $ to start symbol's Follow set

    changed = True
    while changed:
        changed = False
        for lhs, productions in cfg.items():
            for prod in productions:
                for i, symbol in enumerate(prod):
                    if symbol in cfg:  # Only compute Follow for non-terminals
                        before = len(follow[symbol])

                        # Rule 2: Everything in First(B) except ε is added to Follow(A)
                        if i + 1 < len(prod):  # Check next symbol
                            next_symbol = prod[i + 1]
                            if next_symbol in cfg:
                                follow[symbol] |= (first[next_symbol] - {epsilon})
                            else:
                                follow[symbol].add(next_symbol)
                        
                        # Rule 3: If ε is in First(B) or A → αA (A is at the end)
                        if i + 1 == len(prod) or (next_symbol in cfg and epsilon in first[next_symbol]):
                            follow[symbol] |= follow[lhs]

                        if len(follow[symbol]) > before:
                            changed = True

    return follow



def compute_predict(cfg, first, follow):
    predict = {}
    epsilon = "λ"
    
    for lhs, productions in cfg.items():
        for prod in productions:
            predict_key = (lhs, tuple(prod))
            predict[predict_key] = set()
            
            first_set = set()
            for symbol in prod:
                if symbol in cfg:
                    first_set |= (first[symbol] - {epsilon})
                    if epsilon not in first[symbol]:
                        break
                else:
                    first_set.add(symbol)
                    break
            else:
                first_set.add(epsilon)
            
            predict[predict_key] = first_set
            if epsilon in first_set:
                predict[predict_key] |= follow[lhs]
    
    return predict
    

cfg = {
    "<program>": [["<global>", "chungus skibidi", "(", ")", "{", "<body>", "back", "0", "}"]],
    "<global>": [["λ"], ["<global_statement>"]],
    "<global_statement>": [["<data_type>", "<identifier>", "<global_statement_val>","<global>"],
                           ["<identifier>", "=", "<global_val>", "<var_dec_tail>","<global>"],
                           ["sturdy", "<var_data_type>", "<identifier>", "=", "<global_val>", "<var_dec_tail>","<global>"],
                           ["nocap", "<dstruct_id>", "IDENTIFIER", "(", "<parameter>", "<next_param>", ")", "{", "<statement>", "}","<global>"],
                           ["<d_structure>","<global>"]],
    "<global_val>": [["<list_assignment>"],
                     ["<predefined_value>"]],
    "<global_statement_val>": [["=", "<global_val>", "<var_dec_tail>"],
                                ["<dstruct_id>", "(", "<parameter>", "<next_param>", ")", "{", "<statement>", "}"]],
    "<data_id>": [["<data_type>", "<identifier>"]],
    "<identifier>": [["IDENTIFIER", "<list_index>", "<struct_mem>"]],
    "<data_type>": [["chungus"],["chudeluxe"], ["forsen"], ["forsencd"], ["lwk"], ["aura"], ["gng"]],
    "<list_index>": [["λ"],["[", "<indexer>","]"]],
    "<indexer>": [["λ"], ["CHUNGUS_LIT"], ["<identifier>","<userdeffunc_call>"], ["<num_expression>"],["(", "<indexer>", ")", "<type_conversion>"]],
    "<struct_mem>": [["λ"],[".", "<identifier>", "<struct_mem>"],
                      ],
    "<literal>": [["<num_literal>"], ["FORSEN_LIT"], ["FORSENCD_LIT", "<stringCC>"], ["LWK_LIT", "<log_expression_tail>"]],
    "<num_literal>": [["CHUNGUS_LIT"], ["CHUDELUXE_LIT"]],
    "<stringCC>": [["λ"],["+", "FORSENCD_LIT", "<stringCC>"]],
    "<parameter>": [["λ"], ["<data_id>"], ],
    "<next_param>": [["λ"], [",", "<parameter>", "<next_param>"]],
    "<userdeffunc_call>": [["λ"], ["(", "<arg>", "<next_arg>", ")"]],
    "<arg>": [["λ"], ["<predefined_value>"]],
    "<next_arg>": [["λ"], [",", "<arg>", "<next_arg>"]],
    "<expression>": [["<expression_val>", "<_prepost_op>", "<expression_tail>"], 
                     ["<_prepost_op>","<expression_val>", "<expression_tail>"], 
                     ["(", "<expression_val>", "<expression_tail>",")", "<type_conversion>", "<expression_tail>"]],
    "<expression_val>": [["<literal>"], ["<identifier>", "<userdeffunc_call>", "<ts_function>"], ["(", "<expression>", ")", "<type_conversion>"]],
    "<expression_tail>": [["λ"], ["<rel_expression_tail>", "<log_expression_tail>"], ["<num_expression_tail>"]],
    "<num_expression>": [["<num_operand>", "<_arith_op>", "<num_operand>", "<num_expression_tail>"],
                         ["(", "<num_expression>", ")", "<type_conversion>", "<num_expression_tail>"]],
    "<num_operand>": [["<_unary_op>", "<num_val>"],["<num_val>", "<_prepost_op>"],["(", "<num_expression>", ")","<type_conversion>"]],
    "<num_val>": [["<num_literal>"], ["<identifier>","<userdeffunc_call>", "<ts_function>"],["(", "<num_val>", ")", "<type_conversion>", "<num_expression_tail>"]],
    "<num_expression_tail>": [["λ"],["<_arith_op>","<num_operand>", "<num_expression_tail>"]],
    "<_unary_op>": [["λ"], ["<_neg_op>"], ["<_prepost_op>"]],
    "<_neg_op>": [["λ"],["-"]],
    "<_prepost_op>": [["λ"],["++"], ["--"]],
    "<_arith_op>": [["+"], ["-"], ["/"], ["%"], ["*"]],
    "<bool_expression>": [["<relational_expression>", "<log_expression_tail>"], ["<log_expression>", "<log_expression_tail>"]],
    "<log_expression>": [["<log_open>", "<_log_op>", "<log_open>"]],
    "<relational_expression>": [["<rel_operand>", "<rel_expression_tail>", "<log_expression_tail>"], ["<_not_op>","(", "<relational_expression>", ")", "<rel_expression_tail>"]],
    "<rel_operand>": [["<rel_operand_content>"], ["(","<rel_operand_content>",")" , "<type_conversion>"]],
    "<rel_operand_content>": [["<literal>"], ["<identifier>", "<ts_function>"], ["<_not_op>", "(", "<bool_expression>", ")"]],
    "<rel_expression_tail>": [["λ"], ["<_rel_op>", "<rel_operand>", "<log_expression_tail>"],],
    "<lwk_operand>": [["<_not_op>", "<lwk_operand_val>"],["<relational_expression>"]],
    "<lwk_operand_val>": [["<identifier>","<userdeffunc_call>"], ["LWK_LIT", "<log_expression_tail>"]],
    "<log_open>": [["<_not_op>", "<log_operand>"]],
    "<log_operand>": [["LWK_LIT", "<log_expression_tail>"], ["<identifier>", "<userdeffunc_call>", "<ts_function>"], ["<relational_expression>"]],
    "<log_expression_tail>": [["λ"],["<_log_op>", "<log_open>"]],
    "<_rel_op>": [[">"], ["<"], [">="], ["<="], ["<_rel_eq_op>"]],
    "<_rel_eq_op>": [["=="], ["!="]],
    "<_log_op>": [["&&"], ["||"]],
    "<_not_op>": [["λ"], ["!"]],
    "<body>": [["<statement>", "<body>"],
               ["λ"]],
    "<statement>": [["<var_dec>"],
                    ["yap", "(", "<print_arg>", ")"],
                    ["<if_statement>"],
                    ["lethimcook", "(", "<switch_expression>", ")", "{", "<case_statement>", "}"],
                    ["plug", "(", "<var_dec>", ";", "<condition>", ";", "<update>", ")", "{", "<body>", "}"],
                    ["jit", "(", "<condition>", ")", "{", "<body>", "}"],
                    ["<d_structure>"],
                    ["back", "<predefined_value>"]],
    "<if_statement>": [["tuah", "(", "<condition>", ")", "{", "<body>", "}", "<_if_tail>"]],
    "<_if_tail>": [["λ"], ["<if_statement>"], ["hawk", "tuah", "(", "<condition>", ")", "{", "<body>", "}", "<_if_tail>"], ["hawk", "{", "<body>", "}"]],
    "<condition>": [["<lwk_operand>"], ["<_not_op>", "<relational_expression>"]],
    "<switch_expression>": [["<userdeffunc_call>"], ["<identifier>"]],
    "<case_statement>": [["λ"], ["caseoh", "<literal>", ":", "<body>", "getout", "<case_statement>"], ["npc", ":", "<body>", "getout"]],
    "<update>": [["<_prepost_op_update>", "<_update_op>"], ["<update_value>",  "<_prepost_op_update>"]],
    "<update_value>": [["<identifier>"], ["<literal>"]],
    "<_prepost_op_update>": [["++"], ["--"]],
    "<_update_op>": [["<_prepost_op_update>"]],
    "<var_dec>": [["aura", "IDENTIFIER", "IDENTIFIER", "<struct_init>"],
        ["sturdy", "<var_data_type>", "<identifier>", "=", "<local_value>", "<var_dec_tail>"],
        ["<var_data_type>", "<identifier>", "=", "<local_value>", "<var_dec_tail>"],
        ["gng", "IDENTIFIER", "IDENTIFIER", "<gng_var_value>"]],
    "<gng_var_value>": [["λ"], ["=", "CHUNGUS_LIT"]],
    "<struct_var_dec>": [["<struct_var_dec_head>", "<identifier>"]],
    "<var_data_type>": [["λ"], ["<data_type>"]],
    "<value>": [["<predefined_value>"], ["chat", "(", ")"], ["<list_value>"]],
    "<predefined_value>": [["<predefined_value_val>"]],
    "<predefined_value_val>": [["<expression>"]],
    "<var_dec_tail>": [["λ"], [",", "IDENTIFIER", "=", "<predefined_value>", "<var_dec_tail>"]],
    "<list_value_tail>": [["λ"], [",", "<predefined_value>", "<list_value_tail>"]],
    "<print_arg>": [["<print_arg1>", "<print_argN>"]],
    "<print_arg1>": [["FORSENCD_LIT", "<stringCC>"], ["<predefined_value>"]],
    "<print_argN>": [["λ"], [",", "<predefined_value>", "<print_argN>"]],
    "<d_structure>": [["<struct_def>"], ["<enum_def>"]],
    "<struct_def>": [["aura", "<identifier>", "{", "<struct_member_dec>", "}"]],
    "<enum_def>": [["gng", "<identifier>", "{", "<enum_property>", "}"]],
    "<struct_member_dec>": [
        ["<data_id>", "<struct_member_val>", "<struct_member_dec>"],
        ["<struct_var_dec>", "<struct_member_dec>"],
        ["λ"]],
    "<enum_property>": [["IDENTIFIER", "<enum_value>", "<enum_property_tail>"]],
    "<enum_property_tail>": [["λ"], [",", "IDENTIFIER", "<enum_value>", "<enum_property_tail>"]],
    "<enum_value>": [["λ"], ["=", "CHUNGUS_LIT"]],
    "<list_value>": [["[", "<list_value_in>", "]"]],
    "<list_value_in>":[["λ"], ["<predefined_value>", "<list_value_tail>"]],
    "<list_assignment>": [
        ["<list_value>"],
        ["append", "(", "arg>", "<next_arg>", ")"],
        ["insert", "(", "CHUNGUS_LIT,", "<arg>", "<next_arg>", ")"],
        ["remove", "(", "CHUNGUS_LIT", ")"]],
    "<dstruct_id>": [["λ"], ["IDENTIFIER"]],
    "<ts_function>": [["λ"], [".", "ts", "(", ")"]],
    "<taper_function>": [["λ"], [".", "taper", "(", ")"]],
    "<struct_init>": [["λ"], ["=", "<struct_var_value>"]],
    "<struct_var_value>": [["<struct_value_content>"], ["{", "IDENTIFIER", "=", "<struct_value_content>", "<struct_value_tail>", "}"]],
    "<struct_value_tail>": [[",", "IDENTIFIER", "=", "<struct_value_content>", "<struct_value_tail>"], ["λ"]],
    "<struct_value_content>": [["<predefined_value>"], ["<list_value>"]],
    "<local_value>": [["<value>"], ["<list_value>"]],
    "<struct_var_dec_head>": [["λ"], ["aura", "IDENTIFIER"]],
    "<struct_member_val>": [["λ"], ["=", "<struct_value_content>", "<struct_member_val_tail>"]],
    "<struct_member_val_tail>": [["λ"], [",", "IDENTIFIER", "=", "<struct_value_content>", "<struct_member_val_tail>"]],
    "<type_conversion>": [["λ"], [".", "<convert_type>"]],
    "<convert_type>": [["chungus"], ["chudeluxe"]]
}

first_sets = compute_first(cfg)
follow_sets = compute_follow(cfg, first_sets)
predict_sets = compute_predict(cfg, first_sets, follow_sets)



'''print("FIRST SET:")
for non_terminal in cfg.keys():
    print(f"First({non_terminal}) = {first_sets[non_terminal]}")

print("\n\nFOLLOW SET:")
for non_terminal in cfg.keys():
    print(f"Follow({non_terminal}) = {follow_sets[non_terminal]}")

print("\n\nPREDICT SET:")
for (lhs, prod), predict_set in predict_sets.items():
    print(f"Predict({lhs} → {' '.join(prod)}) = {predict_set}")'''