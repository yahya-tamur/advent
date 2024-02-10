from problem import gpl

def get_vars(line, start):
    x, *_, y = line[len(start):].split(' ')
    if x.isnumeric():
        x = int(x)
    if y.isnumeric():
        y = int(y)
    return x, y

def get_ix(letters, x):
    for i, c in enumerate(letters):
        if c == x:
            return i

def rotate(letters, x):
    return [letters[(i+x)%len(letters)] for i in range(len(letters))]

letters = list('abcdefgh')
for line in gpl():
    match line[:10]:
        case 'swap posit':
            x, y = get_vars(line, 'swap position ')
            letters[x], letters[y] = letters[y], letters[x]
        case 'swap lette':
            x, y = get_vars(line, 'swap letter ')
            x, y = get_ix(letters, x), get_ix(letters, y)
            letters[x], letters[y] = letters[y], letters[x]
        case 'rotate lef':
            x, _ = get_vars(line, 'rotate left ')
            letters = rotate(letters, x)
        case 'rotate rig':
            x, _ = get_vars(line, 'rotate right ')
            letters = rotate(letters, -x)
        case 'rotate bas':
            _, x = get_vars(line, '')
            x = get_ix(letters, x)
            letters = rotate(letters, -(x + 1 + (x >= 4)))
        case 'reverse po':
            x, y = get_vars(line, 'reverse positions ')
            if y < x:
                x, y = y, x
            letters = letters[:x] + letters[x:y+1][::-1] + letters[y+1:]
        case 'move posit':
            x, y = get_vars(line, 'move position ')
            letters.insert(y, letters.pop(x))

print(f"part 1: {''.join(letters)}")

letters = list('fbgdceah')
for line in gpl()[::-1]:
    match line[:10]:
        case 'swap posit':
            x, y = get_vars(line, 'swap position ')
            letters[x], letters[y] = letters[y], letters[x]
        case 'swap lette':
            x, y = get_vars(line, 'swap letter ')
            x, y = get_ix(letters, x), get_ix(letters, y)
            letters[x], letters[y] = letters[y], letters[x]
        case 'rotate lef':
            x, _ = get_vars(line, 'rotate left ')
            letters = rotate(letters, -x)
        case 'rotate rig':
            x, _ = get_vars(line, 'rotate right ')
            letters = rotate(letters, x)
        case 'rotate bas':
            _, x = get_vars(line, '')
            for i in range(len(letters)):
                letters_ = rotate(letters, i)
                xi = get_ix(letters_, x)
                letters__ = rotate(letters_, -(xi + 1 + (xi >= 4)))
                if letters == letters__:
                    letters = letters_
                    break
        case 'reverse po':
            x, y = get_vars(line, 'reverse positions ')
            if y < x:
                x, y = y, x
            letters = letters[:x] + letters[x:y+1][::-1] + letters[y+1:]
        case 'move posit':
            x, y = get_vars(line, 'move position ')
            letters.insert(x, letters.pop(y))

print(f"part 2: {''.join(letters)}")


