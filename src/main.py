
from functions import *


def main():
    create_20_random_puzzles(2)

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

    for idx, puzzle in enumerate(puzzles, 1):
        print("\nPuzzle " + str(idx) + ":\n")
        # Test A* using all heuristics
        start = puzzle

        start_state = PuzzleState(start, 0)
        goal_state = PuzzleState(goal, 0)
        heuristics = [PuzzleState.sum_permutation, PuzzleState.hamming_distance, PuzzleState.manhattan_distance]
        print("start:", start_state)
        print("goal:", goal_state)

        for heuristic in heuristics:
            print(heuristic.__name__, "path")
            closed_list, search_list = PuzzleState.a_star(start_state, goal_state, heuristic)

            output_to_files("A_Star", idx, search_list, closed_list, heuristic=heuristic.__name__)

            for index, state in enumerate(search_list):
                print(state, state.level)


def test_dfs_on_20_puzzles(goal, puzzles):
    print("----------------------------")
    print("DEPTH-FIRST SEARCH ALGORITHM")
    print("----------------------------")

    for idx, puzzle in enumerate(puzzles, 1):
        print("\nPuzzle " + str(idx) + ":\n")
        # Depth-First Search
        start = puzzle

        start_state = PuzzleState(start, 0)
        goal_state = PuzzleState(goal, 0)
        print("start:", start_state)
        print("goal:", goal_state)

        dfs_solution_path, dfs_search_path = PuzzleState.depth_first_search(start_state, goal_state)
        
        output_to_files("DFS", idx, dfs_search_path, dfs_solution_path)

        print("search path:")
        for index, state in enumerate(dfs_search_path):
            print(state, state.level)
        print("solution path:")
        print_solution_path(dfs_solution_path)


def test_iter_deepening_on_20_puzzles(goal, puzzles, max_depth):
    print("-----------------------------")
    print("ITERATIVE DEEPENING ALGORITHM")
    print("-----------------------------")

    for idx, puzzle in enumerate(puzzles, 1):
        print("\nPuzzle " + str(idx) + ":\n")
        # Iterative Deepening
        start = puzzle

        start_state = PuzzleState(start, 0)
        goal_state = PuzzleState(goal, 0)
        print("start:", start_state)
        print("goal:", goal_state)

        iter_solution_path, iter_search_path = PuzzleState.iterative_deepening(start_state, goal_state, max_depth)

        output_to_files("Iter_Deepening", idx, iter_search_path, iter_solution_path)

        print("search path:")
        for index, state in enumerate(iter_search_path):
            print(state, state.level)
        print("solution path:")
        print_solution_path(iter_solution_path)


if __name__ == '__main__':
    main()
