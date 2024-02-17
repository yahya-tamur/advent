from problem import gpl
import heapq as hq

# 🌟🌟🌟

b_max_hp, b_dam = [int(line.split(' ')[-1]) for line in gpl()]
p_hp, p_man = 50, 500

spent, hp, mana, b_hp, shield, poison, recharge = range(7)

def solve(difficulty):
    active = [[0, p_hp, p_man, b_max_hp, 0, 0, 0]]

    def run_effects(s):
        s[shield] = max(0, s[shield] - 1)
        if s[poison] > 0:
            s[b_hp] -= 3
            s[poison] -= 1
        if s[recharge] > 0:
            s[mana] += 101
            s[recharge] -= 1

    def check_end(s):
        if s[hp] <= 0:
            return True

        if s[b_hp] <= 0:
            raise StopIteration(s[spent])

        return False

    def cast(s, mana_cost, effect, duration, dam, heal):
        nonlocal active
        if s[mana] >= mana_cost and (effect == -1 or s[effect] == 0):
            s = s.copy()
            s[mana] -= mana_cost
            s[spent] += mana_cost
            s[b_hp] -= dam
            s[hp] += heal
            if effect >= 0:
                s[effect] = duration

            if check_end(s):
                return

            run_effects(s)

            if check_end(s):
                return

            s[hp] -= b_dam if s[shield] == 0 else max(b_dam - 7, 1)

            if check_end(s):
                return

            hq.heappush(active, s)

    try:
        while active:
            s = hq.heappop(active)

            run_effects(s)
            s[hp] -= difficulty

            cast(s, 53, -1, 0, 4, 0)
            cast(s, 73, -1, 0, 2, 2)
            cast(s, 113, shield, 6, 0, 0)
            cast(s, 173, poison, 6, 0, 0)
            cast(s, 229, recharge, 5, 0, 0)
    except StopIteration as ans:
        return ans

print(f"part 1: {solve(0)}")
print(f"part 2: {solve(1)}")
