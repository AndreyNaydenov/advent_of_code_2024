import sys
import re
import time
import numpy as np
import operator
from copy import deepcopy
from functools import reduce
from tqdm import tqdm

def parse():
    data = []
    regex = re.compile("-?\\d+")
    for line in sys.stdin:
        values = [int(d) for d in regex.findall(line)]
        # print(values)
        # (y, x)
        p = np.array((values[1], values[0]))
        v = np.array((values[3], values[2]))
        data.append((p, v))
    return data

def grid_to_string(grid):
    lines = []
    for row in grid:
        els = []
        for el in row:
            if el == 0: els.append(" ")
            else: els.append("^")
        line = "".join(els)
        lines.append(line)
    return "\n".join(lines)

def print_grid(grid):
    print("-"*grid.shape[1])
    print(grid_to_string(grid))
    print("-"*grid.shape[1])

def emulate_robot(field_shape, robot, seconds):
    max_y, max_x = field_shape
    p, v = robot
    new_pos = p + v * seconds
    new_y = ((new_pos[0] % max_y) + max_y) % max_y
    new_x = ((new_pos[1] % max_x) + max_x) % max_x
    robot[0][0] = new_y
    robot[0][1] = new_x
    return robot

def move_robot(field_shape, robot):
    return emulate_robot(field_shape, robot, 1)

def place_positions_on_grid(field_shape, positions, count=True):
    max_y, max_x = field_shape
    grid = np.zeros(field_shape)
    for y in range(max_y):
        for x in range(max_x):
            if (y, x) in positions:
                if count:
                    grid[y, x] = positions.count((y, x))
                else:
                    grid[y, x] = 1
    return grid

def place_robots_on_grid(field_shape, robots, count=True):
    positions = [tuple(r[0]) for r in robots]
    return place_positions_on_grid(field_shape, positions, count=count)

def part1(data, shape):
    time = 100 #seconds
    finish_positions = []
    
    print(place_robots_on_grid(shape, data))

    # each robot can be automatically counted,
    for robot in data:
        emulate_robot(shape, robot, time)
        pos = tuple(robot[0])
        finish_positions.append(pos)

    grid = place_positions_on_grid(shape, finish_positions)
    v_mid = shape[0] // 2
    h_mid = shape[1] // 2
    subgrids = (
        grid[0:v_mid,0:h_mid],
        grid[v_mid+1:,0:h_mid],
        grid[0:v_mid,h_mid+1:],
        grid[v_mid+1:,h_mid+1:],
    )
    # sum and multiply subgrids
    res = reduce(operator.mul, (grid.sum() for grid in subgrids))
    return int(res)

def in_bounds(data, coord):
    il, jl = data.shape
    if coord[0] < 0 or coord[0] >= il: return False
    if coord[1] < 0 or coord[1] >= jl: return False
    return True

def get_adjacent_coords(data, coord, all_coords=False):
    adjacent = (
        (coord[0] - 1, coord[1]),
        (coord[0] + 1, coord[1]),
        (coord[0], coord[1] - 1),
        (coord[0], coord[1] + 1)
    )
    return [c for c in adjacent if in_bounds(data, c) or all_coords ]

def find_region(data, current_coord):
    coords_checked = set()
    region = set()
    value = bool(data[*current_coord])
    next_cells_to_check = [current_coord]
    while next_cells_to_check:
        coord = next_cells_to_check.pop(0)
        if coord in coords_checked:
            #already was on that cell, skip
            continue
        coords_checked.add(coord)
        current_value = bool(data[*coord])
        if current_value == value:
            region.add(coord)
        else:
            continue
        for cell in get_adjacent_coords(data, coord):
            next_cells_to_check.append(cell)
    # print(f"Found region {letter}, size {len(region)}, {region}")
    return region

def is_part_of_some_region(regions, coord):
    for region in regions:
        if coord in region:
            return True
    return False

def get_regions(data):
    regions = []
    il, jl = data.shape
    for i in range(il):
        for j in range(jl):
            current_coord = (i, j)
            if data[*current_coord] == 0:
                # print("skipping 0")
                continue
            # check that current coord is not part of found region
            if is_part_of_some_region(regions, current_coord):
                continue
            region = find_region(data, current_coord)
            regions.append(region)
    return regions

def part2(data, shape):
    max_time = 10000 #seconds

    for step in tqdm(range(max_time)):
        for robot in data:
            move_robot(shape, robot)

        cur_grid = place_robots_on_grid(shape, data, count=False)

        if "^^^^^^^^^^" in grid_to_string(cur_grid):
            print_grid(cur_grid)
            return step + 1

def main():
    #parse stdin
    data = parse()
    # shape = (7, 11) #(y, x)
    shape = (103, 101)
    
    #PART1
    part1_data = deepcopy(data)
    result1 = part1(part1_data, shape)
    print(f"Part1: {result1}")
    
    #PART2
    part2_data = deepcopy(data)
    result2 = part2(part2_data, shape)
    print(f"Part2: {result2}")

main()
