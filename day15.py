import sys
import numpy as np

def parse():
    grid = []
    instructions = []
    sections = "".join(sys.stdin.readlines()).strip().split("\n\n")
    for line in sections[0].split("\n"):
        cells = list(line.strip())
        grid.append(cells)
    for line in sections[1].split("\n"):
        for el in line:
            instructions.append(el)
    return (grid, instructions)

def print_grid(grid):
    for line in grid:
        print("".join(line))

def get_part2_grid(grid):
    new = []
    for line in grid:
        new_line = []
        for el in line:
            if el == "#": new_line.extend(("#", "#"))
            if el == ".": new_line.extend((".", "."))
            if el == "O": new_line.extend(("[", "]"))
            if el == "@": new_line.extend(("@", "."))
        new.append(new_line)
    return np.array(new)

def find_robot(grid):
    return np.argwhere(grid == "@")[0]

def run_instruction(grid, instruction, robot_pos):
    jmax, imax = grid.shape
    jc, ic = robot_pos
    coords_to_check = []
    match instruction:
        case "^":
            coords_to_check = list((x ,ic) for x in range(jc, -1, -1))
        case "v":
            coords_to_check = list((x ,ic) for x in range(jc, jmax))
        case "<":
            coords_to_check = list((jc ,x) for x in range(ic, -1, -1))
        case ">":
            coords_to_check = list((jc ,x) for x in range(ic, imax))

    coords_to_swap = []
    for coord in coords_to_check:
        cell_value = grid[*coord]
        #iterate over cells in front, if we find empty '.' cell, move all cells before +1
        # if not empty cells, do nothing
        if cell_value == "#": return (grid, robot_pos)

        coords_to_swap.append(coord)
        if cell_value == ".": break

    # print("possible, cells to swap:", coords_to_swap)
    new_robot_pos = coords_to_swap[1]
    prev_cell_value = "@"
    grid[*robot_pos] = "."
    for coord in coords_to_swap[1:]:
        save = grid[*coord]
        grid[*coord] = prev_cell_value
        prev_cell_value = save
    return grid, new_robot_pos

def get_next_coord(instruction, coord):
    match instruction:
        case "^": return (coord[0] - 1, coord[1])
        case "v": return (coord[0] + 1, coord[1])
        case "<": return (coord[0], coord[1] - 1)
        case ">": return (coord[0], coord[1] + 1)

def is_move_possible(grid, instruction, pos):
    # returns all cells, that should be moved futher
    cells_to_move = []
    next_pos = get_next_coord(instruction, pos)
    match grid[*next_pos]:
        case ".": return [pos]
        case "#": return
        case "["|"]":
            # run the same algorithm for each box part as for robot (check next cell...)
            second_half_direction = "<" if grid[*next_pos] == "]" else ">"
            second_half_pos = get_next_coord(second_half_direction, next_pos)
            if instruction in (">", "<"):
                cells = is_move_possible(grid, instruction, second_half_pos)
                if cells:
                    return [pos] + [next_pos] + cells
            else:
                cells_current = is_move_possible(grid, instruction, next_pos)
                cells_second_half = is_move_possible(grid, instruction, second_half_pos)
                if cells_current and cells_second_half:
                    cells_to_move.extend(cells_current)
                    cells_to_move.extend(cells_second_half)
                    return [pos] + cells_to_move

def move_if_possible(grid, instruction, pos):
    # print(f"Checking {instruction}")
    cells_to_move = is_move_possible(grid, instruction, pos)
    if not cells_to_move: 
        # print(f"{instruction} Not Possible")
        return (grid, pos)
    # print(f"{instruction} Move Possibe {pos}, {cells_to_move}")
    
    cells_to_move_with_val = []
    # save old values
    for coord in cells_to_move:
        value = grid[*coord]
        cells_to_move_with_val.append((coord, value))
    # clear moved cells
    for coord in cells_to_move:
        grid[*coord] = "."
    # set saved values to next positions
    for coord, value in cells_to_move_with_val:
        next_coord = get_next_coord(instruction, coord)
        grid[*next_coord] = value
        
    return grid, get_next_coord(instruction, pos)

def count_boxes(grid, value="O"):
    positions = np.where(grid == value)
    positions = np.vstack(positions).T
    return sum(j * 100 + i for j, i in positions)

def part1(grid, instructions):
    pos = find_robot(grid)
    for instr in instructions:
         grid, pos = run_instruction(grid, instr, pos)
         # print_grid(grid)
    return count_boxes(grid)
    
def part2(grid, instructions):
    # emulate instructions
    pos = find_robot(grid)
    for instr in instructions:
         grid, pos = move_if_possible(grid, instr, pos)
         # print_grid(grid)
    return count_boxes(grid, value="[")

def main():
    #parse stdin
    data = parse()
    grid = np.array(data[0])
    instructions = data[1]
    # print_grid(grid)
    grid_part2 = get_part2_grid(grid)
    # print_grid(grid_part2)
    
    #PART1
    result1 = part1(grid, instructions)
    print(f"Part1: {result1}")
    
    #PART2
    result2 = part2(grid_part2, instructions)
    print(f"Part2: {result2}")

main()
