from collections import defaultdict

def compute_first(cfg):
    first = defaultdict(set)
    epsilon = "ε"
    
    for lhs, productions in cfg.items():
        for prod in productions:
            if prod[0] not in cfg:  # If the first symbol is a terminal
                first[lhs].add(prod[0])
            if prod[0] == epsilon:  # If epsilon is a production
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
    epsilon = "ε"
    start_symbol = next(iter(cfg))  # Get the start symbol
    follow[start_symbol].add("$")

    changed = True
    while changed:
        changed = False
        for lhs, productions in cfg.items():
            for prod in productions:
                for i, symbol in enumerate(prod):
                    if symbol in cfg:  # Only compute Follow for non-terminals
                        before = len(follow[symbol])

                        if i + 1 < len(prod):  # Check next symbol
                            next_symbol = prod[i + 1]
                            if next_symbol in cfg:
                                follow[symbol] |= (first[next_symbol] - {epsilon})
                            else:
                                follow[symbol].add(next_symbol)
                        

                        if i + 1 == len(prod) or (next_symbol in cfg and epsilon in first[next_symbol]):
                            follow[symbol] |= follow[lhs]

                        if len(follow[symbol]) > before:
                            changed = True

    return follow


def compute_predict(cfg, first, follow):
    predict = {}
    epsilon = "ε"
    
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
    "<program>": [["<global>", "skibidi", "{", "<nl>", "<body>", "}"]],
    "<global>": [["<global_dec>", "<user_def_func>"]],
    "<global_dec>": [["ε"],
        ["<variable_declaration>", "<nl>", "<global_dec>"],
        ["<constant_vardec>", "<nl>", "<global_dec>"]],
    "<user_def_func>": [["ε"],
        ["fein", "<return_type>", "identifier", "(", "<parameter>", ")", "{", "<nl>", "<body>", "}", "<nl>", "<user_def_func>"]],
    "<variable_declaration>": [["<data_id>", "<var_init>"]],
    "<constant_vardec>": [["sturdy", "<variable_declaration>"]],
    "<data_id>": [["<data_type>", "identifier"]],
    "<id>": [["identifier", "<index>"]],
    "<index>": [["ε"],
        ["[", "<expression>", "]"]],
    "<data_type>": [["chungus"],
        ["chudeluxe"],
        ["forsen"],
        ["forsencd"],
        ["lwk"]],
    "<return_type>": [["<data_type>"],
        ["nocap"]],
    "<var_init>": [["=", "<value>", "<var_init_tail>"]],
    "<var_init_tail>": [["ε"],
        [",", "identifier", "<var_init>"]],
    "<value>": [["<expression>"],
        ["chat", "(", ")"],
        ["<list_value>"]],
    "<list_value>": [["[", "<list_content>", "]"],
        ["append", "(", "<arg>", ")"],
        ["insert", "(", "<expression>", ",", "<arg>", ")"],
        ["remove", "(", "<expression>", ")"]],
    "<list_content>": [["ε"],
        ["<arg>"]],
    "<parameter>": [["ε"],
        ["<data_id>", "<parameter_tail>"]],
    "<parameter_tail>": [["ε"],
        [",", "<data_id>", "<parameter_tail>"]],
    "<arg>": [["<expression>", "<arg_tail>"]],
    "<arg_tail>": [["ε"],
        [",", "<expression>", "<arg_tail>"]],
    "<body>": [["ε"],
        ["<statement>", "<body>"]],
    "<statement>": [["<output>", "<nl>", "<body>"],
        ["<variable_declaration>", "<nl>", "<body>"],
        ["<if_statement>", "<body>"],
        ["<switch_statement>", "<nl>", "<body>"],
        ["<for_loop>", "<nl>", "<body>"],
        ["<while_loop>", "<nl>", "<body>"],
        ["<dowhile_loop>", "<nl>", "<body>"],
        ["<return_statement>", "<nl>", "<body>"],
        ["getout", "<nl>", "<body>"],
        ["<id_stmt>", "<nl>", "<body>"]],
    "<output>": [["yap", "(", "<print_arg1>", "<print_argN>",")"]],
    "<print_arg1>": [["<expression>"]],
    "<print_argN>": [["ε"],
        [",", "<expression>", "<print_argN>"]],
    "<if_statement>": [["tuah", "(", "<expression>", ")", "{", "<nl>", "<body>", "}","<nl>", "<if_tail>"]],
    "<if_tail>": [["ε"],
        ["hawk", "<hawk_follow>"]],
    "<hawk_follow>": [["<if_statement>"],
        ["{", "<nl>", "<body>", "}", "<nl>"]],
    "<switch_statement>": [["lethimcook", "(", "<expression>", ")", "{", "<nl>", "<case_statement>", "}"]],
    "<case_statement>": [["ε"],
        ["caseoh", "<constant>", ":", "<nl>", "<body>", "<case_statement>"],
        ["npc", ":", "<nl>", "<body>"]],
    "<constant>": [["chungus_lit"],
        ["forsen_lit"]],
    "<for_loop>": [["plug", "(", "<for_initialization>", ";", "<expression>", ";", "<id_update>", ")", "{", "<nl>", "<body>", "}"]],
    "<while_loop>": [["jit", "(", "<expression>", ")", "{", "<nl>", "<body>", "}"]],
    "<dowhile_loop>": [["lil", "{", "<nl>", "<body>", "}", "<nl>", "jit", "(", "<expression>", ")"]],
    "<for_initialization>": [["<variable_declaration>"],
        ["<id_stmt>"]],
    "<return_statement>": [["back", "<return_value>"]],
    "<return_value>": [["ε"],
        ["<expression>"]],
    "<expression>": [["<expr_head>", "<expr_tail>"]],
    "<expr_head>": [["<term>", "<term_tail>"]],
    "<term>": [["<factor>", "<builtin_func>", "<factor_tail>"]],
    "<factor>": [["neg", "<factor1>"],
        ["!", "<factor1>"],
        ["<factor1>"]],
    "<factor1>": [["<literal>"],
        ["<id>", "<id_factor_tail>"],
        ["<pre_operator>", "<id>"],
        ["(", "<oppar>"]],
    "<id_factor_tail>": [["<post_operator>"],
        ["(", "<func_call_arg>", ")"]],
    "<func_call_arg>": [["ε"],
        ["<arg>"]],
    "<oppar>": [["<typecast>", ")", "<term>"],
        ["<expression>", ")"]],
    "<pre_operator>": [["--"],
        ["++"]],
    "<post_operator>": [["ε"],
        ["<pre_operator>"]],
    "<builtin_func>": [["ε"],
        [".", "<builtin_func1>"]],
    "<builtin_func1>": [["taper", "(", ")"],
        ["ts", "(", ")"]],
    "<typecast>": [["chungus"],
        ["chudeluxe"]],
    "<factor_tail>": [["ε"],
        ["<factor_op>", "<factor>", "<factor_tail>"]],
    "<factor_op>": [["+"],
        ["- "],
        ["/"],
        ["*"],
        ["%"]],
    "<term_tail>": [["ε"],
        ["<term_op>", "<factor>", "<term_tail>"]],
    "<term_op>": [[">"],
        [">="],
        ["<"],
        ["<="],
        ["=="],
        ["!="]],
    "<expr_tail>": [["ε"],
        ["<expr_op>", "<expr_head>", "<expr_tail>"]],
    "<expr_op>": [["&&"],
        ["||"]],
    "<id_stmt>": [["<pre_operator>", "<id>", "<id_update_more>"],
        ["<id>", "<id_stmt_tail>"]],
    "<id_stmt_tail>": [["=", "<value>", "<id_update_more>"],
        ["<pre_operator>", "<id_update_more>"],
        ["(", "<func_call_arg>", ")"]],
    "<id_update>": [["<pre_operator>", "<id>", "<id_update_more>"],
        ["<id>", "<id_update_tail>"]],
    "<id_update_tail>": [["=", "<value>", "<id_update_more>"],
        ["<pre_operator>", "<id_update_more>"]],
    "<id_update_more>": [["ε"],
        [",", "<id_update>"]],
    "<literal>": [["chungus_lit"],
        ["chudeluxe_lit"],
        ["forsen_lit"],
        ["forsencd_lit"],
        ["lwk_lit"]],
    "<nl>": [["nl"]],
}


first_sets = compute_first(cfg)
follow_sets = compute_follow(cfg, first_sets)
predict_sets = compute_predict(cfg, first_sets, follow_sets)

'''
print("Context-Free Grammar (CFG):\n")
for non_terminal, productions in cfg.items():
    non_terminal = non_terminal.strip("<>").upper() 
    for production in productions:
        production_str = " ".join([symbol.strip("<>").upper() if symbol.startswith("<") else symbol for symbol in production])
        production_str = "''" if production_str == "ε" else production_str
        print(f"{non_terminal} ::= {production_str}")


print("FIRST SET:")
for non_terminal in first_sets.keys():
    first_set_str = ", ".join(first_sets[non_terminal]).replace("''", "")
    print(f"First({non_terminal}) -> {{ {first_set_str} }}")

print("\n\nFOLLOW SET:")
for non_terminal in follow_sets.keys():
    follow_set_str = ", ".join(follow_sets[non_terminal]).replace("''", "")  # Remove '' and format set
    print(f"Follow({non_terminal}) -> {{{follow_set_str}}}")

print("\n\nPREDICT SET:")
for (lhs, prod), predict_set in predict_sets.items():
    prod_str = " ".join(prod).replace("''", "")  # Remove '' in productions
    predict_set_str = ", ".join(predict_set).replace("''", "")  # Remove '' in predict set
    print(f"Predict({lhs} → {prod_str}) -> {{{predict_set_str}}}")'''
