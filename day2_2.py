#How many reports are safe?

def check_report_is_safe(report: list[str], mistake_tolerate: bool):
    def handle_return(current_i):
        report_copy = report.copy()
        if mistake_tolerate:
            removed_item = report_copy.pop(current_i+1)
            print("Removed ", removed_item, " trying again without it")
            result = check_report_is_safe(report_copy, mistake_tolerate=False)
            if result:
                return True
            else:
                report_copy = report.copy()
                removed_item = report_copy.pop(current_i)
                print("Removed ", removed_item, " trying again without it")
                result = check_report_is_safe(report_copy, mistake_tolerate=False)
                if result:
                    return True
                else: 
                    report_copy = report.copy()
                    removed_item = report_copy.pop(current_i-1)
                    print("Removed ", removed_item, " trying again without it")
                    result = check_report_is_safe(report_copy, mistake_tolerate=False)
                    return result
        else:
            return False

    # detect if inc or dec
    is_ascending = True
    if (report[1] - report[0]) < 0:
        is_ascending = False
    print("Checking", report, "Is ascending?", is_ascending)
    
    for i in range(len(report)-1):
        diff_to_next = report[i+1] - report[i]
        #print("Diff between i+1 and i", diff_to_next)
        #check that it follows direction
        if is_ascending:
            if diff_to_next < 0:
                return handle_return(i)
        else:
            if diff_to_next > 0:
                return handle_return(i)
        #check that absolute change is in interval 1-3
        if abs(diff_to_next) in [1,2,3]:
            pass
        else:
            return handle_return(i)
    return True

#parse file
f = open("day2.txt", "r")
reports = []
for line in f.readlines():
    report = list(map(int, line.split()))
    reports.append(report)

#iterate over reports and check safety (count all safe)
s = 0
out = open("res2_2.txt", "w")
for report in reports:
    if check_report_is_safe(report, mistake_tolerate=True):
        #print(report, "was safe")
        out.write(f"{str(report)} was safe\n")
        s += 1
    else:
        out.write(f"{str(report)} was UNsafe\n")
        print(report, "was unsafe")

print(len(reports))
print(s)
