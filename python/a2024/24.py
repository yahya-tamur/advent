from problem import get_problem, get_problem_lines, look
from collections import defaultdict

gates = dict()

lines = get_problem_lines()
split = next(i for (i, line) in enumerate(lines) if ':' not in line)

for line in lines[:split]:
    l, r = line.split(': ')
    gates[l] = int(r)

for _ in range(len(gates)):
    for line in lines[split:]:
        l, op, r, _arrow, res = line.split(' ')
        if res not in gates and l in gates and r in gates:
            match op:
                case 'AND':
                    gates[res] = gates[l] & gates[r]
                case 'XOR':
                    gates[res] = gates[l] ^ gates[r]
                case 'OR':
                    gates[res] = gates[l] | gates[r]

ans1 = ""

for i in range(100):
    if (zval := gates.get('z' + str(i).zfill(2))) is not None:
        ans1 = str(zval) + ans1
    else:
        break
print(f"part 1: {int(ans1, 2)}")


inn, out = {name: set() for name in gates}, {name: None for name in gates}

first_carry = None

for line in lines[split:]:
    l, op, r, _, res = line.split(' ') 
    if {l, op, r} == {'x00', 'AND', 'y00'}:
        first_carry = res
    numeric = l[1:].isnumeric()
    out[res] = (op, numeric)
    inn[l].add(op)
    inn[r].add(op)

problems = []
for name in gates:
    if name in {'z00', 'z45', first_carry}:
        continue
    if name[1:].isnumeric():
        if name[0] == 'z' and out[name] != ('XOR', False):
            problems.append(name)
        continue

    if (inn[name], out[name]) not in [\
            ({'OR'}, ('AND', False)), \
            ({'AND', 'XOR'}, ('XOR', True)), \
            ({'OR'}, ('AND', True)), \
            ({'AND', 'XOR'}, ('OR', False))]:
        problems.append(name)

problems.sort()
print(f"part 2: {','.join(problems)}")
