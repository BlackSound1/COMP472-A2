
from functions import *


def main():
    create_20_random_puzzles()
    goal_state = read_state(get_goal_state())
    puzzles = [read_state(x) for x in get_all_puzzles()]
    time_limit = 60

    test_Astar_on_puzzles(goal_state, puzzles, time_limit)
    test_dfs_on_puzzles(goal_state, puzzles, time_limit)
    test_iter_deepening_on_puzzles(goal_state, puzzles, 100, time_limit)

    # testing()


def test_Astar_on_puzzles(goal: tuple, puzzles: list, time_limit) -> None:
    """ Runs the A* algorithm on all puzzles using each heuristic.

    The heuristics we use are: sum permutation, Hamming distance, and a
    modified version of the Manhattan distance.
    :param goal: The goal state
    :param puzzles: All the puzzles being solved
    :return: None
    """
    print("------------")
    print("A* ALGORITHM")
    print("------------")

    heuristics = [PuzzleState.sum_permutation, PuzzleState.hamming_distance, PuzzleState.manhattan_distance]
    for heuristic in heuristics:

        length_solution = []
        length_search = []
        nb_no_solution = 0
        search_cost = []
        solution_cost = []
        execution_time = []

        print(heuristic.__name__, "path")
        for idx, puzzle in enumerate(puzzles, 1):
            print("\nPuzzle", idx, puzzle)
            start = puzzle

            start_state = PuzzleState(start, 0)
            goal_state = PuzzleState(goal, 0)
            solution_path, search_path, elapsed = PuzzleState.a_star(start_state, goal_state, heuristic, time_limit)

            output_to_files("A_Star", idx, search_path, solution_path, elapsed, heuristic=heuristic.__name__)

            if elapsed > time_limit:
                nb_no_solution += 1
                print("no solution")
            else:
                length_search.append(len(search_path))
                length_solution.append(len(solution_path))
                execution_time.append(elapsed)
                total_search = 0
                for node in search_path:
                    total_search += node.get_f_value()[0]
                total_sol = 0
                for node in solution_path:
                    total_sol += node.get_f_value()[0]
                search_cost.append(total_search)
                solution_cost.append(total_sol)

                print("Time taken: " + str(elapsed))

        print_astar_data(heuristic,
                         length_solution,
                         length_search,
                         solution_cost,
                         search_cost,
                         execution_time,
                         nb_no_solution)


def test_dfs_on_puzzles(goal: tuple, puzzles: list, time_limit) -> None:
    """ Runs the DFS algorithm on all puzzles

    :param goal: The goal state
    :param puzzles: All the puzzles being solved
    :return: None
    """
    print("----------------------------")
    print("DEPTH-FIRST SEARCH ALGORITHM")
    print("----------------------------")

    length_solution = []
    length_search = []
    nb_no_solution = 0
    execution_time = []

    for idx, puzzle in enumerate(puzzles, 1):
        print("\nPuzzle", idx, puzzle)
        start = puzzle

        start_state = PuzzleState(start, 0)
        goal_state = PuzzleState(goal, 0)

        dfs_solution_path, dfs_search_path, elapsed = PuzzleState.depth_first_search(start_state, goal_state, time_limit)
        
        output_to_files("DFS", idx, dfs_search_path, dfs_solution_path, elapsed)

        if elapsed > time_limit:
            nb_no_solution += 1
            print("no solution")
        else:
            length_search.append(len(dfs_search_path))
            length_solution.append(len(dfs_solution_path))
            execution_time.append(elapsed)

            print("Time taken: " + str(elapsed))

    print(f"---DFS data---")
    print_data(length_solution, length_search, execution_time, nb_no_solution)


def test_iter_deepening_on_puzzles(goal: tuple, puzzles: list, max_depth: int, time_limit) -> None:
    """ Runs the DFS algorithm with iterative deepening on all puzzles

    :param goal: The goal state
    :param puzzles: All the puzzles being solved
    :param max_depth: The maximum depth to search to before concluding that there is no solution
    :return: None
    """
    print("-----------------------------")
    print("ITERATIVE DEEPENING ALGORITHM")
    print("-----------------------------")

    length_solution = []
    length_search = []
    nb_no_solution = 0
    execution_time = []

    for idx, puzzle in enumerate(puzzles, 1):
        print("\nPuzzle", idx, puzzle)
        start = puzzle

        start_state = PuzzleState(start, 0)
        goal_state = PuzzleState(goal, 0)

        iter_solution_path, iter_search_path, elapsed = PuzzleState.iterative_deepening(start_state, goal_state, max_depth, time_limit)

        output_to_files("Iter_Deepening", idx, iter_search_path, iter_solution_path, elapsed)

        if elapsed > time_limit:
            nb_no_solution += 1
            print("no solution")
        else:
            length_search.append(len(iter_search_path))
            length_solution.append(len(iter_solution_path))
            execution_time.append(elapsed)

            print("Time taken: " + str(elapsed))

    print(f"---Iterative Deepening data---")
    print_data(length_solution, length_search, execution_time, nb_no_solution)


if __name__ == '__main__':
    main()
