import os
import sys

def get_year_day():
    numfile = lambda file: file.name[-3:] == ".py" and file.name[:-3].isdigit()
    mtime = lambda file: file.stat().st_mtime

    file = max((file for file in os.scandir() if numfile(file)), key=mtime)

    year = os.getcwd()[-4:]
    day = int(float(file.name[:-3])) # leading zeroes :)

    return year, day, file

# A new input is always necessary since get_problem will not work with no
# inputs.
def init_injection(new_input=None):

    year, day, file = get_year_day()

    if new_input is None:
        new_input=f"year={year},day={day}"

    print(f"Day {day} on {year}")

    # makes sure local modules are loaded correctly (intcode)
    sys.path.append(os.getcwd())

    code = open(file).read()

    for start in ["get_problem(", "get_problem_lines(", "gp(", "gpl(", "get_code("]:
        f = 0
        while (l := code.find(start,f)) != -1:
            l = l + len(start)
            r = code.find(")", l)
            code = code[:l] + new_input + code[r:]
            f = r+1

    return year, day, code

