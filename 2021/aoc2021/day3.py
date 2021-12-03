
def parsecodes(inputfile):
    with open(inputfile) as f:
        return [x.strip('\n') for x in f.readlines()]

def b2d(binary):
    return int(binary, 2)

def flip(bits):
    return ''.join('1' if x == '0' else '0' for x in bits)

def mostcommonbit(codes, bitpos):
    bits = [code[bitpos] for code in codes]
    # This is crazy, but essentially max() will always pick the first value if
    # there are multiple 'max'-values. The sorting makes sure that '1' is
    # before '0' such that '1' is always picked when there are an equal amont
    # of ones and zeroes.
    sbits = sorted(list(set(bits)), reverse = True)
    return max(sbits, key = bits.count)

def decode_gamma(codes):
    # This heavily assumes that all codes are of equal length. But that is
    # resonable.
    nbits = len(codes[0])
    gamma = [mostcommonbit(codes, bitpos) for bitpos in range(nbits)]
    return ''.join(gamma)

def decode_rating(candidates, leastcommon = False):
    pos = 0
    while len(candidates) > 1:
        bit = mostcommonbit(candidates, pos)
        if leastcommon: bit = flip(bit)

        candidates = [c for c in candidates if c[pos] == bit]
        pos += 1

    return candidates[0]


def day3_part1(inputfile):
    codes   = parsecodes(inputfile)
    gamma   = decode_gamma(codes)
    epsilon = flip(gamma)

    return b2d(gamma) * b2d(epsilon)

def day3_part2(inputfile):
    codes = parsecodes(inputfile)
    ogr   = decode_rating(codes)
    co2sr = decode_rating(codes, leastcommon = True)

    return b2d(ogr) * b2d(co2sr)
