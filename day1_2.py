#parse input into 2 separate lists
f = open("day1.txt")

l1 = []
l2 = []

for line in f.readlines():
    e1, e2 = line.split()
    l1.append(int(e1))
    l2.append(int(e2))

#sort lists
# l1 = sorted(l1)
# l2 = sorted(l2)

#iterate over list 1 and calculate similarity, summ up to get answer
summ = 0
for i in range(len(l1)):
    el = l1[i]
    sim = el * l2.count(el)
    summ += sim

print(summ)
#print(l1)
#print(l2)
