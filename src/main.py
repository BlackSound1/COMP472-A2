from puzzle_state import *
from functions import create_random_puzzle


def main():
    # Tests
    state = PuzzleState(((1, 2, 3), (4, 5, 6), (7, 8, 9)), 0)
    goal = PuzzleState(((2, 1, 3), (9, 6, 4), (7, 8, 5)), 0)
    assert PuzzleState.hamming_distance(state, goal) == 6
    assert PuzzleState.manhattan_distance(state, goal) == 10
    assert PuzzleState.sum_permutation(state, goal) == 10

    state = PuzzleState(((1, 2), (3, 4)), 0)
    goal = PuzzleState(((4, 3), (1, 2)), 0)
    assert PuzzleState.hamming_distance(state, goal) == 4
    assert PuzzleState.manhattan_distance(state, goal) == 6
    assert PuzzleState.sum_permutation(state, goal) == 5

    # Test A* using Manhattan distance as heuristic
    # start_state = create_random_puzzle(3)
    # goal_state = create_random_puzzle(3)
    # search_list = PuzzleState.a_star(start_state, goal_state, PuzzleState.manhattan_distance)

    # print("start:", start_state)
    # print("goal:", goal_state)
    # print("path:")
    # for index, state in enumerate(search_list):
    #     print(state, state.level)

    # Depth-First Search
    start_state = create_random_puzzle(2)
    goal_state = PuzzleState(((1, 2), (3, 4)), 0)
    dfs_result, dfs_search_path = PuzzleState.depth_first_search(start_state, goal_state)

    print("start:", start_state)
    print("goal:", goal_state)

    print("search path:")
    for index, state in enumerate(dfs_search_path):
        print(state, state.level)

    print("solution path:")
    if dfs_result:
        temp = dfs_result.parent
        solution_path = [dfs_result]
        while temp:
            solution_path.append(temp)
            temp = temp.parent
        solution_path.reverse()
        for index, state in enumerate(solution_path):
            print(state, state.level)
    else:
        print("no solution")

    # Iterative Deepening
    start_state = create_random_puzzle(2)
    goal_state = PuzzleState(((1, 2), (3, 4)), 0)
    di_result, di_search_path = PuzzleState.deep_iterating(start_state, goal_state, 100)

    print("start:", start_state)
    print("goal:", goal_state)

    print("search path:")
    for index, state in enumerate(di_search_path):
        print(state, state.level)

    print("solution path:")
    if di_result:
        temp = di_result.parent
        solution_path = [di_result]
        while temp:
            solution_path.append(temp)
            temp = temp.parent
        solution_path.reverse()
        for index, state in enumerate(solution_path):
            print(state, state.level)
    else:
        print("no solution")


if __name__ == '__main__':
    main()
