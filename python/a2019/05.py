from intcode import execute, get_code

input = get_code()
print(f"part 1: {execute(input.copy(), [1])[-1] }")
print(f"part 2: {execute(input, [5])[0]}")
