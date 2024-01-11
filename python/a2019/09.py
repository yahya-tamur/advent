from intcode import execute, get_code

code = get_code()

print(f"part 1: {execute(code.copy(),[1])[0]}")
print(f"part 2: {execute(code,[2])[0]}")
