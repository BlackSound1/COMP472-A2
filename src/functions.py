from puzzle_state import PuzzleState
from random import shuffle


def create_random_puzzle(size):
    random_list = list(range(1, size*size+1))
    shuffle(random_list)
    return PuzzleState([random_list[x:x + size] for x in range(0, len(random_list), size)], 0)


def create_20_random_puzzles(size: int = 3) -> None:
    """Create 20 random puzzles and save them to a file, return None

    Optional argument size is the size of the puzzle.
    Generates a size X size puzzle. Its default is 3 for a 3 x 3 puzzle.
    """

    list_of_possible_numbers = list(range(1, size ** 2 + 1))

    list_of_tuples = []

    for i in range(20):
        shuffle(list_of_possible_numbers)

        new_tuple = tuple([list_of_possible_numbers[x: x + size] for x in
                          range(0, len(list_of_possible_numbers), size)])

        list_of_tuples.append(new_tuple)

    with open('../input/input_puzzles.txt', 'wt') as file:
        file.flush()

        for tup in list_of_tuples:
            file.write(str(tup) + '\n')
