
class PuzzleState():
    """Represents a puzzle state"""

    def __init__(self, state):
        self._state = state
        self._size = len(state)
        self._set_positions()

    @property
    def state(self):
        return self._state

    @property
    def size(self):
        return self._size

    @property
    def positions(self):
        return self._positions

    @state.setter
    def state(self, state):
        self._state = state

    def get_position(self, value):
        return self._positions.get(value)

    def _set_positions(self):
        positions = {}
        for row_index, row in enumerate(self._state):
            if len(row) != self.size:
                raise AssertionError("Puzzle is not square. Must be a n-by-n puzzle.")
            for val_index, val in enumerate(row):
                positions[val] = (row_index, val_index)
        self._positions = positions

    @staticmethod
    def hamming_distance(state, goal_state):
        distance = 0
        state_tuple = state.state
        goal_state_tuple = goal_state.state

        for row_index, row in enumerate(state_tuple):
            for val_index, val in enumerate(row):
                if (state_tuple[row_index][val_index] != goal_state_tuple[row_index][val_index]):
                    distance += 1

        return distance

    @staticmethod
    def manhattan_distance(state, goal_state):
        distance = 0

        for value, position in state.positions.items():
            row_distance = abs(position[0] - goal_state.get_position(value)[0])
            col_distance = abs(position[1] - goal_state.get_position(value)[1])
            distance += row_distance + col_distance

        return distance

# Tests
state = PuzzleState(((1, 2, 3), (4, 5, 6), (7, 8, 9)))
goal = PuzzleState(((2, 1, 3), (9, 6, 4), (7, 8, 5)))
print(PuzzleState.hamming_distance(state, goal))
print(PuzzleState.manhattan_distance(state, goal))

state = PuzzleState(((1, 2), (3, 4)))
goal = PuzzleState(((4, 3), (1, 2)))
print(PuzzleState.hamming_distance(state, goal))
print(PuzzleState.manhattan_distance(state, goal))
