from problem import gpl

# I did implement an interpreter (it's in a previous commit)
# but I needed to understand the code for part 2 anyway.

# Nobody on reddit outright posted their own input so I didn't check
# but I'm pretty sure this will work on any input.

solve = lambda n: \
        (lambda f, n: 1 if n == 1 else n*f(f, n-1))( \
        (lambda f, n: 1 if n == 1 else n*f(f, n-1)), n) + \
        int(gpl()[19].split(' ')[1])*int(gpl()[20].split(' ')[1])

print(f"part 1: {solve(7)}")
print(f"part 2: {solve(12)}")
