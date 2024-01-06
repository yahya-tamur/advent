import sys
import os
import datetime

if not sys.argv[-1].isdigit():
    print('Enter year as last argument, such as "python make_year.py 2020"')
    sys.exit()

year = int(sys.argv[-1])
print(f'Year {year}')

if year not in range(2015,datetime.datetime.now().year+1):
    print('Invalid year')
    sys.exit()

if os.getcwd()[-7:] != '/python':
    print('Run from the "python" folder')
    sys.exit()

try:
    os.mkdir(f'a{year}')
except FileExistsError:
    print('Folder existed')

try:
    os.remove(f'a{year}/problem.py')
except FileNotFoundError:
    pass

os.symlink('../common/problem.py', f'a{year}/problem.py')

print('Created problem.py symlink')
