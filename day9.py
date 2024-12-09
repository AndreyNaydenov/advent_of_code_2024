import sys
import itertools
from tqdm import tqdm
import numpy as np

def parse():
    data = next(sys.stdin).strip()
    return data

def part1(data):
    list_with_spaces = []
    current_file_id = 0
    for i in range(len(data)):
        num = int(data[i])
        if i % 2 == 0:
            for j in range(num):
                list_with_spaces.append(str(current_file_id))
            current_file_id += 1
        else:
            for j in range(num):
                list_with_spaces.append(".")
    # print("".join(list_with_spaces))
    # while "." in list_with_spaces:
    for i in tqdm(range(list_with_spaces.count("."))):
        last_el = list_with_spaces.pop()
        if last_el == ".": continue
        index = list_with_spaces.index(".")
        list_with_spaces[index] = last_el
    # print("".join(list_with_spaces))

    summ = 0
    for i in range(len(list_with_spaces)):
        summ += i * int(list_with_spaces[i])
    return summ

def remove_file_from_end(ls, file_id, file_len):
    file_left = file_len
    for i in range(-1,-len(ls)-1, -1):
        if file_left == 0:
            return
        try:
            el = ls[i]
        except:
            return
        if el == str(file_id):
            ls[i] = "."
            file_left -= 1
    print(f"ERROR {"".join(ls)}")

def part2(data):
    list_with_spaces = []
    current_file_id = 0
    for i in range(len(data)):
        num = int(data[i])
        if i % 2 == 0:
            for j in range(num):
                list_with_spaces.append(str(current_file_id))
            current_file_id += 1
        else:
            for j in range(num):
                list_with_spaces.append(".")

    # print("".join(list_with_spaces))    
    for file_id in tqdm(reversed(range(current_file_id)), total=current_file_id):
        file_len = list_with_spaces.count(str(file_id))
        # print(f"Trying to move {file_id}, len {file_len}")
        #check if we have that space
        space = 0
        space_start_index = 0
        for j in range(len(list_with_spaces)):
            if list_with_spaces[j] == str(file_id): break
            if list_with_spaces[j] == ".":
                space += 1
            else:
                space = 0
            if space == file_len:
                space_start_index = j - file_len + 1
                # print(f"Found space at {space_start_index}")
                break
        if space_start_index == 0:
            # print(f"Failed to find space")
            continue

        remove_file_from_end(list_with_spaces, file_id, file_len)
        for j in range(file_len):
            list_with_spaces[space_start_index+j] = str(file_id)
        # print("".join(list_with_spaces))
    # print("".join(list_with_spaces))
                

    summ = 0
    for i in range(len(list_with_spaces)):
        el = list_with_spaces[i]
        if el == ".": continue
        summ += i * int(el)
    return summ

def main():
    #parse stdin
    data = parse()
    
    #PART1
    result1 = part1(data)
    print(f"Part1: {result1}")
    
    #PART2
    result2 = part2(data)
    print(f"Part2: {result2}")

main()
