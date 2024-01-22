from problem import gpl
from collections import defaultdict

size = 50

m = list()
for line in gpl():
    for c in line:
        m.append({'.': 0, '|': 1, '#': 2}[c])
m.append(0)

def index(z):
    i, j = int(z.real), int(z.imag)
    if i < 0 or j < 0 or i >= size or j >= size:
        return size*size
    return i*size+j

dirs = [1,-1,1j,-1j,1+1j,1-1j,-1+1j,-1-1j]

seen = dict()

for i in range(10000):
    if i == 10:
        print(f"part 1: {m.count(1)*m.count(2)}")

    encoded = tuple(m)
    if encoded in seen:
        break
    seen[encoded] = i
    m_ = list()
    for i in range(size):
        for j in range(size):
            z = i+1j*j
            around = [m[index(z+d)] for d in dirs]
            match m[index(z)]:
                case 0:
                    if around.count(1) >= 3:
                        m_.append(1)
                    else:
                        m_.append(0)
                case 1:
                    if around.count(2) >= 3:
                        m_.append(2)
                    else:
                        m_.append(1)
                case 2:
                    if around.count(1) and around.count(2):
                        m_.append(2)
                    else:
                        m_.append(0)
    m_.append(0)
    m = m_

start, end = seen[tuple(m)], i
n = 1000000000
correct = ((n - start) % (end - start)) + start
mc = next((m for m, i in seen.items() if i == correct))
print(f"part 2: {mc.count(1)*mc.count(2)}")


