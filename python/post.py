import sys

from common.init_injection import init_injection

year, day, code = init_injection()

code = "from problem import post_problem\n" + code
for i in range(2,0,-1):
    start = f'print(f"part {i}: {{'
    if (l := code.rfind(start)) == -1:
        continue
    print(f"Posting part {i}\n")
    s = 0
    #look into why this is a while and not an if
        # in case there's an if a, post this, else post this situation
    while (l := code.find(start, s)) != -1:
        ii, indent = l-1, 0
        while code[ii] == ' ':
            indent += 1
            ii -= 1
        
        r = code.rfind('}")', 0, code.find("\n", l))
        code = code[:l] + f"print('part {i}: ',end='')\n{' '*indent}print(post_problem({year}, {day}, {i}, " + \
                code[l+len(start):r] + "))" + code[r+3:]
        s = l+1

    if 'print' in sys.argv:
        print(code)
    else:
        exec(code)
    sys.exit()

print("Could not find a part to post!")
