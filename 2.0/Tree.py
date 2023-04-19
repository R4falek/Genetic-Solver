import copy
import random
import rstr
import Generator


class Tree:
    def __init__(self):
        self.root = None
        self.height = 0
        self.nodes = []
        self.vars = {}

    def insert(self, node, parent=None):
        if parent is not None:
            parent.add_child(node)
        else:
            if self.root is None:
                self.root = node
        self.nodes.append(node)

    def get_node(self, id):
        return self.nodes[id]

    def get_nodes_by_grammar_type(self, grammar_type):
        ret = []
        for node in self.nodes:
            if node.grammar_type == grammar_type:
                ret.append(node)
        return ret

    def get_random_node(self, grammar_type=None):
        if grammar_type is not None:
            nodes = self.get_nodes_by_grammar_type(grammar_type)
            if len(nodes) != 0:
                return nodes[random.randint(0, len(nodes) - 1)]
            else:
                return None
        else:
            return self.get_node(random.randint(0, len(self.nodes) - 1))

    def get_leafs(self):
        leafs = []

        def _get_leaf_nodes(node):
            if node is not None:
                if len(node.children) == 0:
                    leafs.append(node)
                for n in node.children:
                    _get_leaf_nodes(n)

        _get_leaf_nodes(self.root)
        return leafs

    def show(self):
        def show_children(node, depth):
            for child in node.children:
                for i in range(depth):
                    print("- ", end="")
                print(child.grammar_type, child.value)
                if len(child.children) != 0:
                    show_children(child, depth + 1)
        depth = 1
        curr = self.root
        print(curr.grammar_type, " ", curr.value)
        show_children(curr, depth)

    def to_string(self):
        ret = ""
        for l in self.get_leafs():
            if l.value is not None:
                ret += str(l.value) + " "
        return ret

    def delete(self, node):
        if node.is_root():
            return

        def delete_children(node):
            for child in node.children:
                delete_children(child)
                child.children.clear()
                self.nodes.remove(child)
        delete_children(node)
        node.parent.children.remove(node)
        self.nodes.remove(node)

    def mutate(self, acceptableTypes, instructions):
        mutated = copy.deepcopy(self)

        toChange = mutated.nodes[0]
        while toChange.grammar_type not in acceptableTypes:
            toChange = mutated.get_random_node()
        # print("to change: ", end="")
        # toChange.show()

        def change_node(newValue):
            for node in mutated.nodes:
                if node == toChange:
                    node.value = newValue

        if toChange.grammar_type == 'INTEGER_NUMBER':
            newNumber = random.randrange(1000)
            change_node(newNumber)
            # print(newNumber)

        elif toChange.grammar_type == 'NAME':
            newName = rstr.xeger(r'[a-d]')
            change_node(newName)
            # print(newName)

        elif toChange.grammar_type == 'comparisons':
            newInstruction = Generator.run_generatorMut("c")
            # print("new instruction: ", newInstruction.to_string())
            # toChange.parent.show()

            parent = toChange.parent
            to_change_id = -1
            for child in parent.children:
                to_change_id += 1
                if child == toChange:
                    break

            mutated.add_with_id(newInstruction.root, toChange.parent, to_change_id)
            mutated.delete(toChange)

        elif toChange.grammar_type in instructions:
            newInstruction = Generator.run_generatorMut("i")
            # print("new instruction: ", newInstruction.to_string())
            # toChange.parent.show()
            mutated.add(newInstruction.root, toChange.parent)
            mutated.delete(toChange)

        return mutated

    def add(self, start, parent):

        def add_children(node):
            for child in node.children:
                add_children(child)
                self.nodes.append(child)

        add_children(start)
        self.nodes.append(start)
        parent.add_child(start)

    def add_with_id(self, start, parent, index):

        def add_children(node):
            for child in node.children:
                add_children(child)
                self.nodes.append(child)

        add_children(start)
        self.nodes.append(start)
        parent.add_child_at_id(start, index)

    def check_comp(self, to_remove, tree):
        if to_remove.grammar_type == 'comparisons':
            for node in tree.nodes:
                if node.grammar_type == 'comparisons':
                    return True
        return False

    def crossover(self, instructions, tree):
        crossed = copy.deepcopy(self)
        tree = copy.deepcopy(tree)

        res = 0
        to_remove = crossed.nodes[0]
        while to_remove.grammar_type not in instructions:
            to_remove = crossed.get_random_node()

            #sprawdzamy czy comparisons
            if self.check_comp(to_remove, tree):
                res = 1
                break

        parent = to_remove.parent
        to_remove_id = -1
        for child in parent.children:
            to_remove_id += 1
            if child == to_remove:
                break

        to_add = tree.nodes[0]
        if res == 1:
            to_add = tree.get_random_node(grammar_type='comparisons')
        else:
            while to_add.grammar_type not in instructions:
                to_add = tree.get_random_node()

        crossed.add_with_id(to_add, parent, to_remove_id)
        crossed.delete(to_remove)

        return crossed
