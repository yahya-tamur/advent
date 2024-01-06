from problem import get_problem
stars = get_problem().split('\n\n')
stars = [[list(line) for line in star.split('\n') if line] for star in stars]

def href(star, smudges):
    ans = 0
    for i in range(len(star)-1):
        k = 0
        diff = 0
        while i-k >= 0 and i+k+1 < len(star):
            diff += sum([star[i-k][j] != star[i+k+1][j] \
                    for j in range(len(star[0]))])
            if diff > smudges:
                break
            k += 1
        if diff == smudges:
            ans += i + 1 # one-indexed rows
    return ans

def vref(star, smudges):
    ans = 0
    for j in range(len(star[0])-1):
        k=0
        diff = 0
        while j-k >= 0 and j+k+1 < len(star[0]):
            diff += sum([star[i][j-k] != star[i][j+k+1] \
                    for i in range(len(star))])
            if diff > smudges:
                break
            k += 1
        if diff == smudges:
            ans += j + 1
    return ans

ans = [0,0]
for star in stars:
    for i in range(2):
        ans[i] += href(star,i)*100 + vref(star,i)

print(f"part 1: {ans[0]}")
print(f"part 2: {ans[1]}")
