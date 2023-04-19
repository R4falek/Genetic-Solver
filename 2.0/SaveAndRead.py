import pickle
import Compiler

def save(fname, tree):
    with open(fname, 'wb') as handle:
        pickle.dump(tree, handle, protocol=pickle.HIGHEST_PROTOCOL)

def read(fname):
    with open(fname, 'rb') as handle:
        return pickle.load(handle)

def readString(fname):
    with open(fname) as file:
        program = file.read().rstrip()
        return program

def compile_from_file(fname='best.pickle'):
    program = read(fname)
    res = Compiler.compile(program.to_string(), 100)
    print(res[0])
    print(program.to_string())

def save_step(generation, fitness, individual, fname):
    log = str(generation) + ', ' + str(fitness) + ', ' + individual.to_string() + '\n'
    with open(fname, 'a') as file:
        file.write(log)
