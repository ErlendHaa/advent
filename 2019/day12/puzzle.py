def parse(path):
    with open(path, 'r') as f:
        return [list(map(int, pos.split(','))) for pos in f.readlines()]

class SpaceObject:
    def __init__(self, position):
        self.position = position
        self.velocity = [0,0,0]

        self.orbit_steps = []
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

def orbit(moons):
    while True:
        moons = [moon.apply_gravity(moons) for moon in moons]
        moons = [moon.simulate() for moon in moons]


if __name__ == '__main__':
    positions = parse('input.txt')
    moons = [SpaceObject(pos) for pos in positions]

    moons = fast_forward(moons, 1000)
    part1 = sum(list(map(energy, moons)))

    print('Part 1: {}'.format(part1))
#    print('Part 2: {}'.format(part2))

