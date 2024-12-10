import sys
import numpy as np
from tqdm import tqdm

def parse():
    data = []
    # For matrix data
    for line in sys.stdin:
        cells = list(line.strip())
        data.append(cells)
    return data

def part1(data):
    return

def part2(data):
    return

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
