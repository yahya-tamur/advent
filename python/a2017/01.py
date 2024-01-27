from problem import gp

l = [int(c) for c in gp().strip()]

print(f"part 1: {sum((l[i] * (l[i] == l[(i+1) % len(l)]) for i in range(len(l))))}")
print(f"part 2: {sum((l[i] * (l[i] == l[(i+(len(l)//2)) % len(l)]) for i in range(len(l))))}")

