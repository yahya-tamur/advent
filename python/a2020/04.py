from common import get_problem

part1 = 0
part2 = 0

for ps in get_problem().split('\n\n'):
    ps = eval('{"' + \
        ps.replace('\n', ' ')
            .strip()
            .replace(':', '":"')
            .replace(' ', '","') + '"}')

    if {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'} - set(ps):
        continue

    part1 += 1
    part2 += int(ps['byr']) in range(1920,2003) and \
        int(ps['iyr']) in range(2010,2021) and \
        int(ps['eyr']) in range(2020,2031) and \
        ((ps['hgt'][-2:] == 'cm' and int(ps['hgt'][:-2]) in range(150,194)) or \
        (ps['hgt'][-2:] == 'in' and int(ps['hgt'][:-2]) in range(59,77))) and \
        ps['hcl'][0] == '#' and len(ps['hcl']) == 7 and \
        all((c in "0123456789abcdef" for c in ps['hcl'][1:])) and \
        ps['ecl'] in {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'} and \
        len(ps['pid']) == 9 and \
        all((c in "0123456789" for c in ps['pid']))

print(f"part 1: {part1}")
print(f"part 2: {part2}")

