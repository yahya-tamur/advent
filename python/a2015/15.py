# f(x, y, z, w) = (a11x + a12 y + .. ) * (a 
from problem import gpl

params = [ \
        [int(spec.split(' ')[-1]) for spec in line.split(', ') ] \
        for line in gpl()]

n, m = len(params), len(params[0])

def calc(spec):
    ans, ans2 = 1, sum(prop[m-1]*s for (prop, s) in zip(params, spec))
    for i in range(m-1):
        if (p := sum(prop[i]*s for (prop, s) in zip(params, spec))) <= 0:
            ans = 0
        ans *= p
    return ans, ans2

# I initially used a gradient descent idea for part 1, but it would be harder
# to get it to work for part 2, and 104 choose 4 is small enough to try all
# options.

# As consolation, this works for any number of ingredients.
# 🌟🌟🌟 

p1, p2 = -1, -1
exec(f"""
{"".join(f"{' '*i*4}for x{i} in range(101{' '.join(f' - x{j}' for j in range(i))}):{chr(10)}" for i in range(n-1))}
{" "*n*4}val, cals = calc([{", ".join(f"x{i}" for i in range(n-1))}, 100 - {" - ".join(f"x{i}" for i in range(n-1))}])
{" "*n*4}p1 = max(val, p1)
{" "*n*4}if cals == 500:
{" "*n*4}    p2 = max(val, p2)
""")
print(f"part 1: {p1}")
print(f"part 2: {p2}")

# The ingredient matrix is very nice, and there might be a linear algebra
# solution. I thought of something for part 1, but part 2 is harder. The two
# conditions reduce the possibilities to a plane in R^4 but the function to
# optimize is nonlinear, so it's not easy, even if the matrix is diagonal.

# You could at least reduce the search space by getting two arbitrary values
# and solve for the last two using the two relations, but this is fast enough.


