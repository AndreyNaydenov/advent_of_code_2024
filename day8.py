import sys
import itertools
from tqdm import tqdm
import numpy as np

def parse():
    data = []
    for line in sys.stdin:
        cells = list(line.strip())
        data.append(cells)
    return data

def get_antennas_list(data):
    antennas = {}
    il, jl = data.shape
    for i in range(il):
        for j in range(jl):
            c = data[i][j]
            if c == ".": continue
            ls = antennas.get(c)
            if ls:
                ls.append(np.array((i, j)))
            else:
                antennas[c] = [np.array((i, j))]
    return antennas

def in_bounds(data, coord):
    il, jl = data.shape
    if coord[0] < 0 or coord[0] >= il: return False
    if coord[1] < 0 or coord[1] >= jl: return False
    return True

def get_antinodes(data, pair, limit=1):
    # print(f"Calculating antinodes for {pair}")
    antinodes = []
    diff = pair[0] - pair[1]
    #1 direction
    for n in range(limit):
        antinode = pair[0] + (diff*(n+1))
        if in_bounds(data, antinode):
            antinodes.append(antinode)
        else:
            break
    #2 direction
    for n in range(limit):
        antinode = pair[1] - (diff*(n+1))
        if in_bounds(data, antinode):
            antinodes.append(antinode)
        else:
            break
    return antinodes

def place_antinodes(grid, antinodes:list):
    for antinode in antinodes:
        grid[*antinode] = "#"

def part1(data):
    antennas = get_antennas_list(data)
    antennas_grid = np.copy(data)
    for a, coords in antennas.items():
        # print(f"Checking antenna {a}")
        for pair in itertools.combinations(coords, 2):
            antinodes = get_antinodes(data, pair, limit=1)
            place_antinodes(antennas_grid, antinodes)
    # print(antennas_grid)
    return np.count_nonzero(antennas_grid == "#")

def part2(data):
    antennas = get_antennas_list(data)
    antennas_grid = np.copy(data)
    for a, coords in antennas.items():
        # print(f"Checking antenna {a}")
        for pair in itertools.combinations(coords, 2):
            antinodes = get_antinodes(data, pair, limit=1000)
            place_antinodes(antennas_grid, antinodes)
    # print(antennas_grid)
    return np.count_nonzero(antennas_grid != ".")

def main():
    #parse stdin
    data = parse()
    data = np.array(data)
    
    #PART1
    result1 = part1(data)
    print(f"Part1: {result1}")
    
    #PART2
    result2 = part2(data)
    print(f"Part2: {result2}")

main()
