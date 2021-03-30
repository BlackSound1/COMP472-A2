from puzzle_state import PuzzleState
from random import shuffle
import re
import os


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


def testing():
    # Tests
    state = PuzzleState(((1, 2, 3), (4, 5, 6), (7, 8, 9)))
    goal = PuzzleState(((2, 1, 3), (9, 6, 4), (7, 8, 5)))
    assert PuzzleState.hamming_distance(state, goal) == 6
    assert PuzzleState.manhattan_distance(state, goal) == 10
    assert PuzzleState.sum_permutation(state, goal) == 10

    state = PuzzleState(((1, 2), (3, 4)))
    goal = PuzzleState(((4, 3), (1, 2)))
    assert PuzzleState.hamming_distance(state, goal) == 4
    assert PuzzleState.manhattan_distance(state, goal) == 6
    assert PuzzleState.sum_permutation(state, goal) == 5

    # Test A* using all heuristics
    start_state = create_random_puzzle(3)
    goal_state = create_random_puzzle(3)
    heuristics = [PuzzleState.sum_permutation, PuzzleState.hamming_distance, PuzzleState.manhattan_distance]
    print("start:", start_state)
    print("goal:", goal_state)

    for heuristic in heuristics:
        print(heuristic.__name__, "path")
        search_list = PuzzleState.a_star(start_state, goal_state, heuristic)

        for index, state in enumerate(search_list):
            print(state, state.level)


def output_to_files(puzzle_type: str, puzzle_number: int, search_path: str, solution_path: str, elapsed, heuristic=None):
    directory = f'../output/{puzzle_type}/{puzzle_type}_Puzzle_{puzzle_number}'

    check_or_create_directory(directory)

    search_file, solution_file = get_search_and_solution_directories(directory, heuristic)

    # Write Search File
    write_to_search_file(search_file, search_path, elapsed)

    # Write Solution File
    write_to_solution_file(solution_file, solution_path, elapsed)


def write_to_solution_file(solution_file, solution_path, elapsed):
    with open(solution_file, 'wt') as file:
        file.write('Solution Path:\n')
        if elapsed > 60.0:
            file.write("no solution")
        else:
            for index, state in enumerate(solution_path):
                file.write('State: ' + str(state) + ' Level: ' + str(state.level) + '\n')
            file.write("Time taken: " + str(elapsed))


def write_to_search_file(search_file, search_path, elapsed):
    with open(search_file, 'wt') as file:
        file.write("Search Path:\n")
        if elapsed > 60.0:
            file.write("no solution")
        else:
            for index, state in enumerate(search_path):
                file.write("State: " + str(state) + ' Level: ' + str(state.level) + '\n')
            file.write("Time taken: " + str(elapsed))


def get_search_and_solution_directories(directory, heuristic):
    if heuristic is not None:
        if heuristic == "hamming_distance":
            hamming_directory = directory + '/Hamming_Distance'
            check_or_create_directory(hamming_directory)
            return hamming_directory + '/Search_Path.txt', hamming_directory + '/Solution_Path.txt'
        elif heuristic == "manhattan_distance":
            manhattan_directory = directory + '/Manhattan_Distance'
            check_or_create_directory(manhattan_directory)
            return manhattan_directory + '/Search_Path.txt', manhattan_directory + '/Solution_Path.txt'
        elif heuristic == "sum_permutation":
            sum_directory = directory + '/Sum_Permutation'
            check_or_create_directory(sum_directory)
            return sum_directory + '/Search_Path.txt', sum_directory + '/Solution_Path.txt'
    return directory + '/Search_Path.txt', directory + '/Solution_Path.txt'


def check_or_create_directory(directory):
    if not os.path.isdir(directory):
        os.makedirs(directory)


def print_astar_data(heuristic,
                     length_solution,
                     length_search,
                     solution_cost,
                     search_cost,
                     execution_time,
                     nb_no_solution):
    print(f"\nA* {heuristic.__name__} data")
    if length_solution:
        total_length_sol = sum(length_solution)
        print(f"Average length of solution path: {total_length_sol / len(length_solution)}")
        print(f"Total length of solution path: {total_length_sol}")

        total_length_search = sum(length_search)
        print(f"Average length of search path: {total_length_search / len(length_search)}")
        print(f"Total length of search path: {total_length_search}")

        total_sol_cost = sum(solution_cost)
        print(f"Average cost of solution path: {total_sol_cost / len(solution_cost)}")
        print(f"Total cost of solution path: {total_sol_cost}")

        total_search_cost = sum(search_cost)
        print(f"Average cost of search path: {total_search_cost / len(search_cost)}")
        print(f"Total cost of search path: {total_search_cost}")

        total_exec_time = sum(execution_time)
        print(f"Average execution time: {total_exec_time / len(execution_time)}")
        print(f"Total execution time: {total_exec_time}")

    print(f"Total number of no solution: {nb_no_solution}\n")


def print_data(length_solution, length_search, execution_time, nb_no_solution):
    if length_solution:
        total_length_sol = sum(length_solution)
        total_length_search = sum(length_search)

        print(f"Average length of solution path: {total_length_sol / len(length_solution)}")
        print(f"Total length of solution path: {total_length_sol}")

        print(f"Average length of search path: {total_length_search / len(length_search)}")
        print(f"Total length of search path: {total_length_search}")

        print(f"Average cost of solution path: {total_length_sol / len(length_solution)}")
        print(f"Total cost of solution path: {total_length_sol}")

        print(f"Average cost of search path: {total_length_search / len(length_search)}")
        print(f"Total cost of search path: {total_length_search}")

        total_exec_time = sum(execution_time)
        print(f"Average execution time: {total_exec_time / len(execution_time)}")
        print(f"Total execution time: {total_exec_time}")

    print(f"Total number of no solution: {nb_no_solution}\n")