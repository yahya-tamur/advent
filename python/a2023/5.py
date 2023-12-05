from common import get_problem_lines

l = get_problem_lines(2023,5)

seeds = [int(x) for x in l[0].split(' ')[1:]]

filters = list()

for line in l[1:]:
    if line.find(':') != -1:
        filters.append(list())
        continue
    filters[-1].append(tuple([int(x) for x in line.split(' ')]))

m = 999999999999999999999
for seed in seeds:
    for filter in filters:
        for (dest, src, size) in filter:
            if seed in range(src, src+size):
                seed = dest + (seed - src)
                break
    m = min(m, seed)

print(f"part 1: {m}")

# this bs worked first try!! !!
# I feel like it have some sort of problem it it
def filt_range(filter, ranges):
    unmapped = ranges.copy()
    mapped = list()
    for (dest, src, size) in filter:
        unmapped_ = list()
        for (rng, rng_size) in unmapped:
            if src <= rng and src + size > rng:
                mapsize = min(rng_size, size - (rng - src))
                mapped.append((dest + (rng - src), mapsize))
                if mapsize < rng_size:
                    unmapped_.append((rng+mapsize, rng_size - mapsize))
            elif rng <= src and rng + rng_size > src:
                mapsize = min(size, rng_size - (src - rng))
                mapped.append((dest, mapsize))
                unmapped_.append((rng,src-rng))
                if mapsize + src - rng < rng_size:
                    unmapped_.append((src + mapsize, rng_size - (src - rng)))
            else:
                unmapped_.append((rng,rng_size))
        unmapped = unmapped_
    return unmapped + mapped

seedpairs = [(seeds[i],seeds[i+1]) for i in range(0,len(seeds),2)]
total_range = list()
for (s, size) in seedpairs:
    ranges = [(s, size)]
    for filter in filters:
        ranges = filt_range(filter, ranges)
    total_range += ranges

print(f"part 2: {min((l for l, r in total_range))}")


