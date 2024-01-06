import sys

from init_injection import init_injection

year, day, code = init_injection()

code = "from common import post_problem\n" + code
for i in range(2,0,-1):
    start = f'print(f"part {i}: {{'
    if (l := code.rfind(start)) == -1:
        continue
    l = l + len(start)
    print(f"Posting part {i}")
    r = code.rfind('}")', 0, code.find("\n", l))
    injected = code[:l] + f"post_problem({year}, {day}, {i}, " + \
            code[l:r] + ")" + code[r:]

    if 'print' in sys.argv:
        print(injected)
    else:
        exec(injected)
    sys.exit()

print("Could not find a part to post!")
