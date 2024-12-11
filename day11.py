import sys
from tqdm import tqdm
from collections import Counter

def parse():
    for line in sys.stdin:
        data = list(line.strip().split(" "))
    return list((int(i) for i in data))

def split_number(number):
    str_num = str(number)
    mid = len(str_num) // 2
    return int(str_num[0:mid]), int(str_num[mid:])

def simulate_blinks(stones, blinks):
    stone_counts = Counter(stones)
    for _ in tqdm(range(blinks)):
        new_counts = Counter()
        for number, count in stone_counts.items():
            if number == 0:
                # 0 -> 1
                new_counts[1] += count
            elif len(str(number)) % 2 == 0:
                # %2==0 -> split
                left, right = split_number(number)
                new_counts[left] += count
                new_counts[right] += count
            else:
                # *2024
                new_counts[number * 2024] += count
        
        # Update stone counts for the next blink
        stone_counts = new_counts
    # print(stone_counts)
    return sum(stone_counts.values())

def part1(data):
    return simulate_blinks(data, 25)

def part2(data):
    return simulate_blinks(data, 75)

def main():
    #parse stdin
    data = parse()
    print(data)
    
    #PART1
    result1 = part1(data)
    print(f"Part1: {result1}")
    
    #PART2
    result2 = part2(data)
    print(f"Part2: {result2}")

main()
