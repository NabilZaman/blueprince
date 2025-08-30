
from enum import Enum
from typing import Self
from collections import namedtuple, deque, defaultdict
from time import time

Position = namedtuple('Position', ['x', 'y'])

class Color(Enum):
    GRAY = 'G'
    WHITE = 'W'
    BLACK = 'B'
    GREEN = 'E'
    RED = 'R'
    VIOLET = 'V'
    YELLOW = 'Y'
    PINK = 'P'
    ORANGE = 'O'
    BLUE = 'U'

# Immutable
class PuzzleState:

    def __init__(self, state: list[list[Color]] = None):
        if state is None:
            state = [([Color.GRAY] * 3) for _ in range(3)]
        self.state: list[list[Color]] = state

    def get_color(self, pos: Position) -> Color:
        return self.state[pos.y][pos.x]

    def set_color(self, pos: Position, color: Color) -> Self:
        new_state = self._internal_state_copy()
        new_state[pos.y][pos.x] = color
        return PuzzleState(new_state)

    def _internal_state_copy(self) -> list[list[Color]]:
        return [row.copy() for row in self.state]

    def copy(self) -> Self:
        return PuzzleState(self._internal_state_copy())

    def _internal_state_tuple(self) -> tuple[tuple[Color]]:
        return tuple(tuple(row) for row in self.state)

    def activate(self, pos: Position) -> Self:
        color = self.get_color(pos)
        action = ColorAction(color)
        return action.activate(pos, self)

    def verify_solution(self, corners: list[Color]):
        if len(corners) != 4:
            raise ValueError("'corners' list must contain exactly 4 colors!")
        top_left = self.get_color(Position(0, 2))
        top_right = self.get_color(Position(2, 2))
        bot_left = self.get_color(Position(0, 0))
        bot_right = self.get_color(Position(2, 0))
        result = (corners[0] == top_left and
                corners[1] == top_right and
                corners[2] == bot_left and
                corners[3] == bot_right)
        # if result:
        #     print(corners, top_left, top_right, bot_left, bot_right)
        return result

    def __str__(self):
        result = ''
        for row in reversed(self.state):
            result += str(row) + '\n'
        return result

    def __hash__(self) -> int:
        return self._internal_state_tuple().__hash__()

    def __eq__(self, other):
        if type(other) != type(self):
            return False
        return self._internal_state_tuple().__eq__(other._internal_state_tuple())

def in_bounds(index: int) -> bool:
    return 0 <= index <= 2

def find_adjacent_cells(pos: Position, include_diagonals: bool = False) -> list[Position]:
    left = Position(pos.x - 1, pos.y)
    right = Position(pos.x + 1, pos.y)
    up = Position(pos.x, pos.y + 1)
    down = Position(pos.x, pos.y - 1)
    top_left = Position(pos.x - 1, pos.y + 1)
    top_right = Position(pos.x + 1, pos.y + 1)
    bot_left = Position(pos.x - 1, pos.y - 1)
    bot_right = Position(pos.x + 1, pos.y - 1)
    if include_diagonals:
        neighbors = [up, top_right, right, bot_right, down, bot_left, left, top_left]
    else:
        neighbors = [up, right, down, left]
    return [ neighbor for neighbor in neighbors
             if in_bounds(neighbor.x) and in_bounds(neighbor.y) ]

def find_diagonal_cells(pos: Position) -> list[Position]:
    top_left = Position(pos.x - 1, pos.y + 1)
    top_right = Position(pos.x + 1, pos.y + 1)
    bot_left = Position(pos.x - 1, pos.y - 1)
    bor_right = Position(pos.x + 1, pos.y - 1)
    return [neighbor for neighbor in [top_left, top_right, bot_left, bor_right]
            if in_bounds(neighbor.x) and in_bounds(neighbor.y)]


def find_row_cells(pos: Position) -> list[Position]:
    return [Position(i, pos.y) for i in range(3)]

def find_opposite_cell(pos: Position) -> Position:
    return Position(abs(pos.x - 2), abs(pos.y - 2))

def find_cell_below(pos: Position) -> Position:
    return Position(pos.x, max(pos.y - 1, 0))

def find_cell_above(pos: Position) -> Position:
    return Position(pos.x, min(pos.y + 1, 2))

class ColorAction:

    def __init__(self, color: Color):
        self.activate = self.get_action_by_color(color)

    @classmethod
    def get_action_by_color(cls, color: Color):
        action_table = {
            Color.GRAY: cls.gray_action,
            Color.WHITE: cls.white_action,
            Color.BLACK: cls.black_action,
            Color.GREEN: cls.green_action,
            Color.RED: cls.red_action,
            Color.VIOLET: cls.violet_action,
            Color.YELLOW: cls.yellow_action,
            Color.PINK: cls.pink_action,
            Color.ORANGE: cls.orange_action,
            Color.BLUE: cls.blue_action
        }
        return action_table[color]

    @staticmethod
    def gray_action(_: Position, state: PuzzleState) -> PuzzleState:
        return state

    @staticmethod
    def white_action(pos: Position, state: PuzzleState) -> PuzzleState:
        my_color = state.get_color(pos)
        neighbors = find_adjacent_cells(pos)
        targets = neighbors + [pos]
        for target in targets:
            target_color = state.get_color(target)
            if target_color == Color.GRAY:
                state = state.set_color(target, my_color)
            elif target_color == my_color:
                state = state.set_color(target, Color.GRAY)
        return state

    @staticmethod
    def black_action(pos: Position, state: PuzzleState) -> PuzzleState:
        row = find_row_cells(pos)
        prev_color = state.get_color(row[-1])
        for i in range(len(row)):
            cur_cell = row[i]
            cur_color = state.get_color(cur_cell)
            state = state.set_color(cur_cell, prev_color)
            prev_color = cur_color
        return state

    @staticmethod
    def green_action(pos: Position, state: PuzzleState) -> PuzzleState:
        my_color = state.get_color(pos)
        opposite = find_opposite_cell(pos)
        state = (state.set_color(pos, state.get_color(opposite))
                 .set_color(opposite, my_color))
        return state

    @staticmethod
    def red_action(pos: Position, state: PuzzleState) -> PuzzleState:
        my_color = state.get_color(pos)
        for x in range(3):
            for y in range(3):
                cur_pos = Position(x, y)
                cur_color = state.get_color(cur_pos)
                if cur_color == Color.BLACK:
                    state = state.set_color(cur_pos, my_color)
                if cur_color == Color.WHITE:
                    state = state.set_color(cur_pos, Color.BLACK)
        return state

    @staticmethod
    def violet_action(pos: Position, state: PuzzleState) -> PuzzleState:
        my_color = state.get_color(pos)
        below = find_cell_below(pos)
        state = (state.set_color(pos, state.get_color(below))
                 .set_color(below, my_color))
        return state

    @staticmethod
    def yellow_action(pos: Position, state: PuzzleState) -> PuzzleState:
        my_color = state.get_color(pos)
        above = find_cell_above(pos)
        state = (state.set_color(pos, state.get_color(above))
                 .set_color(above, my_color))
        return state

    @staticmethod
    def pink_action(pos: Position, state: PuzzleState) -> PuzzleState:
        neighbors = find_adjacent_cells(pos, include_diagonals=True)
        prev_color = state.get_color(neighbors[-1])
        for i in range(len(neighbors)):
            neighbor = neighbors[i]
            neighbor_color = state.get_color(neighbor)
            state = state.set_color(neighbor, prev_color)
            prev_color = neighbor_color

        return state

    @staticmethod
    def orange_action(pos: Position, state: PuzzleState) -> PuzzleState:
        neighbors = find_adjacent_cells(pos)
        color_freq: dict[Color, int] = defaultdict(int)
        for neighbor in neighbors:
            neighbor_color = state.get_color(neighbor)
            color_freq[neighbor_color] += 1
        max_freq = max(color_freq.values())
        max_freq_colors = [color for color in color_freq if color_freq[color] == max_freq]
        if len(max_freq_colors) == 1:
            state = state.set_color(pos, max_freq_colors[0])
        return state

    @classmethod
    def blue_action(cls, pos: Position, state: PuzzleState) -> PuzzleState:
        center_color = state.get_color(Position(1,1))
        if center_color == Color.BLUE:
            return state
        center_action = cls.get_action_by_color(center_color)
        return center_action(pos, state)

class SolutionStep:
    def __init__(self, color: Color, pos: Position):
        self.color = color
        self.pos = pos

    def __str__(self):
        return f'{self.color.name} at ({self.pos.x}, {self.pos.y})'


def solver(puzzle_state: PuzzleState, goal: list[Color]) -> list[SolutionStep] | None:
    start_time = time()
    if len(goal) not in (1, 4):
        raise ValueError("Goals list must either specify 1 or 4 elements")

    if len(goal) == 1:
        goal = goal*4

    paths: dict[PuzzleState, list[SolutionStep]] = {
        puzzle_state: []
    }

    state_queue: deque[PuzzleState] = deque()
    state_queue.append(puzzle_state)

    steps = 0
    while len(state_queue) != 0:
        steps += 1
        # print(len(state_queue))
        cur_state = state_queue.popleft()
        for y in range(len(cur_state.state)):
            for x in range(len(cur_state.state[y])):
                pos = Position(x, y)
                color = cur_state.get_color(pos)
                possible_transition = cur_state.activate(pos)
                if possible_transition not in paths:
                    cur_path = paths[cur_state]
                    new_path = cur_path.copy()
                    new_path.append(SolutionStep(color, pos))
                    # print(possible_transition)
                    # Check if we win
                    if possible_transition.verify_solution(goal):
                        # print("winner?\n", possible_transition)
                        print(f"Searched {steps} possible operations in {time() - start_time:.2f} seconds.")
                        return new_path
                    paths[possible_transition] = new_path
                    state_queue.append(possible_transition)

    # we should only reach this if we failed to find a solution
    print(f"Failed to find a solution after {steps} steps")
    return None

gray = Color.GRAY
white = Color.WHITE
black = Color.BLACK
green = Color.GREEN
red = Color.RED
violet = Color.VIOLET
purple = violet
yellow = Color.YELLOW
pink = Color.PINK
orange = Color.ORANGE
blue = Color.BLUE

def create_puzzle(initial_state: list[list[Color]]) -> PuzzleState:
    if len(initial_state) != 3 or not all(len(sublist) == 3 for sublist in initial_state):
        raise ValueError("The given initial state must be a 3x3 grid of colors!")
    return PuzzleState(
        list(reversed(initial_state))
    )

# puzzle1 = PuzzleState(
#     list(reversed([
#         [gray, green, gray],
#         [orange, black, red],
#         [black, white, violet],
#     ]))
# )
#
# solution = solver(puzzle1, [Color.BLACK, Color.VIOLET, Color.ORANGE, Color.RED])
#
# detailed_solution = False
# if detailed_solution:
#     running_solution = puzzle1
#     step_num = 0
#     for step in solution:
#         running_solution = running_solution.activate(step.pos)
#         print(step_num, '. ', step, ':\n', running_solution, sep='')
#         step_num += 1
# else:
#     for step in solution:
#         print(step)
# a = PuzzleState.activate
# p = Position
# print(puzzle1.activate(p(0,2)).activate(p(0,1)).activate(p(2,0)))
