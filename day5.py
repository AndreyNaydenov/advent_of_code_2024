#parse input
rules = []
updates = []
with open("day5.txt") as f:
    part1, part2 = f.read().split("\n\n")
    for line in part1.split("\n"):
        num1, num2 = line.split("|")
        rules.append((int(num1), int(num2)))
    for line in part2.split("\n"):
        if line:
            update = list(map(int, line.split(",")))
            updates.append(update)

#prepare dicts with rules
before_dict = {}
after_dict  = {}
for rule in rules:
    before_num, after_num = rule
    #add to before_list if not present, if present append to list
    before_list = before_dict.get(after_num)
    if before_list:
        before_list.append(before_num)
    else:
        before_dict[after_num] = [before_num]
    #add to after_list if not present, if present append to list
    after_list = after_dict.get(before_num)
    if after_list:
        after_list.append(after_num)
    else:
        after_dict[before_num] = [after_num]

# checks update, if good return middle el value, else None
def check_update(update, before_dict, after_dict):
    # print(f"Checking update {update}")
    for i in range(len(update)):
        current_el = update[i]
        # print(f"Checking el {current_el}")
        rules_before = before_dict.get(current_el)
        # print(f"What shouldn't be after: {rules_before}")
        rules_after = after_dict.get(current_el)
        # print(f"What shouldn't be before: {rules_after}")
        #check after
        if rules_before:
            for j in range(i+1,len(update)):
                if update[j] in rules_before:
                    # print(f"WRONG - {update[j]} is after {update[i]}")
                    return
        #check before
        if rules_after:
            for j in range(i):
                if update[j] in rules_after:
                    print(f"WRONG - {update[j]} is before {update[i]}")
                    return
    #if checks passed, return middle element
    middle = update[len(update)//2]
    return middle
                
    
summ = 0
part2_updates = []
for update in updates:
    #check each element and check that elements after are not in before_dict and elements before are not in after_dict
    result = check_update(update, before_dict, after_dict)
    if result:
        summ += result
    else:
        part2_updates.append(update)
print(f"Part1: {summ}")

from functools import cmp_to_key
def compare(next_el, curr_el):
    for rule in rules:
        if not curr_el == rule[0]: continue
        if not next_el == rule[1]: continue
        return 1
    return -1

summ_part2 = 0
for update in part2_updates:
    # print(f"Reordering {update}")
    sorted_update = sorted(update, key=cmp_to_key(compare))
    # print(f"Reordered: {sorted_update}")
    summ_part2 += sorted_update[len(sorted_update)//2]

print(f"Part2: {summ_part2}")
