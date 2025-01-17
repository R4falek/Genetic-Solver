# Genetic Programming Solver

This project implements a genetic algorithm-based solver that can evolve programs to solve problems, such as arithmetic tasks, logical gate operations, and more.
The solver generates random programs using a custom grammar, evaluates them (translating into Python code, assessing performance based 
on a fitness function) and evolves a population of programs using genetic operations like mutation, crossover, and selection.

## Features

- **Custom Grammar**: Define programs using a custom grammar implemented with PLY.
- **Program Representation**: Programs are represented as trees for easy mutation and crossover operations.
- **Genetic Operations**: Supports mutation, crossover, and tournament selection to evolve programs.
- **Tournament Selection**: Select the fittest programs for the next generation.
- **Translation to Python**: Programs are translated into Python code for evaluation.
- **Cycle Limitation**: Prevent infinite loops by capping execution cycles.
- **Fitness Evaluation**: Translate programs to Python, execute, and evaluate fitness.
- **Flexible Fitness Function**: Inject custom fitness functions via separate files.
- **Evolution Strategy**: Supports adaptive program growth when progress stagnates (grow_if_stuck).
- **Persistence**: Save and load individuals or evolutionary data from files.

## How It Works

1. **Program Generation**: Programs are generated using the Grow method based on a predefined grammar.
2. **Fitness Evaluation**: The program is executed with an input vector, and the output is evaluated against expected results.
3. **Selection**: The best programs are selected using a tournament-based selection process.
4. **Mutation & Crossover**: Selected programs undergo mutation and crossover to generate new offspring.
5. **Termination**: The solver stops once a program achieves the desired result (fitness score of 0).

## Tools
- Python: The main programming language used.
- PLY: Python Lex-Yacc library for creating the custom grammar.

## Use Case: Boolean AND Function for k = 2

### Generated Program (After 12 Generations):

`main { read ( d ) read ( c ) read ( c ) loop ( d equals a ) { write ( c ) } condition ( c equals 54 ) { } write ( d ) loop ( a equals a ) { } }`

### Input vector and generated program output

```
a b   expected                output
1 1       1                  ['c:  1']
0 0       0                  ['d:  0']
1 0       0                  ['c:  0']
0 1       0                  ['d:  0']
```
