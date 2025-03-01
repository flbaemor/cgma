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
    "<program>": [["<global>", "chungus skibidi", "(", ")", "{", "<body_main>", "back", "0", "}"]],
    "<global>": [["ε"], ["<declaration>", "<global>"]],
    "<body_main>": [["ε"], ["<declaration>", "<body_main>"], ["<statement>", "<body_main>"]],
    "<body>": [["ε"], ["<declaration>", "<body>"], ["<statement>", "<body>"], ["back", "<return_value>"]],
    "<declaration>": [["<data_id>", "<declaration_tail>"], ["<expression>"]],
    "<declaration_tail>": [["ε"], ["<var_initialization>"], ["{", "<definition>", "}"]],
    "<var_initialization>": [["=", "<value>", "<var_init_tail>"]],
    "<var_init_tail>": [["ε"], [",", "<identifier>", "<var_initialization>"]],
    "<definition>": [["ε"], ["<body>"]],
    "<expression>": [["<operand>", "<expression_tail>"]],
    "<operand>": [["<pre_operand>", "<operand_content>", "<post_operand>"], ["(", "<oppar>"]],
    "<pre_operand>": [["ε"], ["-"], ["<prepost_operator>"], ["!"]],
    "<operand_content>": [["FORSEN_LIT"], ["FORSENCD_LIT"], ["CHU_LIT"], ["CHUDEL_LIT"], ["LWK_LIT"], ["<identifier>"]],
    "<post_operand>": [["ε"], ["<prepost_operator>"]],
    "<concat>": [["ε"], ["+","<concat_value>"]],
    "<concat_value>": [["<identifier>","<concat>"], ["FORSENCD_LIT","<concat>"], ["FORSEN_LIT","<concat>"]],
    "<prepost_operator>": [["--"], ["++"]],
    "<expression_tail>": [["ε"], ["<dot_suffix>"], ["<operator>", "<operand>", "<expression_tail>"], ["=", "<value>"]],
    "<value>": [["<list_value>"], ["<expression>"], ["chat", "(", ")"]],
    "<list_value>": [["append", "(", "<arg>", ")"], ["insert", "(", "CHUNGUS_LIT", ",", "<arg>", ")"], ["remove", "(", "CHUNGUS_LIT", ")"]],
    "<oppar>": [["<dtype1>", ")", "<expression>"], ["<expression>", ")"]],
    "<dtype1>": [["chungus"], ["chudeluxe"]],
    "<operator>": [["+"], ["-"], ["*"], ["/"], ["%"], ["=="], ["!="], [">"], ["<"], [">="], ["<="], ["&&"], ["||"]],
    "<identifier>": [["IDENTIFIER", "<struct_id>", "<identifier_postfix>"]],
    "<identifier_postfix>": [["ε"], ["<dot_suffix>"], ["(", "<postfix_content>", ")"]],
    "<struct_id>": [["ε"], ["IDENTIFIER"]],
    "<dot_suffix>": [["<index>"], [".", "<dot_suffix_content>"]],
    "<dot_suffix_content>": [["ts", "(", ")"], ["taper", "(", ")"], ["IDENTIFIER", "<dot_suffix>"]],
    "<postfix_content>": [["ε"], ["<parameter>"], ["<arg>"]],
    "<index>": [["ε"], ["[", "<expression>", "]"]],
    "<arg>": [["<expression>", "<arg_tail>"]],
    "<arg_tail>": [["ε"], [",", "<expression>", "<arg_tail>"]],
    "<parameter>": [["<data_id>", "<parameter_tail>"]],
    "<parameter_tail>": [["ε"], [",", "<data_id>", "<parameter_tail>"]],
    "<data_id>": [["<data_type>", "<identifier>"]],
    "<data_type>": [["forsen"], ["forsencd"], ["chungus"], ["chudeluxe"], ["lwk"], ["aura"], ["gng"], ["nocap"]],
    "<statement>": [["yap", "(", "<print_arg>", ")"], ["lethimcook", "(", "<identifier>", ")", "{", "<case_statement>", "}"], ["plug", "(", "<for_initialization>", ";", "<expression>", ";", "<expression>", ")", "{", "<body>", "}"], ["lil", "{", "<body>", "}", "jit", "(", "<expression>", ")"], ["jit", "(", "<expression>", ")", "{", "<body>", "}"], ["<if_statement>"]],
    "<if_statement>": [["tuah", "(", "<expression>", ")", "{", "<body>", "}", "<if_tail>"]],
    "<if_tail>": [["ε"], ["hawk", "<hawk_follow>"]],
    "<hawk_follow>": [["{", "<body>", "}"]],
    "<print_arg>": [["<expression>", "<print_argN>"]],
    "<print_argN>": [["ε"], [",", "<expression>", "<print_argN>"]],
    "<case_statement>": [["caseoh", "<constant>", ":", "<case_line>", "getout", "<case_statement>"], ["npc", ":", "<case_line>", "getout"]],
    "<for_initialization>": [["<data_id>", "<var_initialization>"]],
    "<constant>": [["CHU_LIT"], ["FORSEN_LIT"], ["LWK_LIT"]],
    "<return_value>": [["ε"], ["<expression>"]],
    "<case_line>": [["ε"], ["<data_id>", "<var_initialization>", "<case_line>"], ["<expression>", "<case_line>"], ["<statement>", "<case_line>"]]
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
'''
print("\n\nPREDICT SET:")
for (lhs, prod), predict_set in predict_sets.items():
    print(f"Predict({lhs} → {' '.join(prod)}) = {predict_set}\n")