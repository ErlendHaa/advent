import re
import functools
import math

class Chem:
    def __init__(self, name, count, recipe):
        self.name   = name
        self.count  = count
        self.recipe = recipe
        self.stock  = 0
        self.used   = 0
        self.cap    = 1000000000000

    def load(self, chems):
        self.recipe = [(chems[name], count) for name, count in self.recipe]

    def get(self, needed):
        if self.name == 'ORE':
            if self.used + needed >= self.cap: raise Exception
            self.used += needed
            return

        if needed <= self.stock:
            self.used += needed
            self.stock -= needed
            return

        for chem, count in self.recipe:
            chem.get(count)

        self.stock += self.count

        self.get(needed)

    def __repr__(self):
        return '{} (current stock {})'.format( self.name, self.stock)

def normalize(denominators):
    common = functools.reduce( lambda x,y: (lambda a,b: next(i for i in
        range(max(a,b),a*b+1) if i%a==0 and i%b==0))(x,y), denominators)
    if common >= max(denominators): return denominators
    else:                           return [int(x/common) for x in denominators]


def parse(fpath):
    with open(fpath, 'r') as f:
        lines = [re.split(', | => |\n', line) for line in f.readlines()]

    lines = [list(filter(None, line)) for line in lines]

    ore = Chem('ORE', 1, [])
    chems = {ore.name : ore}

    for line in lines:
        counts, names = [], []

        for component in line:
            count, name = component.split(' ')
            counts.append(int(count))
            names.append(name)

        counts = normalize(counts)
        components = [(name, count) for name, count in zip(names[:-1], counts[:-1])]
        chem = Chem(names[-1], counts[-1], components)


        chems[chem.name] = chem

    for chem in chems.values():
        chem.load(chems)
    return chems

if __name__ == '__main__':
    chems = parse('inputs/day14.txt')

    chems['FUEL'].get(1)
    print('Part 1: {}'.format(chems['ORE'].used))


    cap = 1000000000000
    fuel = chems['ORE'].used

    estimate = int(math.floor(cap/fuel))
    print('low estimate: {}'.format(estimate))
    for chem in chems.values():
        chem.stock *= estimate
        chem.used  *= estimate

    print('update complete, currently used {}'.format(chems['FUEL'].used))
    while True:
        try: chems['FUEL'].get(1)
        except: break

    print('Part 2: {}'.format(chems['FUEL'].used))



