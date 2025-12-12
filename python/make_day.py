from common.init_injection import get_year_day
import os


year, _day, _ = get_year_day()
year = int(year)

day = 1

while f"{str(day).zfill(2)}.py" in os.listdir('.'):
    day += 1


if (year < 2025 and day > 25) or (year >= 2025 and day > 12):
    print('All days made!')
    exit()

f = open(f'./{str(day).zfill(2)}.py', 'w')

f.write("""from problem import get_problem, get_problem_lines, look

inp = get_problem()

print(f"part 1: {inp}")
""")

print(f"Made day {day} on year {year}")
