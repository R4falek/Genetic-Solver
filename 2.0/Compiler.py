import sys
from enum import unique
import Parser


def compile_program(program, cycles_limit, input_vector, output_file):
    python_program = Parser.to_python(program, input_vector, cycles_limit, output_file)
    try:
        exec(python_program)
    except:
        None
    sys.stdout = sys.__stdout__
    return python_program


def compile(program, cycles_limit, input_file='input.txt', output_file='output.txt'):
    #print("compiling ", program)
    res = []
    ret_vars = []
    with open(input_file) as file:
        lines = [line.rstrip() for line in file]
    for line in lines:
        res.append(compile_program(program, cycles_limit, line.split(' ')[:-1], output_file))
        ret_vars.append(get_return_values(output_file))
    return [ret_vars, res]


def unique(list1):
    unique_list = []
    for x in list1:
        if x not in unique_list:
            unique_list.append(x)
    return unique_list


def get_return_values(output_file):
    with open(output_file) as file:
        lines = [line.rstrip() for line in file]
    lines = unique(lines)
    return lines


# --- TEST ---
# program = 'main {   read ( b ) c = c loop ( c equals b ) { loop ( d equals b ) { b = a + c write ( a ) loop ( a equals b & c equals 603 ) { condition ( c equals 293 | d equals d ) { } } } } } '
# program = 'main { read ( c ) write ( c ) c = c + 2 write ( c ) }'
# res = compile(program, 100)
# print(res[0])
# print(res[1][2])
