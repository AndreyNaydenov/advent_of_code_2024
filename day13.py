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
    # print(f"Best {current_best}, {current_best_cost}")
    return current_best, current_best_cost

def is_positive_int(num):
    if not num.is_integer(): return False
    if num < 0: return False
    return True

def solve_machine(machine):
    a, b, prize = machine
    ax, ay = a
    bx, by = b
    px, py = prize
    # using the math and linear algebra we get equation system:
    # ax * an + bx * bn = px
    # ay * an + by * bn = py
    # after solving the equation we get formula
    an = (py*bx-px*by)/(ay*bx-ax*by)
    # print(f"{an=}")
    if not is_positive_int(an): return
    bn = (px-ax*an)/bx
    # print(f"{bn=}")
    if not is_positive_int(bn): return

    # calc cost
    cost = int(an) * 3 + int(bn)
    return cost

def part1(data):
    summ = 0
    for machine in data:
        solutions = get_all_solutions(machine)
        if not solutions: continue
        solution, cost = choose_best_solution(machine, solutions)
        summ += cost
    return summ

def part2(data):
    summ = 0
    for machine in data:
        # add 10000000000000 to coords
        prize = machine[2]
        prize += 10000000000000
        cost = solve_machine(machine)
        if cost:
            summ += cost
    return summ

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
