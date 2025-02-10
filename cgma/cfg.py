from collections import defaultdict

def compute_first(cfg):
    first = defaultdict(set)
    epsilon = "\u03BB"  # Represents epsilon (empty string)
    
    for lhs, productions in cfg.items():
        for prod in productions:
            if prod[0] not in cfg:
                first[lhs].add(prod[0])
            if prod[0] == epsilon:
                first[lhs].add(epsilon)
    
    changed = True
    while changed:
        changed = False
        for lhs, productions in cfg.items():
            for prod in productions:
                before = len(first[lhs])
                
                for symbol in prod:
                    if symbol in cfg:
                        first[lhs] |= (first[symbol] - {epsilon})
                        if epsilon not in first[symbol]:
                            break
                    else:
                        first[lhs].add(symbol)
                        break
                else:
                    first[lhs].add(epsilon)
                
                if len(first[lhs]) > before:
                    changed = True
    
    return first

def compute_follow(cfg, first):
    follow = defaultdict(set)
    start_symbol = list(cfg.keys())[0]
    follow[start_symbol].add("$")  # Start symbol gets EOF symbol
    
    changed = True
    while changed:
        changed = False
        for lhs, productions in cfg.items():
            for prod in productions:
                for i in range(len(prod)):
                    symbol = prod[i]
                    if symbol in cfg:
                        before = len(follow[symbol])
                        
                        # Check the next symbols in production
                        for j in range(i + 1, len(prod)):
                            next_symbol = prod[j]
                            follow[symbol] |= (first[next_symbol] - {"\u03BB"})
                            if "\u03BB" not in first[next_symbol]:
                                break
                        else:
                            follow[symbol] |= follow[lhs]
                        
                        if len(follow[symbol]) > before:
                            changed = True
    
    return follow

def compute_predict(cfg, first, follow):
    predict = defaultdict(set)
    for lhs, productions in cfg.items():
        for prod in productions:
            prod_first = set()
            for symbol in prod:
                if symbol in cfg:
                    prod_first |= (first[symbol] - {"\u03BB"})
                    if "\u03BB" not in first[symbol]:
                        break
                else:
                    prod_first.add(symbol)
                    break
            else:
                prod_first.add("\u03BB")
            
            predict[(lhs, tuple(prod))] = prod_first | (follow[lhs] if "\u03BB" in prod_first else set())
    
    return predict



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
follow_sets = compute_follow(cfg, first_sets)
predict_sets = compute_predict(cfg, first_sets, follow_sets)

print("FIRST SETS:")
for nt in cfg.keys():
    print(f"First({nt}) = {first_sets[nt]}")

print("\nFOLLOW SETS:")
for nt in cfg.keys():
    print(f"Follow({nt}) = {follow_sets[nt]}")

print("\nPREDICT SETS:")
for key, value in predict_sets.items():
    print(f"Predict{key} = {value}")
