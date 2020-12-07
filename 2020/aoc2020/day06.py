def parse(path):
    with open(path) as f:
        groups = []
        group = []
        for line in f.readlines():
            if not line.rstrip():
                groups.append(group)
                group = []
                continue

            group.append(set([x for x in line.strip('\n')]))

        groups.append(group)
        return groups

def puzzle6(path='inputs/day06.txt'):
    groups = parse(path)
    part1 = sum([len( set.union(*x) )        for x in groups])
    part2 = sum([len( set.intersection(*x) ) for x in groups])
    return part1, part2
