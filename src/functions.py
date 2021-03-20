from src.puzzle_state import PuzzleState
from random import shuffle


def create_random_puzzle(size):
    random_list = list(range(1, size ** 2 + 1))
    shuffle(random_list)
    return PuzzleState([random_list[x:x + size] for x in range(0, len(random_list), size)], 0)


def print_solution_path(puzzle_state):
    if puzzle_state:
        parent_state = puzzle_state.parent
        solution_path = [puzzle_state]
        while parent_state:
            solution_path.append(parent_state)
            parent_state = parent_state.parent
        solution_path.reverse()
        for index, state in enumerate(solution_path):
            print(state, state.level)
    else:
        print("no solution")
