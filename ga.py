import random
from solver import bfs_solve

ROWS, COLS = 10, 10

def create_map():
    grid = [['.' for _ in range(COLS)] for _ in range(ROWS)]

    for i in range(ROWS):
        for j in range(COLS):
            if random.random() < 0.3:
                grid[i][j] = '#'

    grid[0][0] = 'S'
    grid[ROWS-1][COLS-1] = 'E'
    return grid

def create_population(n):
    return [create_map() for _ in range(n)]

def fitness_function(grid):
    solvable, path_len = bfs_solve(grid)

    if not solvable:
        return -1000

    return path_len

def select_best(population):
    return sorted(population, key=fitness_function, reverse=True)[:5]

def crossover(p1, p2):
    child = []
    for r in range(ROWS):
        row = []
        for c in range(COLS):
            row.append(p1[r][c] if random.random() < 0.5 else p2[r][c])
        child.append(row)

    child[0][0] = 'S'
    child[ROWS-1][COLS-1] = 'E'
    return child

def mutate(grid):
    for r in range(ROWS):
        for c in range(COLS):
            if random.random() < 0.05:
                grid[r][c] = '#' if grid[r][c] == '.' else '.'

    grid[0][0] = 'S'
    grid[ROWS-1][COLS-1] = 'E'
    return grid