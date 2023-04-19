import sys
import Compiler


def fitness(individual, cycles_limit=100, input_file='input.txt', fitness_file="fitness_function.py"):
    compilation_results = Compiler.compile(individual.to_string(), cycles_limit=cycles_limit)
    # compilation_results = Compiler.compile(individual, cycles_limit=cycles_limit)
    outputs = compilation_results[0]
    with open(input_file) as file:
        lines = [line.rstrip().split(' ')[-1] for line in file]
        targets = lines

    sys.argv = [outputs, targets]
    exec(open(fitness_file).read())

    return sys.argv[0]


def best_from_n_individuals(individuals, n):
    best = individuals[0]
    for i in range(n):
        if fitness(best) >= fitness(individuals[i]):
            best = individuals[i]
    return best


def tournament_selection(all_individuals, n):
    bests = []
    for i in range(int(len(all_individuals) / n)):
        bests.append(best_from_n_individuals(all_individuals[i * n: i * n + n], n))
    remaining_count = len(all_individuals) - len(bests) * n
    if remaining_count != 0:
        bests.append(best_from_n_individuals(all_individuals[len(bests) * n: len(all_individuals)], remaining_count))
    return bests
