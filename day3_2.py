import re
#group 1-mul 2,3-operands 4-do 5-dont
regex = re.compile(r"(mul\((-?\d+),(-?\d+)\))|(do\(\))|(don't\(\))")

f = open("day3.txt")
summ = 0

is_do = True
for line in f.readlines():
    matches = regex.finditer(line)
    for m in matches:
        # print(m, m.groups())
        if m.group(4):
            is_do = True
        if m.group(5):
            is_do = False
        if m.group(1):
            if is_do:
                result = int(m[2]) * int(m[3])
                summ += result  
print(summ)
