from collections import defaultdict

def compute_first(cfg):
    first = defaultdict(set)  # Stores First sets
    epsilon = "ε"  # Represents epsilon (empty string)
    
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
    epsilon = "ε"
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
    "<program>": [["<start>"]],
    "<start>":[["<global_declaration>", "<start>"],["chungus", "<chungus_follow>"]],
    "<chungus_follow>":[["<identifier>", "<declaration_tail>", "<start>"], ["skibidi", "(", ")", "{", "<body_main>", "back", "0", "}"]],
    "<global_declaration>": [["<constant_var>"], ["<gldata_type>", "<identifier>", "<declaration_tail>"], ["<expression>"]],
    "<gldata_type>": [["aura"], ["nocap"], ["forsen"], ["forsencd"], ["chudeluxe"], ["lwk"]],
    "<data_type>": [["chungus"], ["<gldata_type>"]],
    "<body>": [["ε"], ["<declaration>", "<body>"], ["<statement>", "<body>"], ["back", "<return_value>"]],
    "<body_main>": [["ε"], ["<declaration>", "<body_main>"], ["<statement>", "<body_main>"]],
    "<expression>": [["<operand>", "<expression_tail>"]],
    "<operand>": [["<pre_operand>", "<operand_content>"],["<operand_content>", "<post_operand>"], ["(", "<oppar>"]],
    "<pre_operand>": [["-"], ["<prepost_operator>"], ["!"]],
    "<operand_content>": [["FORSEN_LIT"], ["FORSENCD_LIT"], ["CHU_LIT"], ["CHUDEL_LIT"], ["LWK_LIT"], ["<identifier>"]],
    "<post_operand>": [["ε"], ["<prepost_operator>"]],
    "<prepost_operator>": [["--"], ["++"]],
    "<expression_tail>": [["ε"], ["<dot_suffix>"], ["<operator>", "<operand>", "<expression_tail>"], ["=", "<value>"]],
    "<value>": [["<list_value>"], ["<expression>"], ["chat", "(", ")"], ["<multi_struct_val>"]],
    "<multi_struct_val>": [["{",  "<identifier>", "=", "<expression>", "<struct_init_tail>", "}"]],
    "<struct_init_tail>": [["ε"], [",", "<identifier>", "=", "<expression>", "<struct_init_tail>"]],
    "<dtype1>": [["chungus"], ["chudeluxe"]],
    "<oppar>": [["<dtype1>", ")", "<expression>"], ["<expression>", ")"]],
    "<operator>": [["+"], ["-"], ["*"], ["/"], ["%"], ["=="], ["!="], [">"], ["<"], [">="], ["<="], ["&&"], ["||"]],
    "<identifier>": [["IDENTIFIER", "<struct_id>", "<identifier_postfix>"]],
    "<identifier_postfix>": [["ε"], ["<dot_suffix>"], ["(", "<postfix_content>", ")"]],
    "<struct_id>": [["ε"], ["IDENTIFIER"]],
    "<dot_suffix>": [["<index>"], [".", "<dot_suffix_content>"]],
    "<dot_suffix_content>": [["ts", "(", ")"], ["taper", "(", ")"], ["IDENTIFIER", "<dot_suffix>"]],
    "<postfix_content>": [["ε"], ["<parameter>"], ["<arg>"]],
    "<index>": [["[", "<expression>", "]"]],
    "<arg>": [["<expression>", "<arg_tail>"]],
    "<arg_tail>": [["ε"], [",", "<expression>", "<arg_tail>"]],
    "<parameter>": [["<data_id>", "<parameter_tail>"]],
    "<parameter_tail>": [["ε"], [",", "<data_id>", "<parameter_tail>"]],
    "<data_id>": [["<data_type>", "<identifier>"]],
    "<constant_var>": [["sturdy", "<data_id>", "<var_initialization>"]],
    "<declaration>": [["<data_id>", "<declaration_tail>"], ["<expression>"], ["<constant_var>"]],
    "<declaration_tail>": [["ε"], ["<var_initialization>"], ["{", "<body>", "}"]],
    "<var_initialization>": [["=", "<value>", "<var_init_tail>"]],
    "<var_init_tail>": [["ε"], [",", "<identifier>", "<var_initialization>"]],
    "<statement>": [["yap", "(", "<print_arg>", ")"], ["lethimcook", "(", "<identifier>", ")", "{", "<case_statement>", "}"], ["plug", "(", "<for_initialization>", ";", "<expression>", ";", "<expression>", ")", "{", "<body>", "}"], ["lil", "{", "<body>", "}", "jit", "(", "<expression>", ")"], ["jit", "(", "<expression>", ")", "{", "<body>", "}"], ["<if_statement>"], ["pause"]],
    "<if_statement>": [["tuah", "(", "<expression>", ")", "{", "<body>", "}", "<if_tail>"]],
    "<if_tail>": [["ε"], ["hawk", "<hawk_follow>"]],
    "<hawk_follow>": [["{", "<body>", "}"],["<if_statement>"]],
    "<print_arg>": [["<expression>", "<print_argN>"]],
    "<print_argN>": [["ε"], [",", "<expression>", "<print_argN>"]],
    "<case_statement>": [["caseoh", "<constant>", ":", "<case_line>", "getout", "<case_statement>"], ["npc", ":", "<case_line>", "getout"]],
    "<for_initialization>": [["<data_id>", "<var_initialization>"], ["<expression>"]],
    "<constant>": [["CHU_LIT"], ["FORSEN_LIT"], ["LWK_LIT"]],
    "<return_value>": [["ε"], ["<expression>"]],
    "<case_line>": [["ε"], ["<data_id>", "<var_initialization>", "<case_line>"], ["<expression>", "<case_line>"], ["<statement>", "<case_line>"]],
    "<list_value>": [["append", "(", "<arg>", ")"], ["insert", "(", "CHU_LIT", ",", "<arg>", ")"], ["remove", "(", "CHU_LIT", ")"], ["[", "<list_content>", "]"]],
    "<list_content>": [["ε"],["<arg>"]]
}

first_sets = compute_first(cfg)
follow_sets = compute_follow(cfg, first_sets)
predict_sets = compute_predict(cfg, first_sets, follow_sets)

'''print("Context-Free Grammar (CFG):\n")
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
