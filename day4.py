import re
from pprint import pprint

# readfile and parse matrix
f = open("day4.txt")
original_arr = []
for line in f.readlines():
    original_arr.append(list(line.strip()))

#check in all directions and summ appearences
summ = 0
regex = re.compile("XMAS")
def check_occurencies(array):
    summ = 0
    for line in array:
        for m in regex.findall("".join(line)):
            summ += 1
        for m in regex.findall("".join(reversed(line))):
            summ += 1
    return summ

#check horizontally
summ += check_occurencies(original_arr)
print(summ)

#check vertically
rotated_arr = [list(row) for row in zip(*original_arr[::-1])]
summ += check_occurencies(rotated_arr)
print(summ)

#check main and second diagonal
def rotate_45(array, clockwise=True):
    n = len(array)
    m = len(array[0])
    new_size = n + m - 1
    rotated = [[] for _ in range(new_size)]
    for i in range(n):
        for j in range(m):
            if clockwise:
                rotated[i + j].append(array[i][j])
            else:
                rotated[j - i + (n - 1)].append(array[i][j])
    return rotated
    
summ += check_occurencies(rotate_45(original_arr))
print(summ)
summ += check_occurencies(rotate_45(original_arr, clockwise=False))
print(summ)

# pprint(rotated_arr)
# pprint(original_arr)
