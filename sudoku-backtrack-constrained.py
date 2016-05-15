import sys
from copy import deepcopy


# ==================================================================
# Maps a coordinate into one of the 9 boxes
# ==================================================================
def determine_box(row, col):
    if row / 3 < 1:
        if col / 3 < 1:
            return 0
        elif col / 3 < 2:
            return 1
        else:
            return 2
    elif row / 3 < 2:
        if col / 3 < 1:
            return 3
        elif col / 3 < 2:
            return 4
        else:
            return 5
    else:
        if col / 3 < 1:
            return 6
        elif col / 3 < 2:
            return 7
        else:
            return 8


# ==================================================================
# Creates 3 lists of 9 sets, for each row, column, box.
# Iterates through the open vars, finds the coordinate most constrained
# and returns it.
# ==================================================================
def determine_next_open_var(grid):
    all_nums = set('123456789')
    rows = []
    cols = []
    boxs = []

    for i in range(0, len(grid)):
        rows.append(set())
        for j in range(0, len(grid[i])):
            if i == 0:
                cols.append(set())
                boxs.append(set())
            val = grid[i][j]
            if val != ' ':
                cols[j].add(val)
                rows[i].add(val)
                boxs[determine_box(i, j)].add(val)

    next_vals = None
    next_square = None
    vals = set()
    for i in range(0, len(grid)):
        for j in range(0, len(grid[i])):
            vals.clear()
            if grid[i][j] == ' ':
                # what can't sets do?
                vals = vals.union(rows[i])
                vals = vals.union(cols[j])
                vals = vals.union(boxs[determine_box(i, j)])
                possible_vals = all_nums.difference(vals)

                if len(possible_vals) > 0 and (next_vals is None or len(possible_vals) < len(next_vals)):
                    # if this square has less constraints than the previous one, save it
                    next_vals = possible_vals
                    next_square = (i, j)
    return Node(next_square, next_vals, deepcopy(grid))


# ==================================================================
# Determines if a grid is a goal state
# ==================================================================
def is_goal(grid):
    all_nums = set('123456789')
    rows = []
    cols = []
    boxs = []

    for i in range(0, len(grid)):
        rows.append(set())
        for j in range(0, len(grid[i])):
            if i == 0:
                cols.append(set())
                boxs.append(set())
            val = grid[i][j]
            if val != ' ':
                cols[j].add(val)
                rows[i].add(val)
                boxs[determine_box(i, j)].add(val)

    rt = True
    for i in range(0, len(grid)):
        if len(all_nums.intersection(rows[i])) != 9 or len(all_nums.intersection(cols[i])) != 9 or len(
                all_nums.intersection(boxs[i])) != 9:
            rt = False
    return rt


# ==================================================================
# Pretty Printer for grids
# ==================================================================
def pretty_printer(grid):
    for i in range(0, len(grid)):
        for j in range(0, len(grid[i])):
            print(grid[i][j], end="")
            if (j + 1) % 3 == 0 and j < 7:
                print('|', end="")
        print()
        if (i + 1) % 3 == 0 and i < 7:
            print('-----------')


# ==================================================================
# Recursive Backtracking Search Function
# ==================================================================
def backtrack(node, accumulator):
    if is_goal(node.grid):
        accumulator.num_solutions = accumulator.num_solutions + 1
        accumulator.solutions.append(node.grid)
        return node

    next = determine_next_open_var(node.grid)

    if next.vals is None:
        # there are no solutions down this way
        return None

    # try out each of the possible values for this square
    for num in next.vals:
        (y, x) = next.square
        next.grid[y][x] = num
        result = backtrack(next, accumulator)
    # if result is not None:    #Commented out now that we're accumulating all solutions
    #       return result

    return None


# ==================================================================
# Node class representing... a Node
# ==================================================================
class Node():
    def __init__(self, square, vals, grid):
        self.square = square  # square we picked to set a number, tuple (y, x)
        self.vals = vals  # possible values left for this row
        self.grid = grid


# ==================================================================
# Class to hold solutions
# ==================================================================
class Accumulator():
    def __init__(self):
        self.num_solutions = 0
        self.solutions = []


# ==================================================================
# ==================================================================
#
# Program Beginning
#
# ==================================================================
# ==================================================================
# filename = "easy1.txt"
# filename = sys.argv[1]

filename = 'problems/easy1.txt'

file = open(filename)

grid = []

for line in file:
    row = []
    for char in line:
        if char != '\n':
            row.append(char if char != '.' else ' ')
    grid.append(row)

first = Node((0, 0), set(), grid)

accumulator = Accumulator()

# recursive search
backtrack(first, accumulator)

print("There were " + str(accumulator.num_solutions) + " solutions found")
idx = 0
for sol in accumulator.solutions:
    idx += 1
    print("=====================")
    print("Solution #" + str(idx))
    print()
    pretty_printer(sol)

