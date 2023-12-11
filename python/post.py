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

    code = code.replace("get_problem()", f"get_problem(year={year},day={day})")
    code = code.replace("get_problem_lines()", \
            f"get_problem_lines(year={year},day={day})")

    for i in range(2,0,-1):
        start_pattern = f"print(f\"part {i}: {{"
        start = code.rfind(start_pattern) + len(start_pattern)
        if start == -1 + len(start_pattern):
            continue
        print(f"Posting part {i}")
        end = code.rfind('}")', 0, code.find("\n", start))
        injected = code[:start] + f"post_problem({year}, {day}, {i}, " + \
                code[start:end] + ")" + code[end:]

        exec(injected)
        sys.exit()

print("Could not find a part to post!")
