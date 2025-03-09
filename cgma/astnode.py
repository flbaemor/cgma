class ASTNode:
    def __init__(self, type_, value=None, children=None):
        self.type = type_
        self.value = value
        self.children = children if children else []

    def add_child(self, child):
        self.children.append(child)

    def __repr__(self):
        return f"ASTNode(type={self.type}, value={self.value}, children={self.children})"