from puzzle_state import *


def main():
    # Tests
    state = PuzzleState(((1, 2, 3), (4, 5, 6), (7, 8, 9)))
    goal = PuzzleState(((2, 1, 3), (9, 6, 4), (7, 8, 5)))
    print(PuzzleState.hamming_distance(state, goal))
    print(PuzzleState.manhattan_distance(state, goal))

    state = PuzzleState(((1, 2), (3, 4)))
    goal = PuzzleState(((4, 3), (1, 2)))
    print(PuzzleState.hamming_distance(state, goal))
    print(PuzzleState.manhattan_distance(state, goal))


if __name__ == '__main__':
    main()
