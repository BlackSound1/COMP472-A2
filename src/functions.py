from puzzle_state import PuzzleState
from random import shuffle
import re


def create_random_puzzle(size):
    random_list = list(range(1, size ** 2 + 1))
    shuffle(random_list)
    return PuzzleState([random_list[x:x + size] for x in range(0, len(random_list), size)], 0)


def create_20_random_puzzles(size: int = 3) -> None:
    """Create 20 random puzzles and save them to a file, as well as its goal state

    :param size: The size of the puzzle
    :returns None

    Optional argument size is the size of the puzzle.
    Generates a size X size puzzle. Its default is 3 for a 3 x 3 puzzle.
    """

    list_of_possible_numbers = list(range(1, size ** 2 + 1))

    write_goal_state_to_file(list_of_possible_numbers, size)

    list_of_tuples = []

    for i in range(20):
        shuffle(list_of_possible_numbers)

        new_tuple = create_tuple_of_tuples_of_numbers(list_of_possible_numbers, size)

        list_of_tuples.append(new_tuple)

    write_puzzles_to_file(list_of_tuples)


def write_goal_state_to_file(list_of_possible_numbers, size):
    goal_state = create_tuple_of_tuples_of_numbers(list_of_possible_numbers, size)
    with open('../input/goal_state.txt', 'wt') as file:
        file.flush()
        file.write(str(goal_state))


def write_puzzles_to_file(tuple_of_tuples):
    with open('../input/input_puzzles.txt', 'w') as file:
        file.flush()
        for tup in tuple_of_tuples:
            file.write(str(tup) + '\n')


def create_tuple_of_tuples_of_numbers(list_of_possible_numbers, size):
    return tuple([tuple(list_of_possible_numbers[x: x + size]) for x in
            range(0, len(list_of_possible_numbers), size)])


def get_all_puzzles():
    with open('../input/input_puzzles.txt', 'r') as file:
        return file.readlines()


def get_goal_state():
    with open('../input/goal_state.txt', 'rt') as file:
        return file.readline()


def read_state(state: str):
    new_state = '(' + state.lstrip("(").rstrip(')\n') + ')'

    list_of_strings = re.findall('\((?:\d+,\s)+\d+\)', new_state)

    list_to_return = []

    for string in list_of_strings:
        list_of_nums = [int(x) for x in re.findall('\d+',string)]
        tup = tuple(list_of_nums)
        list_to_return.append(tup)

    return tuple(list_to_return)


def print_solution_path(solution_path):
    if solution_path:
        for index, state in enumerate(solution_path):
            print(state, state.level)
    else:
        print("no solution")
    print()
