from problem import gpl
from md5 import fast_md5
from multiprocessing import Pool

inp = gpl()[0]

#inp = 'abc'

#i is 0 throuh 20. proccesses values in 
def f(i):
    ans = list()
    for j in range(i*2_000_000, (i+1)*2_000_000):
        if (md := fast_md5(inp + str(j)))[:5] == '00000':
            ans.append((j, md[5:7]))
    return ans

with Pool(20) as p:
    ans = []
    for a in p.map(f, range(20)):
        ans += a
    ans.sort()
    ans = [a[1] for a in ans]


    print(f"part 1: {''.join([a[0] for a in ans[:8]])}")
    key = ['x']*8
    left = {str(i) for i in range(8)}

    for a in ans:
        if a[0] in left:
            key[int(a[0])] = a[1]
            left.remove(a[0])

    print(f"part 2: {''.join(key)}")

