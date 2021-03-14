from puzzle_state import PuzzleState
from random import shuffle


def create_random_puzzle(size):
    random_list = list(range(1, size*size+1))
    shuffle(random_list)
    return PuzzleState([random_list[x:x + size] for x in range(0, len(random_list), size)], 0)
