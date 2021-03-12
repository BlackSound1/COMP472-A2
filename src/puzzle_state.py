from copy  import deepcopy


class PuzzleState():
    """Represents a puzzle state"""

    def __init__(self, state):
        self.state = state
        self._size = len(state)
        self._set_positions()

    def __str__(self):
        return str(self._state)

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
        state_as_list = []
        for row in state:
            state_as_list.append(list(row))
        self._state = state_as_list

    def get_position(self, value):
        return self._positions.get(value)

    def get_value(self, position):
        if self.is_legal_position(position):
            return self.state[position[0]][position[1]]
        return None

    def is_legal_position(self, position):
        return position[0] >= 0 and position[0] < self._size and position[1] >= 0 and position[1] < self._size

    def switch_positions(self, start_position, end_position):
        start_value = self.get_value(start_position)
        end_value = self.get_value(end_position)
        
        new_state = deepcopy(self._state)
        new_state[start_position[0]][start_position[1]] = end_value
        new_state[end_position[0]][end_position[1]] = start_value

        return PuzzleState(new_state)

    def get_next_states(self, start_value):
        position = self.get_position(start_value)
        if not position:
            return [] 
        moved_up = (position[0] - 1, position[1])
        moved_down = (position[0] + 1, position[1])
        moved_right = (position[0], position[1] + 1)
        moved_left = (position[0], position[1] - 1)

        possible_next_positions = [moved_up, moved_right, moved_down, moved_left]
        next_positions = [self.switch_positions(position, pos) for pos in possible_next_positions if self.is_legal_position(pos)]

        return next_positions

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
