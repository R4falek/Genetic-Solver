class Node:
    def __init__(self, parent=None, children=None):
        self.children = []
        self.parent = parent
        self.grammar_type = None
        self.value = None

        if children is not None:
            for child in children:
                self.add_child(child)

    def add_child(self, child):
        child.parent = self
        self.children.append(child)

    def add_child_at_id(self, child, id):
        child.parent = self
        self.children.insert(id, child)

    def is_root(self):
        if self.parent is None:
            return True
        else:
            return False

    def depth(self):  # Depth of current node
        if self.is_root():
            return 0
        else:
            return 1 + self.parent.depth()

    def show(self):
        print(str(self.grammar_type), str(self.value))
        return str(self.grammar_type) + str(self.value)
