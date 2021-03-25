from copy import deepcopy
import time

class PuzzleState:
    """Represents a puzzle state"""

    def __init__(self, state, level=0, parent=None):
        self.state = state
        self._size = len(state)
        self._parent = parent
        self._level = level
        self._set_positions()

    def __str__(self):
        return str(self._state)

    def __eq__(self, other_state):
        return self.state == other_state.state

    def __hash__(self):
        return hash(('state', list(self.state)))

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
        h_value = heuristic_func(self, goal_state)
        self._f_value = (h_value + self.level, h_value)

    def get_position(self, value):
        return self._positions.get(value)

    def get_value(self, position):
        if self.is_legal_position(position):
            return self.state[position[0]][position[1]]
        return None

    def is_legal_position(self, position):
        return 0 <= position[0] < self._size and 0 <= position[1] < self._size

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
        PuzzleState.hamming_distance.monotonic = False
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
        PuzzleState.manhattan_distance.monotonic = True
        distance = 0
        for value, position in state.positions.items():
            row_distance = abs(position[0] - goal_state.get_position(value)[0])
            col_distance = abs(position[1] - goal_state.get_position(value)[1])
            distance += row_distance + col_distance
        return distance

    @staticmethod
    def sum_permutation(state, goal_state):
        PuzzleState.sum_permutation.monotonic = False
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
        highest_value = goal_state.size**2-1

        start_time = time.time()
        elapsed = 0.0

        def compare_and_replace_state_in_list(state, state_list):
            old_state_index = state_list.index(state)
            old_state = state_list[old_state_index]
            old_state_f_value = old_state.get_f_value()
            state_f_value = state.get_f_value()
            if old_state_f_value > state_f_value:
                state_list[old_state_index] = state

        while PuzzleState.hamming_distance(current_state, goal_state) != 0 and len(open_list) != 0:
            elapsed = time.time() - start_time
            current_state = open_list[0]

            if elapsed > 60.0:
                return None, None, elapsed

            if current_state in closed_list:
                if hasattr(heuristic_func, 'monotonic') and not heuristic_func.monotonic:
                    compare_and_replace_state_in_list(current_state, closed_list)
                del open_list[0]
                continue

            for start in range(1, highest_value):
                next_best_states = current_state.get_next_states(start)
                for state in next_best_states:
                    state.set_f_value(heuristic_func, goal_state)
                    if state not in open_list:
                        open_list.append(state)
                    else:
                        compare_and_replace_state_in_list(state, open_list)

            closed_list.append(current_state)
            open_list.sort(key=lambda x: x.get_f_value())

        if len(open_list) == 0:
            return [], closed_list, elapsed
        elif len(open_list) == 1:
            return open_list, closed_list, elapsed

        # Backtrack last state's ancestor to get path
        last_state = closed_list[-1]
        path_list = [last_state]
        
        parent = last_state._parent
        while parent is not None:
            path_list.append(parent)
            parent = parent._parent
        path_list.reverse()

        return path_list, closed_list, elapsed

    @staticmethod
    def depth_first_search(start, goal, max_iter=-1):
        open_list = []
        closed_list = []
        open_list.append(start)

        start_time = time.time()
        elapsed = 0.0
        while open_list:
            elapsed = time.time() - start_time
            if elapsed > 60.0:
                return None, None, elapsed

            current_state = open_list.pop()
            closed_list.append(current_state)
            if current_state == goal:
                solution_path = [current_state]
                parent = current_state._parent
                while parent:
                    solution_path.append(parent)
                    parent = parent._parent
                solution_path.reverse()
                return solution_path, closed_list, elapsed
            else:
                if max_iter == -1 or current_state._level < max_iter:
                    state_children = ([current_state.get_next_states(i)[j]
                                       for i in range(1, (start.size ** 2) + 1)
                                       for j in range(len(current_state.get_next_states(i)))
                                       ])
                    for children in state_children:
                        if children not in open_list and children not in closed_list:
                            open_list.append(children)
        return None, closed_list, elapsed

    @staticmethod
    def iterative_deepening(start, goal, max_depth):
        search_path = []
        start_time = time.time()
        elapsed = 0.0

        for i in range(max_depth + 1):
            # time.sleep(0.1)  # Demonstrates that Iterative Deepening really is just fast and doesn't take 0.0 seconds
            elapsed = time.time() - start_time
            if elapsed > 60.0:
                return None, None, elapsed

            solution_path, search_path, _ = PuzzleState.depth_first_search(start, goal, i)
            if solution_path:
                return solution_path, search_path, elapsed
        return None, search_path, elapsed
