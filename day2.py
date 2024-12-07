#How many reports are safe?

def check_report_is_safe(report: list[str]):
    print("Checking", report)
    # detect if inc or dec
    is_ascending = True
    if (report[1] - report[0]) < 0:
        is_ascending = False
    print("Is ascending?", is_ascending)
    
    for i in range(len(report)-1):
        diff_to_next = report[i+1] - report[i]
        print("Diff between i+1 and i", diff_to_next)
        #check that it follows direction
        if is_ascending:
            if diff_to_next < 0:
                return False
        else:
            if diff_to_next > 0:
                return False
        #check that absolute change is in interval 1-3
        if abs(diff_to_next) in [1,2,3]:
            pass
        else:
            return False
    return True

#parse file
f = open("day2.txt", "r")
reports = []
for line in f.readlines():
    report = list(map(int, line.split()))
    reports.append(report)

#iterate over reports and check safety (count all safe)
s = 0
for report in reports:
    if check_report_is_safe(report):
        print(report, "was safe")
        s += 1

print(s)
