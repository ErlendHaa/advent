from collections import deque

def parse(fpath):
    with open(fpath) as f:
        return [int(x) for x in f.readline().strip('\n')]

def phases(sequence):
    base = [0, 1, 0, -1]
    for _ in range(100):
        pattern = base
        newseq  = []

        for n in range(len(sequence)):
            element = []

            pattern = deque([y for x in base for y in (x,)*(n+1)])
            tmp = pattern.popleft()
            pattern.append(tmp)

            for value in sequence:
                mult = pattern.popleft()
                pattern.append(mult)
                element.append(value * mult)

            newseq.append(abs(sum(element)) % 10 )
        sequence = newseq
    return sequence

def puzzle16(path='inputs/day16.txt'):
    sequence = parse(path)
    part1 = phases(sequence)
    return ''.join([str(x) for x in part1[:8]]), 'Not solved'
