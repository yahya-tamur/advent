from common import get_problem

passports = get_problem().split('\n\n')
fields = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']

def get_field(p, field):
    if (start := p.find(field + ':')) == -1:
        return None
    start += len(field) + 1
    ends = [len(p) if e < 0 else e for e in [p.find(' ', start), p.find('\n',start)]]
    return p[start:min(ends)]

def validate(p):
    byr = get_field(p, 'byr')
    if not byr or not byr.isdigit() or int(byr) not in range(1920,2003):
        return False
    iyr = get_field(p, 'iyr')
    if not iyr or not byr.isdigit() or int(iyr) not in range(2010,2020):
        return False
    eyr = get_field(p, 'iyr')
    if not eyr not byr.isdigit() or int(eyr) not in range(2010,2020):
        return False
    hgt = get_field(p, 'hgt')
    if len(hgt)



print(f"part 1: {len([1 for p in passports if all([p.find(field + ':') != -1 for field in fields])])}")

