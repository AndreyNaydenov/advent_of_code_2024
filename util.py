import numpy as np

def print_grid(grid):
    # print 2d numpy array
    for line in grid:
        print("".join(line))

def get_pos(grid, value):
    # returns first found element
    return np.argwhere(grid == value)[0]
    
def in_bounds(grid, pos):
    # check if pos coords in bounds of the 2d grid
    il, jl = grid.shape
    if pos[0] < 0 or pos[0] >= il: return False
    if pos[1] < 0 or pos[1] >= jl: return False
    return True

def get_adjacent_coords(grid, pos, all_coords=False, include_direction=False):
    # get coords of adjacent 4 cells
    # if all_coords, include adjacent cells that are out of bounds
    adjacent = (
        (np.array((pos[0] - 1, pos[1])),"^"),
        (np.array((pos[0] + 1, pos[1])),"v"),
        (np.array((pos[0], pos[1] - 1)),"<"),
        (np.array((pos[0], pos[1] + 1)),">")
    )
    adjacent = [c for c in adjacent if in_bounds(grid, c[0]) or all_coords ]
    if not include_direction:
        adjacent = [c[0] for c in adjacent]
    return adjacent
