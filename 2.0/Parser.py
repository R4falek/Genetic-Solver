from ply import lex
from ply import yacc

#TOKENS

reserved = {
    'loop': 'LOOP',
    'condition': 'CONDITION',
    'main': 'MAIN',
    'read': 'READ',
    'write': 'WRITE',
    'equals': 'EQUALS' #w sensie ==
}

tokens = [
        'PLUS',
        'MINUS',
        'STAR',
        'SLASH',
        'EQUAL',
        'AND',
        'OR',
        'LP',
        'RP',
        'LPC',
        'RPC',
        'NAME',
        'INTEGER_NUMBER',
        'ID'
] + list(reserved.values())

t_PLUS = r'\+'
t_MINUS = r'\-'
t_STAR = r'\*'
t_SLASH = r'\/'
t_EQUAL = r'\='
t_AND = r'\&'
t_OR = r'\|'
t_LP = '\('
t_RP = r'\)'
t_LPC = r'\{'
t_RPC = r'\}'
t_NAME = r'[a-zA-Z_][a-zA-Z0-9_]*' #nazwa zmiennej
t_ignore = ' \t'

def t_INTEGER_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t


# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Check for reserved words
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'NAME')
    return t

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()

# # Test it out
# data = '''
#
#  '''
#
# # Give the lexer some input
# lexer.input(data)
#
# # Tokenize
# while True:
#     tok = lexer.token()
#     if not tok:
#         break  # No more input
#     print(tok)

def get_token(p):
    lexer.input(p)
    tok = lexer.token()
    return tok

#GRAMMAR

def p_program(p):
    '''
    program : main
    '''
    p[0] = p[1]

def p_empty(p):
    '''
    empty :
    '''
    p[0] = 'None\n'


def p_main(p):
    '''
    main : MAIN LPC instructions RPC
    '''
    p[0] = p[3]

def p_instructions(p):
    '''
    instructions : instruction
        | instruction instructions
        | empty

    '''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        p[0] = str(p[1]) + str(p[2])

def p_instruction(p):
    '''
    instruction : loop
        | condition
        | var_assignment
        | read
        | write
        | empty
    '''
    p[0] = p[1]

def p_loop(p):
    '''
    loop : LOOP LP comparisons RP LPC instructions RPC
    '''
    p[0] = 'while ' + p[3] + ':\n' + cycles_limit_check + p[6] + p[7] + '\n'

def p_condition(p):
    '''
    condition : CONDITION LP comparisons RP LPC instructions RPC
    '''
    p[0] = 'if ' + p[3] + ':\n' + cycles_limit_check + p[6] + p[7] + '\n'

cycles_limit_check = 'if cycles_limit < 1:\n exit(0)\n}\ncycles_limit -= 1\n'

def p_comparisons(p):
    '''
    comparisons : comparison
        | comparison logic_operator comparison
    '''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4:
        p[0] = p[1] + " " + p[2] + " " + p[3]

def p_comparison(p):
    '''
    comparison : NAME EQUALS number
            | NAME EQUALS NAME
    '''
    p[0] = p[1] + ' == ' + str(p[3])

def p_number(p):
    '''
    number : INTEGER_NUMBER
    '''
    p[0] = str(p[1])

def p_var_assignment(p):
    '''
    var_assignment : NAME EQUAL number
        | NAME EQUAL NAME
        | NAME EQUAL math_operation
    '''
    p[0] = p[1] + ' = ' + str(p[3]) + '\n' + cycles_limit_check

def p_math_operator(p):
    '''
    math_operator : PLUS
        | MINUS
        | STAR
        | SLASH
    '''
    p[0] = p[1]

def p_math_operation(p):
    '''
    math_operation : NAME math_operator NAME
        | NAME math_operator number
        | number math_operator number
    '''
    p[0] = str(p[1]) + " " + p[2] + " " + str(p[3])

def p_logic_operator(p):
    '''
    logic_operator : AND
        | OR
    '''
    if p[1] == '&':
        p[0] = 'and'
    if p[1] == '|':
        p[0] = 'or'

def p_read(p):
    #example: read(result)
    '''
    read : READ LP NAME RP
    '''
    global read_counter, variable_values

    # p[0] = p[3] + ' = ' + 'input ' + p[2] + variable_values[read_counter] + p[4] + '\n'
    p[0] = p[3] + ' = ' + variable_values[read_counter] + '\n' + cycles_limit_check
    if read_counter < len(variable_values) - 1:
        read_counter += 1

def p_write(p):
    '''
    write : WRITE LP NAME RP
    '''
    p[0] = 'print' + ' ' + p[2] + '\'' + p[3] + ': \', ' + 'int(' + p[3] + ')' + p[4] + '\n' + cycles_limit_check


# Error rule for syntax errors
def p_error(p):
    if p == None:
        token = "end of file"
    else:
        token = f"{p.type}({p.value}) on line {p.lineno}"
        print(f"Syntax error: Unexpected {token}")

def init_variables(program):
    variables = []
    lexer.input(program)
    while True:
        tok = lexer.token()
        if not tok:
            break
        if 'LexToken(NAME' == str(tok)[0:13]:
            if not variables.__contains__(str(tok)[15:16]):
                variables.append(str(tok)[15:16])
    ret = ''
    for var in variables:
        ret += var + ' = 1\n'
    return ret


def change_stduot_to_file(outfile='output.txt'):
    return 'import sys \nsys.stdout = open(\'' + outfile + '\', \'w\')\n'


variable_values = []
read_counter = 0


def to_python(program, var_values, cycles_limit, output_file):
    global variable_values, read_counter
    read_counter = 0
    variable_values = var_values

    program_copy = program
    parser = yacc.yacc()
    program = parser.parse(program)
    tab = 0
    program = iter(program.splitlines())
    ready_to_compile = ''
    for line in program:
        if line == '}':
            tab -= 1
        ready_to_compile += line + '\n'
        if line.split()[0] == 'if' or line.split()[0] == 'while':
            tab += 1
        for i in range(tab):
            ready_to_compile += '\t'
    tmp = ready_to_compile.splitlines()
    ready_to_compile = ''
    for line in tmp:
        if '}' not in line:
            ready_to_compile += line + '\n'
    return change_stduot_to_file(output_file) + 'cycles_limit = ' + str(cycles_limit) + '\n' + init_variables(program_copy) + ready_to_compile


def get_tokens(p):
    lexer.input(p)
    tokens = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        tokens.append(tok)
    return tokens

# --- TEST ---
# program = '''
#     main {  D = b / 170 condition ( i equals y & k equals f ) { read ( W ) X = 469 - 993 } write ( d ) write ( W ) write ( Q ) loop ( k equals S ) {  M = X loop ( F equals 392 | M equals g ) { M = U write ( g ) } condition ( l equals 783 | r equals k ) { condition ( j equals d | G equals 985 ) { write ( u ) write ( h )  } } } read ( B ) loop ( G equals K & m equals q ) { write ( Q ) } loop ( D equals r & I equals i ) { loop ( n equals V & H equals 422 ) { write ( D ) } }  write ( r ) d = 504 E = B loop ( M equals n & R equals 54 ) { write ( H ) } loop ( v equals k & W equals R ) { condition ( O equals 449 ) { condition ( L equals j ) { Q = 869 } } } loop ( Z equals 916 | Q equals s ) { read ( Q ) read ( q ) }  loop ( v equals 115 & d equals 840 ) { condition ( v equals C ) { condition ( n equals v | l equals M ) { write ( r ) N = C } } } write ( V )  write ( m ) D = 456 read ( l )   a = g loop ( k equals L | Y equals f ) { loop ( Z equals 968 ) { condition ( i equals F ) { Y = V } } loop ( K equals 19 & m equals 787 ) { condition ( g equals 282 ) { read ( H ) read ( H ) read ( i ) read ( Z )  read ( D ) read ( o ) } loop ( X equals q ) { write ( A ) } condition ( M equals M ) { condition ( O equals 562 ) { condition ( a equals r & h equals u ) { condition ( F equals 461 ) { write ( B ) f = S }  } } } k = 793 / 107 loop ( c equals L & d equals 537 ) { condition ( R equals 781 ) { write ( U ) Z = n read ( g ) } condition ( H equals w ) { loop ( k equals X ) { condition ( i equals 635 & l equals 117 ) { N = 644 } loop ( T equals c ) { read ( i ) condition ( a equals b ) {  Y = 801 - 864 Z = d }  read ( i ) } } loop ( b equals 159 ) { read ( M ) write ( l ) read ( h ) write ( z ) read ( R ) } L = 664 } } } v = 692 - 259 } i = 774  H = Y + 768  write ( b ) write ( b ) condition ( a equals E | I equals 10 ) { t = 754 }  loop ( C equals 542 & C equals e ) { write ( j ) Y = 259 - 502 } loop ( g equals J ) {  }   write ( p ) Y = 586 + 556 write ( X ) loop ( K equals x & p equals R ) { c = 969 * 54 read ( J ) }  loop ( Z equals 794 & K equals B ) { read ( L )  I = 836 write ( g ) } condition ( s equals 769 ) { loop ( E equals c | j equals 995 ) { W = A / X } } read ( V ) condition ( X equals 90 ) { loop ( O equals o & O equals H ) { condition ( N equals 2 ) { condition ( S equals 642 & W equals w ) { read ( X ) read ( q ) } } read ( n ) loop ( q equals 837 & u equals 951 ) { condition ( c equals 327 ) { m = g  } read ( O ) loop ( d equals 838 & C equals 426 ) { read ( R )  } loop ( c equals 613 ) { write ( i ) write ( C ) } condition ( E equals 140 ) {  } } } read ( y ) condition ( N equals j ) { write ( O ) condition ( J equals 142 ) { U = X * 454 condition ( t equals e ) {  c = o write ( U ) write ( A ) }  } Q = U loop ( t equals 600 | W equals 295 ) { condition ( q equals 647 | B equals 21 ) { loop ( b equals 685 & B equals L ) { write ( Z ) b = 261 } } loop ( P equals 451 ) { write ( o ) } write ( d ) } a = I G = T S = B condition ( G equals I ) { l = h / x } write ( C ) } } loop ( P equals W | i equals 753 ) { y = 763 } write ( v ) read ( Y ) condition ( e equals 883 ) { } }
# '''
# parser=yacc.yacc()
# res = parser.parse(program)

