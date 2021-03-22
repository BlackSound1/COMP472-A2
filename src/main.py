from puzzle_state import *
from functions import *


def main():
    create_20_random_puzzles(2)

    goal_state = read_state(get_goal_state())

    puzzles = get_all_puzzles()

    test_Astar_on_20_puzzles(goal_state, puzzles)
    test_dfs_on_20_puzzles(goal_state, puzzles)
    test_iter_deepening_on_20_puzzles(goal_state, puzzles, 100)

    # Tests
    # state = PuzzleState(((1, 2, 3), (4, 5, 6), (7, 8, 9)))
    # goal = PuzzleState(((2, 1, 3), (9, 6, 4), (7, 8, 5)))
    # assert PuzzleState.hamming_distance(state, goal) == 6
    # assert PuzzleState.manhattan_distance(state, goal) == 10
    # assert PuzzleState.sum_permutation(state, goal) == 10
    #
    # state = PuzzleState(((1, 2), (3, 4)))
    # goal = PuzzleState(((4, 3), (1, 2)))
    # assert PuzzleState.hamming_distance(state, goal) == 4
    # assert PuzzleState.manhattan_distance(state, goal) == 6
    # assert PuzzleState.sum_permutation(state, goal) == 5
    #
    # # Test A* using all heuristics
    # start_state = create_random_puzzle(3)
    # goal_state = create_random_puzzle(3)
    # heuristics = [PuzzleState.sum_permutation, PuzzleState.hamming_distance, PuzzleState.manhattan_distance]
    # print("start:", start_state)
    # print("goal:", goal_state)
    #
    # for heuristic in heuristics:
    #     print(heuristic.__name__, "path")
    #     search_list = PuzzleState.a_star(start_state, goal_state, heuristic)
    #
    #     for index, state in enumerate(search_list):
    #         print(state, state.level)


def test_Astar_on_20_puzzles(goal, puzzles):
    print("------------")
    print("A* ALGORITHM")
    print("------------")

    for idx, puzzle in enumerate(puzzles, 0):
        print("\nPuzzle " + str(idx + 1) + ":\n")
        # Test A* using Manhattan distance as heuristic
        start = read_state(puzzle)

        start_state = PuzzleState(start, 0)
        goal_state = PuzzleState(goal, 0)
        heuristics = [PuzzleState.sum_permutation, PuzzleState.hamming_distance, PuzzleState.manhattan_distance]
        print("start:", start_state)
        print("goal:", goal_state)

        for heuristic in heuristics:
            print(heuristic.__name__, "path")
            search_list = PuzzleState.a_star(start_state, goal_state, heuristic)

            for index, state in enumerate(search_list):
                print(state, state.level)


def test_dfs_on_20_puzzles(goal, puzzles):
    print("------------")
    print("DEPTH-FIRST SEARCH ALGORITHM")
    print("------------")

    for idx, puzzle in enumerate(puzzles, 0):
        print("\nPuzzle " + str(idx + 1) + ":\n")
        # Depth-First Search
        start = read_state(puzzle)

        start_state = PuzzleState(start, 0)
        goal_state = PuzzleState(goal, 0)
        print("start:", start_state)
        print("goal:", goal_state)

        dfs_solution_path, dfs_search_path = PuzzleState.depth_first_search(start_state, goal_state)
        print("search path:")
        for index, state in enumerate(dfs_search_path):
            print(state, state.level)
        print("solution path:")
        print_solution_path(dfs_solution_path)


def test_iter_deepening_on_20_puzzles(goal, puzzles, max_depth):
    print("------------")
    print("ITERATIVE DEEPENING ALGORITHM")
    print("------------")

    for idx, puzzle in enumerate(puzzles, 0):
        print("\nPuzzle " + str(idx + 1) + ":\n")
        # Iterative Deepening
        start = read_state(puzzle)

        start_state = PuzzleState(start, 0)
        goal_state = PuzzleState(goal, 0)
        print("start:", start_state)
        print("goal:", goal_state)

        iter_solution_path, iter_search_path = PuzzleState.iterative_deepening(start_state, goal_state, max_depth)
        print("search path:")
        for index, state in enumerate(iter_search_path):
            print(state, state.level)
        print("solution path:")
        print_solution_path(iter_solution_path)


if __name__ == '__main__':
    main()
