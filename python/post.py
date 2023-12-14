import os
import sys

numfile = lambda file: file.name[-3:] == ".py" and file.name[:-3].isdigit()
mtime = lambda file: file.stat().st_mtime

file = max((file for file in os.scandir() if numfile(file)), key=mtime)

year = os.getcwd()[-4:]
day = file.name[:-3]
print(f"Day {day} on {year}")

with open(file) as contents:
    code = "from common import post_problem\n" + contents.read()

    for start in ["get_problem(", "get_problem_lines("]:
        if (l := code.find(start)) != -1:
            l = l + len(start)
            r = code.find(")", l)
            code = code[:l] + f"year={year},day={day}" + code[r:]

    for i in range(2,0,-1):
        start = f"print(f\"part {i}: {{"
        if (l := code.rfind(start)) == -1:
            continue
        l = l + len(start)
        print(f"Posting part {i}")
        r = code.rfind('}")', 0, code.find("\n", l))
        injected = code[:l] + f"post_problem({year}, {day}, {i}, " + \
                code[l:r] + ")" + code[r:]

        #print(injected)
        exec(injected)
        sys.exit()

print("Could not find a part to post!")
