from dotenv import load_dotenv
import requests
import os
import sys

load_dotenv()

session = open(os.getenv('SESSION_FILE')).read().strip()

inputs = os.getenv('INPUT_DIR')

def get_problem(year=0, day=0, file=""):
    if file:
        return open(file).read()
    if year==0:
        # no idea if this is safe lmao
        # but it worked on 'python 7.py' and 'python a2021/7.py'
        fullpath = (os.getcwd() + '/' + sys.argv[0]).split('/')
        year = int(fullpath[-2][1:])
        day = int(fullpath[-1][:-3])

    if f'a{year}' not in os.listdir(inputs) or \
            f'{day}.txt' not in os.listdir(f'{inputs}/a{year}'):
        r = requests.get(f'https://adventofcode.com/{year}/day/{day}/input',
                         cookies={'session':session})
        if r.ok:
            if f'a{year}' not in os.listdir(inputs):
                os.mkdir(f'{inputs}/a{year}')
            with open(f'{inputs}/a{year}/{day}.txt', 'w') as file:
                file.write(r.text)
        else:
            print("Error getting problem. Received:")
            print()
            print(r.text)
            print()
            print("Maybe the session is expired?")
            print()
            sys.exit()

    return open(f'{inputs}/a{year}/{day}.txt').read()

def get_problem_lines(year=0, day=0, file=""):
    return [s for s in get_problem(year=year, day=day, file=file).split('\n') \
            if s]

def post_problem(year, day, level, ans):
    print(f"Sending {ans}")
    resp = requests.post(f'https://adventofcode.com/{year}/day/{day}/answer', \
            {'level' : str(level), 'answer': str(ans) },
            cookies={'session':session})
    start, end = "<article>", "</article>"
    l = resp.text.find(start) + len(start)
    r = resp.text.find(end, l)
    ans = resp.text[l:r]
    while ans.find('<') != -1:
        ans = ans[:ans.find('<')] + ans[ans.find('>')+1:]
    splitans = []
    while ans:
        i = ans.rfind(' ',0,80)
        if i == 0 or len(ans) < 80:
            i = len(ans)
        splitans.append(ans[:i].strip())
        ans = ans[i:]
    return '\n'.join(splitans)


gp = get_problem
gpl = get_problem_lines


if __name__ == '__main__':
    if 'get' in sys.argv:
        print(get_problem(sys.argv[2],sys.argv[3]))
    elif 'post' in sys.argv:
        print(post_problem(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]))
    elif 'refresh' in sys.argv:
        try:
            os.remove(f'{inputs}/a{sys.argv[2]}/{sys.argv[3]}.txt')
        except FileNotFoundError:
            pass
        print(get_problem(sys.argv[2],sys.argv[3]))
    else:
        print("To get:")
        print("python problem.py get <year> <day>")
        print("To post:")
        print("python problem.py post <year> <day> <level> <answer>")
        print("To get from the internet:")
        print("python problem.py refresh <year> <day>")
