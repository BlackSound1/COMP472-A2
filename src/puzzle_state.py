from copy import deepcopy
import time
import heapq


class PuzzleState:
    """Represents a puzzle state"""

    def __init__(self, state, level=0, parent=None):
        self.state = state
        self._size = len(state)
        self._parent = parent
        self._level = level
        self._f_value = 0
        self._set_positions()

    def __str__(self):
        return str(self._state)

    def __eq__(self, other_state):
        return self.state == other_state.state

    def __lt__(self, other_state):
        return self._f_value < other_state._f_value

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
    def state(self, state: tuple) -> None:
        """ Directly manipulates the state, because _state is a private variable

        :param state: The state
        :return: The state as a list
        """
        state_as_list = []
        for row in state:
            state_as_list.append(list(row))
        self._state = state_as_list

    def get_f_value(self) -> int:
        """ Gets the f value

        :return: The f value
        """
        return self._f_value

    def set_f_value(self, heuristic_func, goal_state: tuple) -> None:
        """ Sets the f value based on the given given goal state and the given heuristic function

        :param heuristic_func: The heuristic function to call
        :param goal_state: The goal state
        :return: None
        """
        h_value = heuristic_func(self, goal_state)
        self._f_value = (h_value + self.level, h_value)

    def get_position(self, value: int) -> tuple:
        """ Gets the position of the given value

        :param value: The value to find the position of
        :return: The position of the value
        """
        return self._positions.get(value)

    def get_value(self, position: tuple):
        """ Gets the value of a given position

        :param position: The position to evaluate
        :return: The value of the state
        """
        if self.is_legal_position(position):
            return self.state[position[0]][position[1]]
        return None

    def is_legal_position(self, position: tuple) -> bool:
        """ Checks whether a given position is valid or not

        :param position: The tuple containing the given position to check
        :return: True or False
        """
        return 0 <= position[0] < self._size and 0 <= position[1] < self._size

    def get_next_states(self, start_value: int) -> list:
        """ Gets all possible states that can be derived directly from the current state of the puzzle

        :param start_value: THe start value
        :return: The list of all next states
        """
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

    def _switch_positions(self, start_position: tuple, end_position: tuple):
        """ Switches 2 tiles

        :param start_position: The first tile position
        :param end_position: The second tile position
        :return: A new PuzzleState with the 2 tiles switched
        """
        start_value = self.get_value(start_position)
        end_value = self.get_value(end_position)

        new_state = deepcopy(self._state)
        new_state[start_position[0]][start_position[1]] = end_value
        new_state[end_position[0]][end_position[1]] = start_value

        return PuzzleState(new_state, self._level + 1, self)

    def _set_positions(self) -> None:
        """ Sets the positions of each tile based on the current state

        :return: None
        """
        positions = {}
        for row_index, row in enumerate(self._state):
            if len(row) != self.size:
                raise AssertionError("Puzzle is not square. Must be a n-by-n puzzle.")
            for val_index, val in enumerate(row):
                positions[val] = (row_index, val_index)
        self._positions = positions

    @staticmethod
    def hamming_distance(state, goal_state) -> int:
        """ Computes the Hamming distance between a current given state and the goal state

        :param state: The current PuzzleState
        :param goal_state: The goal state
        :return: The Hamming distance
        """
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
    def manhattan_distance(state, goal_state) -> float:
        """ Computes the Manhattan distance between a current given state and the goal state.

        This is a modified version of the typical Manhattan distance which we find to be slightly
        more admissible for this type of puzzle

        :param state: The current PuzzleState
        :param goal_state: The goal state
        :return: The modified Manhattan distance
        """
        PuzzleState.manhattan_distance.monotonic = True
        distance = 0
        for value, position in state.positions.items():
            row_distance = abs(position[0] - goal_state.get_position(value)[0])
            col_distance = abs(position[1] - goal_state.get_position(value)[1])
            distance += row_distance + col_distance
        return distance / 2

    @staticmethod
    def sum_permutation(state, goal_state) -> int:
        """ Computes the sum permutation between a current given state and the goal state.

        :param state: The current PuzzleState
        :param goal_state: The goal state
        :return: The sum permutation
        """
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
    def a_star(start_state, goal_state, heuristic_func, time_limit=60) -> tuple:
        """ Performs the A* algorithm.

        :param time_limit: The time limit
        :param start_state: The Starting PuzzleState
        :param goal_state: The goal state
        :param heuristic_func: The heuristic function to use for the algorithm
        :return: The open list, the closed list, and the elapsed time of the algorithm, all as a tuple.
        """

        current_state = start_state
        current_state.set_f_value(heuristic_func, goal_state)
        open_list = [start_state]
        heapq.heapify(open_list)
        closed_list = []
        highest_value = goal_state.size**2 - 1

        start_time = time.time()
        elapsed = 0.0

        def compare_and_replace_state_in_heap(state, state_heap) -> None:
            """ Replaces the current PuzzleState with one that already exists in
            the given list, if this current PuzzleState has a lower f value

            :param state_heap: The heap of states to check against
            :param state: The given PuzzleState
            :return: None
            """
            if has_smaller_f_in_list(state, state_heap):
                old_state_index = state_heap.index(state)
                state_heap[old_state_index] = state
                heapq.heapify(state_heap)

        def has_smaller_f_in_list(state, state_list) -> bool:
            """ Checks if there exists a smaller value for f in the given list

            :param state: The given PuzzleState
            :param state_list: The list to check against
            :return: True or False
            """
            old_state_index = state_list.index(state)
            old_state = state_list[old_state_index]
            old_state_f_value = old_state.get_f_value()
            state_f_value = state.get_f_value()
            if old_state_f_value > state_f_value:
                return True
            return False

        while current_state != goal_state and len(open_list) != 0:
            elapsed = time.time() - start_time
            current_state = heapq.heappop(open_list)

            if elapsed > time_limit:
                return None, None, elapsed

            for start in range(1, highest_value + 1):
                next_best_states = current_state.get_next_states(start)
                for state in next_best_states:
                    state.set_f_value(heuristic_func, goal_state)
                    if state in closed_list:
                        if (hasattr(heuristic_func, 'monotonic') and 
                                not heuristic_func.monotonic and 
                                has_smaller_f_in_list(state, closed_list)):
                            heapq.heappush(open_list, state)
                    elif state in open_list:
                        compare_and_replace_state_in_heap(state, open_list)
                    else:
                        heapq.heappush(open_list, state)

            closed_list.append(current_state)

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
    def depth_first_search(start, goal, max_iter: int = -1, time_limit=60) -> tuple:
        """ Performs the Depth First Search algorithm

        :param time_limit: The time limit
        :param start: The starting PuzzleState
        :param goal: The goal state
        :param max_iter: the maximum number of iteration to perform. Default is -1.
        :return: The open list, the closed list, and the elapsed time of the algorithm, all as a tuple.
        """
        open_list = []
        closed_list = []
        open_list.append(start)

        start_time = time.time()
        elapsed = 0.0
        while open_list:
            elapsed = time.time() - start_time
            if elapsed > time_limit:
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
    def iterative_deepening(start, goal, max_depth: int, time_limit=60) -> tuple:
        """ Performs the Depth First Search algorithm, this time with iterative deepening

        :param time_limit: The time limit
        :param start: The starting PuzzleState
        :param goal: The goal state
        :param max_depth: The maximum depth to search to
        :return: The open list, the closed list, and the elapsed time of the algorithm, all as a tuple.
        """
        search_path = []
        start_time = time.time()
        elapsed = 0.0

        for i in range(max_depth + 1):
            # time.sleep(0.1)  # Demonstrates that Iterative Deepening really is just fast and doesn't take 0.0 seconds
            elapsed = time.time() - start_time
            if elapsed > time_limit:
                return None, None, elapsed

            solution_path, search_path, _ = PuzzleState.depth_first_search(start, goal, i, time_limit)
            if solution_path:
                return solution_path, search_path, elapsed
        return None, search_path, elapsed
