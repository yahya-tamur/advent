from common.init_injection import get_year_day

year, day = get_year_day()

day += 1

if day > 25:
    print('All days made!')
    exit()

print(f"Making day {day} on year {year}")

f = open(f'./{day}.py', 'w')

f.write("""from problem import get_problem, get_problem_lines

inp = get_problem()

print(f"part 1: {inp}")
""")

