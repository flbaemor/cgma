cfg = {
    "<program>": [["<start>"]],
    "<start>":[["<global_declaration>", "<start>"],["chungus", "<chungus_follow>"]],
    "<chungus_follow>":[["<identifier>", "<declaration_tail>", "<start>"], ["skibidi", "(", ")", "{", "<body_main>", "back", "0", "}"]],
    "<global_declaration>": [["<constant_var>"], ["<gldata_type>", "<identifier>", "<declaration_tail>"], ["<expression>"]],
}