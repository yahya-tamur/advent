# https://en.wikipedia.org/wiki/MD5

# The way I got this to work is by downloading another implementation and
# adding print statements to both.

from math import sin, floor

s = [ 7, 12, 17, 22,  7, 12, 17, 22,  7, 12, 17, 22,  7, 12, 17, 22, \
      5,  9, 14, 20,  5,  9, 14, 20,  5,  9, 14, 20,  5,  9, 14, 20, \
      4, 11, 16, 23,  4, 11, 16, 23,  4, 11, 16, 23,  4, 11, 16, 23, \
      6, 10, 15, 21,  6, 10, 15, 21,  6, 10, 15, 21,  6, 10, 15, 21 ]


K = [floor((1 << 32) * abs(sin(i+1))) for i in range(64)]


def md5(s_inp):
    len_str = len(s_inp)

    a0 = 0x67452301
    b0 = 0xefcdab89
    c0 = 0x98badcfe
    d0 = 0x10325476

    inp = int.from_bytes(bytes(s_inp, 'utf-8'), 'little')

    inp += 0x80 << (len_str)*8
    len_bytes = len_str + 1

    while len_bytes % 64 != 56:
        len_bytes += 1
    inp += (len_str*8 & 0xFFFF_FFFF_FFFF_FFFF) << 8*(len_bytes)
    len_bytes = len_bytes + 8
    for i in range(0, len_bytes*8, 512):
        M = [(inp >> (i + j*32)) & 0xFFFF_FFFF for j in range(16)]
        A, B, C, D = a0, b0, c0, d0
        for i in range(64):
            if i in range(16):
                F = (B & C) | (~B & D)
                g = i
            elif i in range(16,32):
                F = (D & B) | (~D & C)
                g = (5*i + 1) & 15
            elif i in range(32, 48):
                F = B ^ C ^ D
                g = (3*i + 5) & 15
            else:
                F = C ^ (B | (~D))
                g = 7*i & 15
            F = (F + A + K[i] + M[g]) & 0xFFFF_FFFF
            A = D
            D = C
            C = B
            B = (B + ( (F << s[i])  | (F >> (32 - s[i]))) ) & 0xFFFF_FFFF
        a0 = (a0 + A) & 0xFFFF_FFFF
        b0 = (b0 + B) & 0xFFFF_FFFF
        c0 = (c0 + C) & 0xFFFF_FFFF
        d0 = (d0 + D) & 0xFFFF_FFFF

    # answer has opposite endianness!
    ans = []
    for aa in [a0, b0, c0, d0]:
        aaa = hex(aa)[2:].zfill(8)
        for i in range(6,-1,-2):
            ans.append(aaa[i:i+2])

    return ''.join(ans)
print(md5('abc'*100))
