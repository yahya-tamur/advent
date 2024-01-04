import os
import sys

# Go to a year folder and run "python ../input.py" to run the
# most recently changed solution on the input from the file named "input"
# in the current directory instead of the usual input.
# Run "python ../input.py print" to see the changed code instead of running.

# Probably should not have just copy-pasted this part:
numfile = lambda file: file.name[-3:] == ".py" and file.name[:-3].isdigit()
mtime = lambda file: file.stat().st_mtime

file = max((file for file in os.scandir() if numfile(file)), key=mtime)

year = os.getcwd()[-4:]
day = file.name[:-3]
print(f"Day {day} on {year}")

with open(file) as contents:
    code = contents.read()
    for start in ["get_problem(", "get_problem_lines(", "gp(", "gpl("]:
        f = 0
        while (l := code.find(start,f)) != -1:
            l = l + len(start)
            r = code.find(")", l)
            code = code[:l] + f"file='input'" + code[r:]
            f = r+1

    if 'print' in sys.argv:
        print(code)
    else:
        exec(code)
