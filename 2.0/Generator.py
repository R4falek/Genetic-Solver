import random
import sys
import rstr
from Tree import Tree
from Node import Node

grammar1 = {
        'S': [['program']],
        'program': [['MAIN', 'LPC', 'instructions', 'RPC']],
        'instructions': [['instruction'], ['instruction', 'instructions']],
        'instruction': [['loop'], ['condition'], ['var_assignment'], ['read'], ['write'], ['empty']],
        'loop': [['LOOP', 'LP', 'comparisons', 'RP', 'LPC', 'instructions', 'RPC']],
        'condition': [['CONDITION', 'LP', 'comparisons', 'RP', 'LPC', 'instructions', 'RPC']],
        'comparisons': [['comparison'], ['comparison', 'logic_operator', 'comparison']],
        'comparison': [['NAME', 'EQUALS', 'INTEGER_NUMBER'], ['NAME', 'EQUALS', 'NAME']],
        'var_assignment': [['NAME', 'EQUAL', 'INTEGER_NUMBER'], ['NAME', 'EQUAL', 'NAME'], ['NAME', 'EQUAL', 'math_operation']],
        'math_operator': [['PLUS'], ['MINUS'], ['STAR'], ['SLASH']],
        'math_operation': [['NAME', 'math_operator', 'NAME'], ['NAME', 'math_operator', 'INTEGER_NUMBER'],
                           ['INTEGER_NUMBER', 'math_operator', 'INTEGER_NUMBER']],
        'logic_operator': [['AND'], ['OR']],
        'read': [['READ', 'LP', 'NAME', 'RP']],
        'write': [['WRITE', 'LP', 'NAME', 'RP']],
    }

tokens = {
    'LOOP': 'loop',
    'CONDITION': 'condition',
    'MAIN': 'main',
    'READ': 'read',
    'WRITE': 'write',
    'EQUALS': 'equals',
    'empty': '',

    'PLUS': '+',
    'MINUS': '-',
    'STAR': '*',
    'SLASH': '/',
    'EQUAL': '=',
    'AND': '&',
    'OR': '|',
    'LP': '(',
    'RP': ')',
    'LPC': '{',
    'RPC': '}',
    'NAME': 'NAME_',
    'INTEGER_NUMBER': 'INT',
    'ID': 'ID_'
}


def __get_token(term):
    if term == 'NAME': #utworzenie nowej zmiennej lub wykorzystanie istniejącej z prawdopodobieństwem 50:50
        global variables
        global variables_all
        if random.random() < 0.5 and len(variables) > 0:
            index = random.randrange(0, len(variables))
            name = variables[index]
        else:
            first = variables_range[0]
            last = variables_range[-1]
            name = rstr.xeger(r'[' + first + '-' + last + ']')
            variables.append(name)
        return name
    if term == 'INTEGER_NUMBER':
        return random.randrange(1000)
    return tokens.get(term)


def __get_fraze(grammar, term):
    frazes = grammar.get(term)
    if frazes is None:
        return None
    random_fraze = frazes[random.randrange(len(frazes))]
    return random_fraze


def __run(grammar, start, tree, parent=None):
    global l
    if start is None or (start == "instructions" and l <= 0):
        return
    fraze = __get_fraze(grammar, start)

    for term in fraze:
        node = Node()
        node.grammar_type = term
        tree.insert(node, parent)

        if __get_fraze(grammar, term) is None:
            node.value = __get_token(term)
            l = l - 1
        else:
            __run(grammar, term, tree, node)


def __generate(tree):
    __run(grammar1, "S", tree)
    while l > 0:
        __run(grammar1, "instructions", tree, tree.nodes[3])


l = 0
variables_range = None
variables = []
variables_all = []
def run_generator(var_range='a-z', len=30):
    tree = Tree()
    global l
    global variables_range
    variables_range = var_range
    global variables
    global variables_all
    for v in variables:
        if v not in variables_all:
            variables_all.append(v)
    variables.clear()
    try:
        l = sys.argv[1]
    except:
        l = len
    __generate(tree)
    # print(l - 1)
    return tree


def __generateMut(tree):
    while l > 0:
        __run(grammar1, "instruction", tree)

def __generateCompar(tree):
    while l > 0:
        __run(grammar1, "comparisons", tree)

def run_generatorMut(whatGenerate, len=30):
    tree = Tree()
    global l
    try:
        l = sys.argv[1]
    except:
        l = len
    if whatGenerate == "i":
        __generateMut(tree)
    elif whatGenerate == "c":
        __generateCompar(tree)
    # print(l - 1)
    return tree
