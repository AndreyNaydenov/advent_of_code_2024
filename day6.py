#parse input to matrix
import sys
from enum import Enum
from tqdm import tqdm
import time

class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

#find starting pos
def find_start(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == "^":
                return (i, j)

def is_in_bounds(matrix, current_pos):
    i, j = current_pos
    if i >= len(matrix) or i < 0: return False
    if j >= len(matrix[0]) or j < 0: return False
    return True

def get_next_cell(current_pos, direction):
    i, j = current_pos
    match direction:
        case Direction.UP:
            return (i-1, j)
        case Direction.DOWN:
            return (i+1, j)
        case Direction.LEFT:
            return (i, j-1)
        case Direction.RIGHT:
            return (i, j+1)   

def move(matrix, current_pos, direction: Direction):
    #returns new pos
    def turn_right(direction: Direction):
        return Direction((direction.value + 1) % 4)
        
    def is_next_move_possible(matrix, current_pos, direction):
        next_cell_pos = get_next_cell(current_pos, direction)
        #if we exited matrix - True
        if not is_in_bounds(matrix, next_cell_pos): 
            return True
        #if not exited, check cell contents
        i, j = next_cell_pos
        # print(f"Current cell {current_pos}, next cell {next_cell_pos}:{matrix[i][j]}")
        if matrix[i][j] == "#": return False
        return True
            
    #check what is next in current direction
    if is_next_move_possible(matrix, current_pos, direction):
        # move forward
        new_pos = get_next_cell(current_pos, direction)
    else:
        # turn right and move forward
        while not is_next_move_possible(matrix, current_pos, direction):
            direction = turn_right(direction)
        new_pos = get_next_cell(current_pos, direction)
    return matrix, new_pos, direction

def print_matrix(matrix):
    for line in matrix:
        print("".join(line))

def copy_matrix(matrix):
    new_matrix = []
    for line in matrix:
        new_matrix.append(line.copy())
    return new_matrix

def is_looping(matrix):
    current_pos = find_start(matrix)
    direction = Direction.UP
    while is_in_bounds(matrix, current_pos):
        #mark position
        # print_matrix(matrix)
        i, j = current_pos
        if matrix[i][j] == "X":
            matrix[i][j] = "Y"
        elif matrix[i][j] == "Y":
            matrix[i][j] = "Z"
        elif matrix[i][j] == "Z":
            matrix[i][j] = "A"
        elif matrix[i][j] == "A":
            matrix[i][j] = "B"
        elif matrix[i][j] == "B":
            return True
        else:
            matrix[i][j] = "X"
            # ni, nj = get_next_cell(current_pos, direction)
            # if matrix[ni][nj] == "X":
                # return True
        matrix, current_pos, direction = move(matrix, current_pos, direction)
    return False

def part1(matrix):
    current_pos = find_start(matrix)
    direction = Direction.UP
    while is_in_bounds(matrix, current_pos):
        #mark position
        i, j = current_pos
        matrix[i][j] = "X"
        # display_matrix(matrix, 0.1)
        matrix, current_pos, direction = move(matrix, current_pos, direction)

    #count all X's
    summ = 0
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == "X": summ += 1
    return summ

def briteforce_part2(matrix):
    summ = 0
    # !!! I need to bruteforce only places where guard goes
    checked_matrix = copy_matrix(matrix)
    part1(checked_matrix)
    
    positions_to_try = []
    for i in range(len(checked_matrix)):
        for j in range(len(checked_matrix[0])):
            if not checked_matrix[i][j] == "X": continue
            positions_to_try.append((i, j))

    # Do not try to place obstacle on start pos
    positions_to_try.remove(find_start(matrix))
    for pos in tqdm(positions_to_try):
        i, j = pos
        matrix_copy = copy_matrix(matrix)
        #try to solve with #
        matrix_copy[i][j] = "#"
        if is_looping(matrix_copy):
            # print_matrix(matrix_copy)
            summ += 1
        else:
            # print(f"Pos {pos} - not looping")
            pass
    return summ
        
            
    #place # in all possible places and detect if guard goes into loop
    pass

def main():
    #parse stdin
    matrix = []
    for line in sys.stdin:
        matrix.append(list(line.rstrip()))

    #PART1
    matrix1 = copy_matrix(matrix)
    result1 = part1(matrix1)
    print(f"Part1: {result1}")

    #PART2
    matrix2 = copy_matrix(matrix)
    result2 = briteforce_part2(matrix2)
    print(f"Part2: {result2}")

main()
