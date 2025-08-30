
from solver import *

# Step 0: Optionally enable this flag to show intermediate results.
SHOW_DETAIL = False

# Step 1: Define the Goal state
# Either set the `goal_color` variable or the `goal_colors` list
# `goal_colors`, if set, should be defined in the following way:
# Example Box
# c0 ---- c1
#  |       |
# c2 ---- c3
# goal_colors = [ c0, c1, c2, c3 ]
#
goal_color = None
# OR
goal_colors = [white, white, white, white]

# Step 2: Define the initial puzzle configuration
initial_state = [
    [gray, gray, gray],
    [gray, white, gray],
    [gray, gray, gray]
]

# Step 3: Run the solver
if goal_color is not None:
    goal_colors = [goal_color] * 4

puzzle = create_puzzle(initial_state)
solution = solver(puzzle, goal_colors)

if SHOW_DETAIL:
    running_solution = puzzle
    step_num = 0
    for step in solution:
        running_solution = running_solution.activate(step.pos)
        print(step_num, '. ', step, ':\n', running_solution, sep='')
        step_num += 1
else:
    for step in solution:
        print(step)

# Note: Instructions are given with 0-indexed coordinates with the origin at the bottom-left
# ie.
#
# (0, 2) - (1, 2) - (2, 2)
# (0, 1) - (1, 1) - (2, 1)
# (0, 0) - (1, 0) - (2, 0)
#
