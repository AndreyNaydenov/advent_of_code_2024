import re
pattern = r"mul\((-?\d+),(-?\d+)\)"
regex = re.compile(pattern)

f = open("day3.txt")
summ = 0
for line in f.readlines():
    for result in map(lambda x: int(x.group(1)) * int(x.group(2)), regex.finditer(line)):
        summ += result
print(summ)
