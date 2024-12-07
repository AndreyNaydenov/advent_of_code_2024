# readfile and parse matrix
f = open("day4.txt")
original_arr = []
for line in f.readlines():
    original_arr.append(list(line.strip()))

#ignore outer 1 line of elements
#iterate over the rest and check
summ = 0
xl = len(original_arr[0])
yl = len(original_arr)
for y in range(yl):
    if y in (0, yl - 1): continue
    for x in range(xl):
        if x in (0, xl - 1): continue
        cur_el = original_arr[y][x]
        #if not A, skip
        if not cur_el == "A": continue
        #if A, check that near cells have right letters
        lu_el = original_arr[y-1][x-1]
        ld_el = original_arr[y+1][x-1]
        ru_el = original_arr[y-1][x+1]
        rd_el = original_arr[y+1][x+1]
        els_string = "".join((lu_el, ru_el, rd_el, ld_el))
        if els_string in ("MMSS", "MSSM", "SSMM", "SMMS"):
            summ += 1
print(summ)
        
        
        
