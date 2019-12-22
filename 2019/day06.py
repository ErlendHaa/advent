

def parse(fpath):
   with open(fpath) as f:
        return [x.strip('\n').split(')') for x in f]

class node:
    def __init__(self, name, parent, childs=None):
        if childs is None: childs = []

        self.name   = name
        self.childs = childs
        self.parent = parent
        self.orbits = 0

    def add(self, child):
        self.childs.append( child )

    def __repr__(self):
        return '{}'.format(self.name)

    def __eq__(self, name):
        return self.name == name

    def __hash__(self):
        return hash(self.name)

def mkuniverse(pairs):
    universe = {}
    for pname, cname in pairs:
        if pname not in universe:
            universe[pname] = node(pname, None)

        if cname in universe:
            universe[cname].parent = universe[pname]
        else:
            universe[cname] = node(cname, parent=universe[pname])
        universe[pname].add( universe[ cname ] )

    def update_orbit(planet):
        for child in planet.childs:
            child.orbits = planet.orbits + 1
            update_orbit(child)

    update_orbit(universe['COM'])
    return universe

def distance(start, end):
    def root(child, path):
        if child.parent:
            path.append(child)
            return root(child.parent, path)
        return path

    p1 = set(root( start, [] ))
    p2 = set(root( end, [] ))

    return len(p1.symmetric_difference(p2)) - 2

if __name__ == '__main__':
    pairs   = parse('inputs/day06.txt')
    planets = mkuniverse(pairs)

    part1 = sum([p.orbits for p in planets.values()])
    part2 = distance(planets['YOU'], planets['SAN'])

    print('Part 1: {}'.format(part1))
    print('Part 2: {}'.format(part2))
