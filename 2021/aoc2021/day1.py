from collections import deque


def getdepths(inputfile):
    with open(inputfile) as f:
        return list(map(int, f.readlines()))

def rollingwindow(array, windowsize):
    window = deque(array[:windowsize - 1], maxlen = windowsize)

    for x in array[windowsize - 1:]:
        window.append(x)
        yield window

def count_increase(iterable):
    return len([x for x, y in rollingwindow(iterable, 2) if x < y])

def day1_part1(inputfile):
    depths = getdepths(inputfile)
    return count_increase(depths)

def day1_part2(inputfile):
    depths  = getdepths(inputfile)
    windows = rollingwindow(depths, 3)
    reduced = list(map(sum, windows))
    return count_increase(reduced)
