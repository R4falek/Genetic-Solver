import random
import Generator
import Selection
import SaveAndRead


class Solver:
    def __init__(self, max_len=30, pop_size=100, generations=100, t_size=2, add_best=False, grow_if_stuck=False):
        self.add_best = add_best
        self.MAX_LEN = max_len
        self.POP_SIZE = pop_size
        self.GENERATIONS = generations
        self.T_SIZE = t_size
        self.CROSSOVER_PROB = 0.7
        self.fitness_best = 0
        self.CYCLES_LIMIT = 100
        self.population = []
        self.var_range = 'a-d'
        self.log_file = 'solver_logs.txt'
        self.grow_if_stuck = grow_if_stuck
        self.grow_tick = 10
        self.gens_to_trigger_grow = 30
        self.max_len_after_grow = 500

    def set_up(self):
        open(self.log_file, 'w').close()
        for i in range(self.POP_SIZE):
            individual = Generator.run_generator(var_range=self.var_range, len=self.MAX_LEN)
            self.population.append(individual)
        if self.add_best:
            self.population[0] = SaveAndRead.read('best.pickle')
        return self.population

    def print_parameters(self):
        print("MAX_LEN =", self.MAX_LEN, "POP_SIZE =", self.POP_SIZE, "GENERATIONS =", self.GENERATIONS, "T_SIZE =", self.T_SIZE)

    def evolve(self):
        self.set_up()
        self.print_parameters()
        instructions = ['loop', 'condition', 'var_declaration', 'var_assignment', 'read', 'write']
        acceptable_types = ['loop', 'condition', 'var_assignment', 'read', 'write', 'NAME', 'INTEGER_NUMBER', 'comparisons']

        last_gen_fitness = None
        gens_to_trigger_grow = self.gens_to_trigger_grow
        for i in range(self.GENERATIONS):
            best_individual = Selection.best_from_n_individuals(self.population, self.POP_SIZE)
            SaveAndRead.save("best.pickle", best_individual)
            tournament_winners = Selection.tournament_selection(self.population, self.T_SIZE)
            new_population = tournament_winners
            new_population.append(best_individual)
            fitness = Selection.fitness(best_individual, self.CYCLES_LIMIT)
            print("Generation: " + str(i) + " fitness: " + str(fitness) + " best:", best_individual.to_string())
            SaveAndRead.save_step(i, fitness, best_individual, self.log_file)

            if self.grow_if_stuck:
                if last_gen_fitness == fitness:
                    if gens_to_trigger_grow == 0:
                        gens_to_trigger_grow = self.gens_to_trigger_grow
                        self.MAX_LEN += self.grow_tick
                    else:
                        gens_to_trigger_grow -= 1
                else:
                    gens_to_trigger_grow = self.gens_to_trigger_grow
            last_gen_fitness = fitness

            if fitness == self.fitness_best:
                print("PROBLEM SOLVED")
                return

            for k in range(len(tournament_winners) - 1):
                if random.random() < self.CROSSOVER_PROB:
                    parent1 = tournament_winners[k]
                    parent2 = tournament_winners[random.randint(0, len(tournament_winners) - 1)]
                    child = parent1.crossover(instructions, parent2)
                    new_population.append(child)
                else:
                    parent = tournament_winners[k]
                    child = parent.mutate(acceptable_types, instructions)
                    new_population.append(child)

            while len(new_population) < self.POP_SIZE:
                individual = Generator.run_generator(var_range=self.var_range, len=self.MAX_LEN)
                new_population.append(individual)
            self.population = new_population

        print("PROBLEM NOT SOLVED")