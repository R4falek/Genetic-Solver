import Parser
from Solver import Solver
import Generator
import SaveAndRead
import Compiler

##################SOLVER TEST##########################
solver = Solver(max_len=50, generations=1000, add_best=False, grow_if_stuck=False)
solver.evolve()

# program = SaveAndRead.read('dodawanie.pickle')
# res = Compiler.compile(program.to_string(), 100)
# print(res[0])
# print(res[1][0])

# p = Generator.run_generator('a-d', 40)
# SaveAndRead.save_step(1, 3, p, 'solver_logs.txt')
SaveAndRead.compile_from_file()
