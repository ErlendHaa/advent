from collections import defaultdict
from collections import Counter

def initialstate(inputfile):
    return Counter(map(int, open(inputfile).read().strip('\n').split(',')))

def simulate(school, days):
    for day in range(days):
        update = defaultdict(lambda: 0)

        for daysleft, nfish in school.items():
            if daysleft == 0:
                update[8] += nfish
                update[6] += nfish
            else:
                update[daysleft - 1] += nfish

        school = update

    return school

def day6_part1(inputfile):
    state  = initialstate(inputfile)
    school = simulate(state, 80)
    return sum([x for x in school.values()])

def day6_part2(inputfile):
    state  = initialstate(inputfile)
    school = simulate(state, 256)
    return sum([x for x in school.values()])
