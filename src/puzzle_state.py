from copy import deepcopy


class PuzzleState():
    """Represents a puzzle state"""

    def __init__(self, state, level, parent=None):
        self.state = state
        self._size = len(state)
        self._level = level
        self.parent = parent
        self._set_positions()

    def __str__(self):
        return str(self._state)

    def __eq__(self, other_state):
        return self.state == other_state.state

    def __hash__(self):
        return hash(('state', list(self.state)))

    def isIn(self, a):
        for node in a:
            if (self == node):
                return True
        return False

    @property
    def state(self):
        return self._state

    @property
    def size(self):
        return self._size

    @property
    def level(self):
        return self._level

    @property
    def positions(self):
        return self._positions

    @state.setter
    def state(self, state):
        state_as_list = []
        for row in state:
            state_as_list.append(list(row))
        self._state = state_as_list

    def get_f_value(self):
        return self._f_value

    def set_f_value(self, heuristic_func, goal_state):
        self._f_value = 2 * heuristic_func(self, goal_state) + self.level

    def get_position(self, value):
        return self._positions.get(value)

    def get_value(self, position):
        if self.is_legal_position(position):
            return self.state[position[0]][position[1]]
        return None

    def is_legal_position(self, position):
        return position[0] >= 0 and position[0] < self._size and position[1] >= 0 and position[1] < self._size

    def get_next_states(self, start_value):
        position = self.get_position(start_value)
        if not position:
            return []
        moved_up = (position[0] - 1, position[1])
        moved_down = (position[0] + 1, position[1])
        moved_right = (position[0], position[1] + 1)
        moved_left = (position[0], position[1] - 1)

        possible_next_positions = [moved_up, moved_right, moved_down, moved_left]
        next_positions = [self._switch_positions(position, pos) for pos in possible_next_positions if
                          self.is_legal_position(pos)]

        return next_positions

    def _switch_positions(self, start_position, end_position):
        start_value = self.get_value(start_position)
        end_value = self.get_value(end_position)

        new_state = deepcopy(self._state)
        new_state[start_position[0]][start_position[1]] = end_value
        new_state[end_position[0]][end_position[1]] = start_value

        return PuzzleState(new_state, self._level + 1, self)

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
                if state_tuple[row_index][val_index] != goal_state_tuple[row_index][val_index]:
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

    @staticmethod
    def sum_permutation(state, goal_state):
        sum = 0

        for row in goal_state.state:
            for current in row:
                left = []
                is_left = True
                for row in goal_state.state:
                    for value in row:
                        if value == current:
                            is_left = False
                        if is_left and value != current:
                            left.append(value)

                is_right = False
                for row in state.state:
                    for value in row:
                        if is_right and value in left:
                            sum += 1
                        if value == current:
                            is_right = True
        return sum

    @staticmethod
    def a_star(start_state, goal_state, heuristic_func):
        current_state = start_state
        current_state.set_f_value(heuristic_func, goal_state)
        open_list = [start_state]
        closed_list = []

        while PuzzleState.hamming_distance(current_state, goal_state) != 0 and len(open_list) != 0:
            current_state = open_list[0]

            if current_state in closed_list:
                del open_list[0]
                current_state = open_list[0]
                continue

            for start in range(1, 10):
                next_best_states = current_state.get_next_states(start)
                for state in next_best_states:
                    if state not in open_list:
                        state.set_f_value(heuristic_func, goal_state)
                        open_list.append(state)

            closed_list.append(current_state)
            open_list.sort(key=lambda x: x.get_f_value())

        if len(open_list) == 0:
            return []

        # Backtrack to get path
        reversed_search_list = list(reversed(closed_list))
        level = reversed_search_list[0].level
        path_list = [reversed_search_list[0]]
        for state in reversed_search_list:
            if state.level == level - 1 and PuzzleState.manhattan_distance(state, path_list[-1]) == 2:
                level -= 1
                path_list.append(state)

        return path_list

    @staticmethod
    def depth_first_search(start, goal):
        open_list = []
        closed_list = []
        open_list.append(start)

        while open_list:
            X = open_list.pop()
            if X == goal:
                closed_list.append(X)
                return X, closed_list
            else:
                X_children = ([X.get_next_states(i)[j] for i in range(1, (start.size ** 2) + 1) for j in
                               range(len(X.get_next_states(i)))])
                closed_list.append(X)
                for children in X_children:
                    if not children.isIn(open_list) and not children.isIn(closed_list):
                        open_list.append(children)
        return None, closed_list

    @staticmethod
    def deep_iterating(start, goal, max_depth):
        closed_list = []
        for i in range(max_depth):
            open_list = []
            closed_list = []
            result, closed_list = PuzzleState.dfs_limited(open_list, closed_list, start, goal, i)
            if result and result == goal:
                return result, closed_list
        return None, closed_list

    @staticmethod
    def dfs_limited(open_list, closed_list, start, goal, max_iter):
        open_list.append(start)
        k = 1
        while open_list:
            X = open_list.pop()

            if X == goal:
                closed_list.append(X)
                return X, closed_list
            else:
                closed_list.append(X)
                if k <= max_iter:
                    X_children = ([X.get_next_states(i)[j] for i in range(1, (start.size ** 2) + 1) for j in
                                   range(len(X.get_next_states(i)))])
                    k += 1
                    for children in X_children:
                        if not children.isIn(open_list) and not children.isIn(closed_list):
                            open_list.append(children)
        return None, closed_list
