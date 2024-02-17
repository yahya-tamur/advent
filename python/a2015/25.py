from problem import gp

words = gp().replace(',','').replace('.','').split(' ')
row, column = int(words[-3]), int(words[-1])

r, c = 1, 1
num = 20151125
while not (r == row and c == column):
    num = (num*252533) % 33554393
    if r == 1:
        r, c = c+1, 1
    else:
        r, c = r-1, c+1

print(f"part 1: {num}")
print(f"part 2: {0}")
