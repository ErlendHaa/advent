
def parse(inputfile):
    return [
        [x.split() for x in line.strip('\n').split(' | ')]
        for line
        in open(inputfile).readlines()
    ]

def day8_part1(inputfile):
    entries = parse(inputfile)

    segments = {
        '1' : 2,
        '4' : 4,
        '7' : 3,
        '8' : 7,
    }

    count = 0
    for _, output in entries:
        for seq in output:
            if len(seq) == segments['1']: count +=1
            if len(seq) == segments['4']: count +=1
            if len(seq) == segments['7']: count +=1
            if len(seq) == segments['8']: count +=1

    return count

def decode(signal):
    """ This is purly rule-based - and it's horrendous"""
    s = {}

    s['1'] = [x for x in signal if len(x) == 2][0]
    s['4'] = [x for x in signal if len(x) == 4][0]
    s['7'] = [x for x in signal if len(x) == 3][0]
    s['8'] = [x for x in signal if len(x) == 7][0]

    z = [x for x in s['4'] if x not in s['1']]

    s['6'] = [x for x in signal if len(x) == 6 and len([y for y in s['1'] if y in x]) == 1][0]
    s['0'] = [x for x in signal if len(x) == 6 and len([y for y in z      if y in x]) == 1][0]
    s['9'] = [x for x in signal if len(x) == 6 and x != s['0'] and x != s['6']][0]

    s['3'] = [x for x in signal if len(x) == 5 and len([y for y in s['1'] if y in x]) == 2][0]
    s['5'] = [x for x in signal if len(x) == 5 and len([y for y in z      if y in x]) == 2][0]
    s['2'] = [x for x in signal if len(x) == 5 and x != s['3'] and x != s['5']][0]

    # Use the sorted signal patterns as key's
    return { ''.join(sorted(v)) : k for k, v in s.items() }

def day8_part2(inputfile):
    entries = parse(inputfile)
    count = 0
    for signal, output in entries:
        signal = decode(signal)
        count += int(''.join([signal[''.join(sorted(x))] for x in output]))

    return count





