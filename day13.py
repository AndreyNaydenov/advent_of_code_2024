import sys
import numpy as np
from tqdm import tqdm

def parse():
    data = []
    # For matrix data
    for section in "".join(sys.stdin.readlines()).strip().split("\n\n"):
        # print(section)
        a, b, prize = section.split("\n")
        a = a.replace("Button A: X+", "").replace(", Y+", " ").split()
        b = b.replace("Button B: X+", "").replace(", Y+", " ").split()
        prize = prize.replace("Prize: X=", "").replace(", Y=", " ").split()
        a = np.array(tuple(int(x) for x in a))
        b = np.array(tuple(int(x) for x in b))
        prize = np.array(tuple(int(x) for x in prize))
        data.append((a, b, prize))
    return data

def get_all_solutions(machine, limit=101):
    a, b, prize = machine
    possible_solutions = []
    for ax in range(limit):
        for bx in range(limit):
            res = a * ax + b * bx
            # print(res, prize)
            if (res == prize).all():
                possible_solutions.append((ax, bx))
    return possible_solutions

def choose_best_solution(machine, solutions):
    current_best = ()
    current_best_cost = 500
    for s in solutions:
        ax, bx = s
        cost = ax * 3 + bx
        if cost < current_best_cost:
            current_best_cost = cost
            current_best = s
    print(f"Best {current_best}, {current_best_cost}")
    return current_best, current_best_cost

def part1(data):
    summ = 0
    for machine in tqdm(data):
        solutions = get_all_solutions(machine)
        if not solutions: continue
        solution, cost = choose_best_solution(machine, solutions)
        summ += cost
    return summ

def part2(data):
    summ = 0
    for machine in tqdm(data):
        prize = machine[2]
        prize += 10000000000000
        solutions = get_all_solutions(machine, limit=1000000000000)
        if not solutions: continue
        solution, cost = choose_best_solution(machine, solutions)
        summ += cost
    return summ

def main():
    #parse stdin
    data = parse()
    # print(data)
    
    #PART1
    # result1 = part1(data)
    # print(f"Part1: {result1}")
    
    #PART2
    result2 = part2(data)
    print(f"Part2: {result2}")

main()
