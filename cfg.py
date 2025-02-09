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



cfg = {
    "<program>": [["<global>", "<user_defined_function>", "chungus", "skibidi", "(", ")", "{", "<body>", "back", "0", "}"]],
    "<global>": [["<global_statement>", "<global>"],
                ["λ"]],
    "<global_statement>": [["<var_data_type>", "<identifier>", "=", "<global_val>", "<var_dec_tail>"],
                            ["<const_dec>", "<var_data_type>", "<identifier>", "=", "<var_dec_tail>"],
                            ["<d_structure>"]],
    "<global_val>": [["<list_assignment>"],
                     ["<predefined_value>"]],
    "<const_dec>": [["sturdy"],
                   ["λ"]],
    "<data_id>": [["<data_type>", "<identifier>"]],
    "<identifier>": [["IDENTIFIER", "<list_index>", "<struct_mem>"]],
    "<data_type>": [["chungus"], ["chudeluxe"], ["forsen"], ["forsencd"], ["lwk"], ["aura"], ["gng"]],
    "<list_index>": [["[", "<indexer>", "]"],
                     ["λ"]],
    "<indexer>": [["CHU_LIT"], ["<identifier>"], ["<num_expression>"], ["<userdeffunc_call>"]],
    "<struct_mem>": [[".", "<identifier>", "<struct_mem>"],
                      ["λ"]],
    "<literal>": [["<num_literal>"], ["FORSEN_LIT"], ["FORSENCD_LIT", "<stringCC>"], ["LWK_LIT"]],
    "<num_literal>": [["CHU_LIT"], ["CHUDEL_LIT"]],
    "<stringCC>": [["+", "FORSENCD_LIT", "<stringCC>"],
                   ["λ"]],
    "<user_defined_function>": [["<return_type>", "IDENTIFIER", "(", "<parameter>", "<next_param>", ")", "{", "<statement>", "}", "<global>", "<user_defined_function>"],
                                ["λ"]],
    "<return_type>": [["nocap"], ["<data_type>", "<dstruct_id>"]],
    "<parameter>": [["<data_id>"], ["λ"]],
    "<next_param>": [[",", "<parameter>", "<next_param>"],
                      ["λ"]],
    "<userdeffunc_call>": [["<type_conversion>", "IDENTIFIER", "(", "<arg>", "<next_arg>", ")"]],
    "<arg>": [["<predefined_value>"], ["λ"]],
    "<next_arg>": [[",", "<arg>", "<next_arg>"],
                    ["λ"]],
    "<expression>": [["<num_expression>"], ["<bool_expression>"]],
    "<num_expression>": [["<num_operand>", "<_arith_op>", "<num_operand>", "<num_expression_tail>"],
                         ["<type_conversion>", "(", "<num_expression>", ")"]],
    "<num_operand>": [["<type_conversion>", "<_unary_op>", "<num_val>", "<_prepost_op>"]],
    "<num_val>": [["<num_literal>"], ["<identifier>", "<ts_function>"]],
    "<num_expression_tail>": [["<_arith_op>", "<num_operand>", "<num_expression_tail>"],
                              ["λ"]],
    "<_unary_op>": [["-"], ["<_prepost_op>"], ["λ"]],
    "<_prepost_op>": [["++"], ["--"], ["λ"]],
    "<_arith_op>": [["+"], ["-"], ["/"], ["%"], ["*"]],
    "<bool_expression>": [["<relational_expression>"],
                          ["<log_open>", "<_log_op>", "<log_open>", "<log_expression_tail>"]],
    "<relational_expression>": [["<rel_operand>", "<_rel_op>", "<rel_operand>", "<rel_expression_tail>"]],
    "<rel_operand>": [["<type_conversion>", "<rel_operand_content>"]],
    "<rel_operand_content>": [["<num_literal>"], ["<identifier>", "<ts_function>", "<num_expression>", "<relational_expression>", "(", "<rel_operand_content>" ")"]],
    "<rel_expression_tail>": [["<_rel_op>", "<rel_operand>", "<rel_expression_tail>"],
                              ["λ"]],
    "<forsen_operand>": [["FORSEN_LIT"], ["FORSENCD_LIT"], ["<identifier>"], ["(<relational_expression>)"]],
    "<lwk_operand>": [["<_not_op>", "LWK_LIT"], ["<_not_op>", "<identifier>"], ["<_not_op>", "<userdeffunc_call>"], ["(<relational_expression>)"]],
    "<log_open>": [["<_not_op>", "<log_operand>"]],
    "<log_operand>": [["LWK_LIT"], ["<userdeffunc_call>"], ["<bool_expression>"]],
    "<log_expression_tail>": [["<_log_op>", "<log_open>", "<log_expression_tail>"], ["λ"]],
    "<_rel_op>": [[">"], ["<"], [">="], ["<="], ["<_rel_eq_op>"]],
    "<_rel_eq_op>": [["=="], ["!="]],
    "<_log_op>": [["&&"], ["||"]],
    "<_not_op>": [["!"], ["λ"]],
    "<body>": [["<statement>", "<body>"],
               ["λ"]],
    "<statement>": [["<var_dec>"],
                    ["yap", "(<print_arg>)"],
                    ["<if_statement>"],
                    ["lethimcook", "(<switch_expression>)", "{<case_statement>}"],
                    ["plug", "(<var_dec>;", "<condition>;", "<update>)", "{<body>}"],
                    ["jit", "(<condition>)", "{<body>}"],
                    ["<d_structure>"],
                    ["back", "<predefined_value>"]],
    "<if_statement>": [["tuah", "(<condition>)", "{<body>}", "<_if_tail>"]],
    "<_if_tail>": [["<if_statement>"], ["hawk", "tuah", "(<condition>)", "{<body>}", "<_if_tail>"], ["hawk", "{<body>}"], ["λ"]],
    "<condition>": [["<lwk_operand>"], ["<bool_expression>"]],
    "<switch_expression>": [["<userdeffunc_call>"], ["<identifier>"]],
    "<case_statement>": [["caseoh", "<literal>", ":", "<body>", "getout", "<case_statement>"], ["npc:", "<body>", "getout"], ["λ"]],
    "<update>": [["<update_value>", "<_update_op>"], ["<_prepost_op>", "<update_value>"]],
    "<update_value>": [["<identifier>"], ["<literal>"]],
    "<_update_op>": [["<_prepost_op>"]],
    "<var_dec>": [
        ["<var_data_type>", "<identifier>", "=", "<local_value>", "<var_dec_tail>"],
        ["<const_dec>", "<var_data_type>", "<identifier>", "=", "<value>"],
        ["<const_dec>", "<var_data_type>", "<identifier>", "=", "<list_value>"],
        ["<struct_var_dec>", "<struct_init>"],
        ["gng", "IDENTIFIER", "IDENTIFIER", "<gng_var_value>"]],
    "<gng_var_value>": [["=", "CHU_LIT"], ["λ"]],
    "<struct_var_dec>": [["<struct_var_dec_head>", "<identifier>"]],
    "<var_data_type>": [["<data_type>"], ["λ"]],
    "<value>": [["<predefined_value>"], ["chat()"]],
    "<predefined_value>": [
        ["<type_conversion>", "<literal>"],
        ["<type_conversion>", "<identifier>", "<taper_function>"],
        ["<type_conversion>", "<expression>"],
        ["<userdeffunc_call>", "<taper_function>"]],
    "<var_dec_tail>": [[" , IDENTIFIER = <predefined_value>", "<var_dec_tail>"], ["λ"]],
    "<list_value_tail>": [[",", "<predefined_value>", "<list_value_tail>"], ["λ"]],
    "<print_arg>": [["<print_arg1>", "<print_argN>"]],
    "<print_arg1>": [["FORSEN_LIT", "<stringCC>"], ["<predefined_value>"]],
    "<print_argN>": [[",", "<predefined_value>", "<print_argN>"], ["λ"]],
    "<d_structure>": [["<struct_def>"], ["<enum_def>"]],
    "<struct_def>": [["aura", "<identifier>", "{", "<struct_member_dec>", "}"]],
    "<enum_def>": [["gng", "<identifier>", "{", "<enum_property>", "}"]],
    "<struct_member_dec>": [
        ["<data_id>", "<struct_member_val>", "<struct_member_dec>"],
        ["<struct_var_dec>", "<struct_member_dec>"],
        ["λ"]],
    "<enum_property>": [["IDENTIFIER", "<enum_value>", "<enum_property_tail>"]],
    "<enum_property_tail>": [[",", "IDENTIFIER", "<enum_value>", "<enum_property_tail>"], ["λ"]],
    "<enum_value>": [["=", "CHUNGUS_LIT"], ["λ"]],
    "<list_value>": [["[", "<predefined_value>", "<list_value_tail>", "]"], ["[]"]],
    "<list_assignment>": [
        ["<list_value>"],
        ["append", "(<arg>", "<next_arg>", ")"],
        ["insert", "(CHUNGUS_LIT,", "<arg>", "<next_arg>", ")"],
        ["remove", "(CHUNGUS_LIT)"]],
    "<dstruct_id>": [["IDENTIFIER"], ["λ"]],
    "<ts_function>": [[".ts()"], ["λ"]],
    "<taper_function>": [[".taper()"], ["λ"]],
    "<struct_init>": [["=", "<struct_var_value>"], ["λ"]],
    "<struct_var_value>": [["<struct_value_content>"], ["{", "IDENTIFIER", "=", "<struct_value_content>", "<struct_value_tail>", "}"]],
    "<struct_value_tail>": [[",", "IDENTIFIER", "=", "<struct_value_content>", "<struct_value_tail>"], ["λ"]],
    "<struct_value_content>": [["<predefined_value>"], ["<list_value>"]],
    "<local_value>": [["<value>"], ["<list_value>"]],
    "<struct_var_dec_head>": [["aura", "IDENTIFIER"], ["λ"]],
    "<struct_member_val>": [["=", "<struct_value_content>", "<struct_member_val_tail>"], ["λ"]],
    "<struct_member_val_tail>": [[",", "IDENTIFIER", "=", "<struct_value_content>", "<struct_member_val_tail>"], ["λ"]],
    "<type_conversion>": [["(", "<convert_type>", ")"], ["λ"]],
    "<convert_type>": [["chungus"], ["chudeluxe"]]
}

first_sets = compute_first(cfg)
for non_terminal in cfg.keys():  # Preserve original CFG order
    print(f"First({non_terminal}) = {first_sets[non_terminal]}")
