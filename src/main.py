
from functions import *


def main():
    create_20_random_puzzles()

    goal_state = read_state(get_goal_state())

    puzzles = [read_state(x) for x in get_all_puzzles()]

    test_Astar_on_20_puzzles(goal_state, puzzles)
    test_dfs_on_20_puzzles(goal_state, puzzles)
    test_iter_deepening_on_20_puzzles(goal_state, puzzles, 100)

    # testing()


def test_Astar_on_20_puzzles(goal, puzzles):
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
            # print("\nPuzzle " + str(idx) + ":\n")
            # Test A* using all heuristics
            start = puzzle

            start_state = PuzzleState(start, 0)
            goal_state = PuzzleState(goal, 0)
            # print("start:", start_state)
            # print("goal:", goal_state)
            solution_path, search_path, elapsed = PuzzleState.a_star(start_state, goal_state, heuristic)

            output_to_files("A_Star", idx, search_path, solution_path, elapsed, heuristic=heuristic.__name__)

            if elapsed > 60.0:
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

                # for index, state in enumerate(search_path):
                #     print(state, state.level)
                # print("Time taken: " + str(elapsed))

        print(f"\nA* {heuristic.__name__} data")
        if length_solution:
            total_length_sol = sum(length_solution)
            print(f"Average length of solution path: {total_length_sol / len(length_solution)}")
            print(f"Total length of solution path: {total_length_sol}")
            total_length_search = sum(length_search)
            print(f"Average length of search path: {total_length_search / len(length_search)}")
            print(f"Total length of solution path: {total_length_search}")
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


def test_dfs_on_20_puzzles(goal, puzzles):
    print("----------------------------")
    print("DEPTH-FIRST SEARCH ALGORITHM")
    print("----------------------------")

    length_solution = []
    length_search = []
    nb_no_solution = 0
    execution_time = []

    for idx, puzzle in enumerate(puzzles, 1):
        # print("\nPuzzle " + str(idx) + ":\n")
        # Depth-First Search
        start = puzzle

        start_state = PuzzleState(start, 0)
        goal_state = PuzzleState(goal, 0)
        # print("start:", start_state)
        # print("goal:", goal_state)

        dfs_solution_path, dfs_search_path, elapsed = PuzzleState.depth_first_search(start_state, goal_state)
        
        output_to_files("DFS", idx, dfs_search_path, dfs_solution_path, elapsed)

        if elapsed > 60:
            nb_no_solution += 1
            print("no solution")
        else:
            length_search.append(len(dfs_search_path))
            length_solution.append(len(dfs_solution_path))
            execution_time.append(elapsed)

            # print("search path:")
            # for index, state in enumerate(dfs_search_path):
            #     print(state, state.level)
            # print("solution path:")
            # print_solution_path(dfs_solution_path)
            # print("Time taken: " + str(elapsed))

    print(f"DFS data")
    if length_solution:
        total_length_sol = sum(length_solution)
        total_length_search = sum(length_search)

        print(f"Average length of solution path: {total_length_sol / len(length_solution)}")
        print(f"Total length of solution path: {total_length_sol}")

        print(f"Average length of search path: {total_length_search / len(length_search)}")
        print(f"Total length of solution path: {total_length_search}")

        print(f"Average cost of solution path: {total_length_sol / len(length_solution)}")
        print(f"Total cost of solution path: {total_length_sol}")

        print(f"Average cost of search path: {total_length_search / len(length_search)}")
        print(f"Total cost of search path: {total_length_search}")

        total_exec_time = sum(execution_time)
        print(f"Average execution time: {total_exec_time / len(execution_time)}")
        print(f"Total execution time: {total_exec_time}")

    print(f"Total number of no solution: {nb_no_solution}\n")


def test_iter_deepening_on_20_puzzles(goal, puzzles, max_depth):
    print("-----------------------------")
    print("ITERATIVE DEEPENING ALGORITHM")
    print("-----------------------------")

    length_solution = []
    length_search = []
    nb_no_solution = 0
    execution_time = []

    for idx, puzzle in enumerate(puzzles, 1):
        # print("\nPuzzle " + str(idx) + ":\n")
        # Iterative Deepening
        start = puzzle

        start_state = PuzzleState(start, 0)
        goal_state = PuzzleState(goal, 0)
        # print("start:", start_state)
        # print("goal:", goal_state)

        iter_solution_path, iter_search_path, elapsed = PuzzleState.iterative_deepening(start_state, goal_state, max_depth)

        output_to_files("Iter_Deepening", idx, iter_search_path, iter_solution_path, elapsed)

        if elapsed > 60:
            nb_no_solution += 1
            print("no solution")
        else:
            length_search.append(len(iter_search_path))
            length_solution.append(len(iter_solution_path))
            execution_time.append(elapsed)

            # print("search path:")
            # for index, state in enumerate(iter_search_path):
            #     print(state, state.level)
            # print("solution path:")
            # print_solution_path(iter_solution_path)
            # print("Time taken: " + str(elapsed))

    print(f"Iterative Deepening data")
    if length_solution:
        total_length_sol = sum(length_solution)
        total_length_search = sum(length_search)

        print(f"Average length of solution path: {total_length_sol / len(length_solution)}")
        print(f"Total length of solution path: {total_length_sol}")

        print(f"Average length of search path: {total_length_search / len(length_search)}")
        print(f"Total length of solution path: {total_length_search}")

        print(f"Average cost of solution path: {total_length_sol / len(length_solution)}")
        print(f"Total cost of solution path: {total_length_sol}")

        print(f"Average cost of search path: {total_length_search / len(length_search)}")
        print(f"Total cost of search path: {total_length_search}")

        total_exec_time = sum(execution_time)
        print(f"Average execution time: {total_exec_time / len(execution_time)}")
        print(f"Total execution time: {total_exec_time}")

    print(f"Total number of no solution: {nb_no_solution}\n")


if __name__ == '__main__':
    main()
