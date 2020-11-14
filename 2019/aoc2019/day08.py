import numpy as np
import matplotlib.pyplot as plt

TRANSPARENT = 2

def parse(path):
    raw = []
    with open(path, 'r') as f:
        while True:
            x = f.read(1)
            if not x: return x
            try:
                raw.append(int(x))
            except:
                break
    layers = []
    for i in range(0, len(raw), 25*6):
        x = np.reshape(np.array(raw[i:i + (25*6)]), (6,25))
        layers.append(x)

    return layers

def part1(layers):
    counts = []
    for layer in layers:
        unique, count = np.unique(layer, return_counts=True)
        counts.append(dict(zip(unique, count)))

    m, idx = float('inf'), 0
    for i, x in enumerate(counts):
        if x[0] >= m: continue
        m = x[0]
        idx = i

    return counts[idx][1] * counts[idx][2]

def part2(layers):

    layers = [x.flatten() for x in layers]

    image = layers[-1]
    for layer in reversed(layers[:-1]):
        for i, new in enumerate(layer):
            if new == TRANSPARENT: continue
            image[i] = new

    image = np.reshape(image, (6, 25))

    plt.imshow(image)
    plt.show()

def puzzle8(path='inputs/day08.txt'):
    layers = parse(path)

    part2(layers)
    return part1(layers), 'see plot'
