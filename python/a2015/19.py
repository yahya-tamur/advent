from problem import gp

inp = gp()

specs, mol = inp.split('\n\n')

specs = [spec.split(' => ') for spec in specs.split('\n')]

seen = set()

for l, r in specs:
    for i in range(len(mol)-len(l)+1):
        if mol[i:i+len(l)] == l:
            seen.add(mol[:i] + r + mol[i+len(l):])

print(f"part 1: {len(seen)}")

# I spent a long time trying to actually parse the string, but I couldn't get
# it fast enough. I saw the solution on reddit, and tried to write a parser
# assuming every rule is either a pair or a parentheses, but it still wasn't
# fast enough, and with the assumption, writing a complicated parser just to
# get the number of steps seemed unnecessary.


mol = mol.replace('Rn', '').replace('Ar', '')
print(f"part 2: {sum(c.isupper() for c in mol)  - 2*mol.count('Y') - 1}")

