import sys
import numpy as np
from tqdm import tqdm
import random

def parse():
    available_patterns = []
    designs = []
    sections = "".join(sys.stdin.readlines()).strip().split("\n\n")
    for pattern in sections[0].split(", "):
        available_patterns.append(pattern)
        
    for design in sections[1].split("\n"):
        if design.startswith("#"):
            continue
        designs.append(design)
    return available_patterns, designs

def is_possible(design, available_patterns):
    remaining = design
    # print(design)
    while remaining:
        matched = False
        for p in available_patterns:
            if remaining.startswith(p):
                # print(f"Found {p} at the start of {remaining}")
                remaining = remaining.replace(p, "", 1)
                matched = True
        if not matched: 
            # print(f"{design} is IMPOSSIBLE")
            return False
    # print(f"{design} is POSSIBLE")
    return True

def is_any_sorting_possible(design, sortings):
    for sorting in sortings:
        if is_possible(design, sorting):
            return True
    return False

def part1(data):
    available_patterns, designs = data
    print(len(available_patterns))
    available_patterns_sorted = sorted(available_patterns, key=len)
    available_patterns_reversed = sorted(available_patterns, key=len, reverse=True)
    sortings = [available_patterns, available_patterns_sorted, available_patterns_reversed]

    for i in range(100):
        copy = available_patterns.copy()
        random.shuffle(copy)
        sortings.append(copy)

    summ = 0
    for design in designs:
        if is_any_sorting_possible(design, sortings):
            summ += 1
    return summ

def part2(data):
    # bruteforce algorithm:
    # get result from part1, but now keet track of each unique combination in a set()
    # combination - (pattern1, pattern2, pattern3) - design == "".join(combination)
    # for each combination that we got we can try to find subcombinations where
    # some pattern1 in combination == pattern2 + pattern3
    # and also add them to the set()
    # OOOHH, we get the same problem, recursively
    return

def main():
    #parse stdin
    data = parse()
    # print(data)
        
    #PART1
    result1 = part1(data)
    print(f"Part1: {result1}")
    
    #PART2
    result2 = part2(data)
    print(f"Part2: {result2}")

main()
