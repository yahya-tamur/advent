from dotenv import load_dotenv
import requests
import os

load_dotenv()

session = open(os.getenv('SESSION_FILE')).read()
# remove new line
session = session[:-1]

inputs = os.getenv('INPUT_DIR')

def get_problem(year, day):
    if f'a{year}' not in os.listdir(inputs):
        os.mkdir(f'{inputs}/a{year}')
    if f'{day}.txt' not in os.listdir(f'{inputs}/a{year}'):
        r = requests.get(f'https://adventofcode.com/{year}/day/{day}/input',
                         cookies={'session':session})
        with open(f'{inputs}/a{year}/{day}.txt', 'w') as file:
            file.write(r.text)

    return open(f'{inputs}/a{year}/{day}.txt').read()

def get_problem_lines(year, day):
    return [s for s in get_problem(year, day).split('\n') if s]


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 3:
        print('example usage:\npython common.py 2021 11')
        sys.exit()
    print(get_problem(sys.argv[1],sys.argv[2]))
