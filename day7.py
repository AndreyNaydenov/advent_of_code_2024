import sys
from tqdm import tqdm

def parse():
    data = []
    for line in sys.stdin:
        result, numbers = line.split(":")
        result = int(result)
        numbers = list(int(i) for i in numbers.strip().split(" "))
        data.append((result, numbers))
    return data

def ternary(n):
    if n == 0: return '0'
    nums = []
    while n:
        n, r = divmod(n, 3)
        nums.append(str(r))
    return ''.join(reversed(nums))

def apply_combination(combination, numbers):
    # 0 - add; 1 - mul; 2 - glue operator
    result = numbers[0]
    for i in range(len(combination)):
        operator = combination[i]
        if operator == "0":
            result += numbers[i+1]
        elif operator == "1":
            result *= numbers[i+1]
        else:
            result = int(str(result) + str(numbers[i+1]))
    # print(f"Tried {combination} Result {result}")
    return result

def check_all_combinations(result, numbers):
    max_num_of_operators = len(numbers) - 1
    max_num_of_combinations = 2 ** (max_num_of_operators)
    for i in range(max_num_of_combinations):
        current_combination = tuple(c for c in reversed(f"{i:0{max_num_of_operators}b}"))
        current_result = apply_combination(current_combination, numbers)
        if current_result == result:
            return current_combination

def check_all_combinations_p2(result, numbers):
    max_num_of_operators = len(numbers) - 1
    max_num_of_combinations = 3 ** (max_num_of_operators)
    for i in range(max_num_of_combinations):
        current_combination = tuple(c for c in reversed(f"{ternary(i):>0{max_num_of_operators}}"))
        current_result = apply_combination(current_combination, numbers)
        if current_result == result:
            return current_combination

def can_be_solved(result, numbers):
    res = check_all_combinations(result, numbers)
    if res:
        print(f"Found possible combination {res}")
        return True
    else:
        print(f"NOT POSSIBLE")
        return False

def can_be_solved_p2(result, numbers):
    res = check_all_combinations_p2(result, numbers)
    if res:
        # print(f"Found possible combination {res}")
        return True
    else:
        # print(f"NOT POSSIBLE")
        return False

def part1(data):
    summ = 0
    for expected_result, numbers in data:
        print(f"Checking {expected_result}, {numbers}")
        if can_be_solved(expected_result, numbers):
            summ += expected_result
    return summ

def part2(data):
    summ = 0
    for expected_result, numbers in tqdm(data):
        # print(f"Checking {expected_result}, {numbers}")
        if can_be_solved_p2(expected_result, numbers):
            summ += expected_result
    return summ

def main():
    #parse stdin
    data = parse()
    
    #PART1
    result1 = part1(data)
    print(f"Part1: {result1}")
    
    #PART2
    print("Part2 calculating...")
    result2 = part2(data)
    print(f"Part2: {result2}")

main()
