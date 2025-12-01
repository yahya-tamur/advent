from common.init_injection import get_year_day

year, day, _ = get_year_day()

day += 1

if day > 25:
    print('All days made!')
    exit()

f = open(f'./{str(day).zfill(2)}.py', 'w')

f.write("""from problem import get_problem, get_problem_lines, look

inp = get_problem()

print(f"part 1: {inp}")
""")

print(f"Made day {day} on year {year}")
