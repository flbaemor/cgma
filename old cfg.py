cfg = {
    "<program>": [["<start>"]],
    "<start>":[["<global_declaration>", "<nl>", "<start>"],
        ["chungus", "<chungus_follow>"]],
    "<chungus_follow>":[["<identifier>", "<declaration_tail>", "<nl>", "<start>"], 
        ["skibidi", "(", ")", "{", "<nl>", "<body_main>", "back", "0", "<nl>", "}"]],
    "<global_declaration>":[["<constant_var>"], 
        ["<gldata_type>", "<identifier>", "<declaration_tail>"],
        ["<id1>"]],
    "<gldata_type>":[["forsen"], 
        ["forsencd"], 
        ["chudeluxe"], 
        ["lwk"]
        ["aura"],
        ["nocap"]],
    "<data_type>":[["chungus"],
        ["<gldata_type>"]],
    "<body>":[["<declaration>", "<nl>", "<body>"],
        ["<statement>", "<nl>", "<body>"],
        ["back", "<return_value>", "<nl>"],
        ["ε"]],
    "<expression>":[["<operand>", "<expression_tail>"]],
    "<operand>":[["(", "<oppar>"],
        ["!", "<bool_operand>"],
        ["-", "<arith_operand>"],
        ["<prepost_operator>", "<identifier>"],
        ["CHU_LIT"],
        ["CHUDEL_LIT"],
        ["FORSEN_LIT"],
        ["FORSENCD_LIT"],
        ["LWK_LIT"],
        ["<identifier>", "<post_operand>"]],
    "<bool_operand>":[["LWK_LIT"],
        ["<identifier>"],
        ["(", "<expression>", ")"]],
    "<arith_operand>":[["CHU_LIT"],
        ["CHUDEL_LIT"],
        ["<identifier>"],
        ["(", "<expression>", ")"]],
    "<prepost_operator>":[["--"], ["++"]],
    "<expression_tail>":[["<operator>", "<operand>", "<expression_tail>"],
        ["<dot_suffix>"],
        ["ε"]],
    "<post_operand>":[["<prepost_operator>"], 
        ["ε"]],
    "<prepost_operator>":[["--"], 
        ["++"]],
    "<expression_tail>":[["<operator>", "<operand>", "<expression_tail>"],
        ["<dot_suffix>"],
        ["ε"]],
    "<value>":[["<list_value>"],
        ["<expression>"],
        ["chat()"],
        ["<multi_struct_val>"]],
    "<multi_struct_val>":[["{", "<identifier>", "=", "<expression>", "<struct_init_tail>", "}"]],
    "<struct_init_tail>":[[",", "<identifier>", "=", "<expression>", "<struct_init_tail>"], 
        ["ε"]],
    "<dtype1>":[["chungus"],
        ["chudeluxe"]],
    "<oppar>":[["<dtype1>", ")", "<expression>"],
        ["<expression>", ")"]],
    "<operator>":[["+"], 
        ["-"], 
        ["*"], 
        ["/"], 
        ["%"],
        ["=="], 
        ["!="], 
        [">"], 
        ["<"], 
        [">="], 
        ["<="], 
        ["&&"], 
        ["||"]],
    "<identifier>":[["IDENTIFIER", "<struct_id>", "<identifier_postfix>"]],
    "<identifier_postfix>":[["<dot_suffix>"], 
        ["(", "<postfix_content>", ")"], 
        ["ε"]],
    "<struct_id>":[["IDENTIFIER"], ["ε"]],
    "<dot_suffix>":[["<index>"], 
        [".", "<dot_suffix_content>"]],
    "<dot_suffix_content>":[["ts()"], 
        ["taper()"], 
        ["IDENTIFIER", "<dot_suffix>"]],
    "<postfix_content>":[["<parameter>"], 
        ["<arg>"], 
        ["ε"]],
    "<index>":[["[", "<expression>", "]"]],
    "<arg>":[["<expression>", "<arg_tail>"]],
    "<arg_tail>":[[",", "<expression>", "<arg_tail>"], 
        ["ε"]],
    "<parameter>":[["<data_id>", "<parameter_tail>"]],
    "<parameter_tail>":[[",", "<data_id>", "<parameter_tail>"], 
        ["ε"]],
    "<data_id>":[["<data_type>", "<identifier>"]],
    "<constant_var>":[["sturdy", "<data_id>", "<var_initialization>"]],
    "<declaration>":[["<data_id>", "<declaration_tail>"],
        ["<constant_var>"],
        ["<id1>"]],
    "<declaration_tail>":[["<var_initialization>"],
        ["{", "<nl>", "<body>", "}"],
        ["ε"]],
    "<var_initialization>":[["=", "<value>", "<var_init_tail>"]],
    "<var_init_tail>":[[",", "<identifier>", "<var_initialization>"], 
        ["ε"]],
    "<statement>":[
        ["yap", "(", "<print_arg>", ")"],
        ["lethimcook", "(", "<identifier>", ")", "{", "<nl>", "<case_statement>", "}"],
        ["plug", "(", "<for_initialization>", ";", "<expression>", ";", "<id1>", ")", "{", "<nl>", "<body>", "}"],
        ["lil", "{", "<nl>", "<body>", "}", "jit", "(", "<expression>", ")"],
        ["jit", "(", "<expression>", ")", "{", "<nl>", "<body>", "}"],
        ["<if_statement>"],
        ["pause"]],
    "<if_statement>":[["tuah", "(", "<expression>", ")", "{", "<nl>", "<body>", "}", "<if_tail>"]],
    "<if_tail>":[["hawk", "<hawk_follow>"],
        ["ε"]],
    "<hawk_follow>":[["<if_statement>"],
        ["{", "<nl>", "<body>", "}"]],
    "<print_arg>":[["<expression>", "<print_argN>"]],
    "<print_argN>":[[",", "<expression>", "<print_argN>"],
        ["ε"]],
    "<case_statement>":[["caseoh", "<constant>", ":", "<nl>", "<case_line>", "getout", "<nl>", "<case_statement>"],
        ["npc", ":", "<nl>", "<case_line>", "getout", "<nl>"]],
    "<for_initialization>":[["<data_id>", "<var_initialization>"],
        ["<id1>"]],
    "<constant>":[["CHU_LIT"],
        ["FORSEN_LIT"],
        ["LWK_LIT"]],
    "<return_value>":[["<expression>"],
        ["ε"]],
    "<case_line>":[["<data_id>", "<var_initialization>", "<nl>", "<case_line>"],
        ["<id1>", "<nl>", "<case_line>"],
        ["<statement>", "<nl>", "<case_line>"],
        ["ε"]],
    "<list_value>":[["append", "(", "<arg>", ")"],
        ["insert", "(", "CHU_LIT", ",", "<arg>", ")"],
        ["remove", "(", "CHU_LIT", ")"],
        ["[", "<list_content>", "]"]],
    "<list_content>":[["<arg>"],
        ["ε"]],
    "<nl>":[["\n"]],
    "<id1>":[["<prepost_operator>", "<identifier>"],
        ["<identifier>", "<id1_follow>"]],
    "<id1_follow>":[["<post_operand>"],
        ["<var_initialization>"]]
}


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
    "<dot_suffix_struct>": [["ε"], ["dot_suffix"]],
    "<dot_suffix_content>": [["ts", "(", ")"], ["taper", "(", ")"], ["IDENTIFIER", "<dot_suffix_struct>"]],
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