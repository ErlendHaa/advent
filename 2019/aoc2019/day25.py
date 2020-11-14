import random

from . import helpers

movement = [
    'north',
    'south',
    'west',
    'east'
]

instructions = {
    't' : 'take',
    'd' : 'drop',
    'i' : 'inv',
    'n' : 'north',
    's' : 'south',
    'e' : 'east',
    'w' : 'west',
}

items = [
    'loom',
    'mutex',
    'sand',
    'wreath',
]

def parse(path):
    with open(path, mode='r') as f:
        return [int(x) for x in f.readline().split(',')]

def randomwalk():
    return movement[random.choice(range(len(movement)))]

def parse_input(inst):
    try:
        x = instructions[inst.lower()]
    except KeyError:
        x = inst

    return helpers.ascii_cmd(x)

def puzzle25(path='inputs/day25.txt'):
    tape  = parse(path)
    droid = helpers.computer('ascii', tape, [])

    while True:
        droid()
        promt = helpers.ascii_interpret(droid.out)
        droid.outputs = []
        print(promt)

        response = parse_input(input('->'))
        droid.update(response)

