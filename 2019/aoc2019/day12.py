def parse(path):
    with open(path, 'r') as f:
        return [list(map(int, pos.split(','))) for pos in f.readlines()]

class SpaceObject:
    def __init__(self, position):
        self.position = position
        self.velocity = [0,0,0]

    def __repr__(self):
        return 'pos: {}, \tvel: {}'.format(self.position, self.velocity)

    def apply_gravity(self, moons):
        for moon in moons:
            for axis, (pos, relative) in enumerate(zip(self.position, moon.position)):
                if pos == relative: continue
                if pos < relative: self.velocity[axis] += 1
                if pos > relative: self.velocity[axis] -= 1
        return self

    def simulate(self):
        for axis, vel in enumerate(self.velocity):
            self.position[axis] += vel
        return self

def fast_forward(moons, steps=1):
    for _ in range(steps):
        moons = [moon.apply_gravity(moons) for moon in moons]
        moons = [moon.simulate() for moon in moons]

    return moons

def energy(moon):
    return sum(list(map(abs, moon.position))) * sum(list(map(abs, moon.velocity)))

def orbits(moons):
    xs, ys, zs = {},{},{}
    it = 0
    orbitx, orbity, orbitz = None, None, None
    while not (orbitx and orbity and orbitz):
        x = str([(m.position[0], m.velocity[0]) for m in moons])
        y = str([(m.position[1], m.velocity[1]) for m in moons])
        z = str([(m.position[2], m.velocity[2]) for m in moons])

        if not orbitx and x in xs:
            orbitx = it - xs[x]
        else: xs[x] = it

        if not orbity and y in ys:
            orbity = it - ys[y]
        else: ys[y] = it

        if not orbitz and z in zs:
            orbitz = it - zs[z]
        else: zs[z] = it

        moons = fast_forward(moons, 1)
        it += 1

    return orbitx, orbity, orbitz

def equals(x, y, z):
    a, b, longest = tuple(sorted([x, y, z]))

    ref = longest
    while True:
        if not ref % a and not ref % b: break
        ref += longest

    return ref

def puzzle12(path='inputs/day12.txt'):
    positions = parse(path)
    moons = [SpaceObject(list(pos)) for pos in positions]

    moons = fast_forward(moons, 1000)
    part1 = sum(list(map(energy, moons)))

    moons = [SpaceObject(list(pos)) for pos in positions]
    x, y, z = orbits(moons)
    part2 = equals(x,y,z)

    return part1, part2
