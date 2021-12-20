def parse(inputfile):
    alg, image = open(inputfile).read().split('\n\n')

    image = [[x for x in line] for line in image.split('\n')]

    img = set()
    offset = 100 # Hack to avoid having to deal with negative indices

    for y, line in enumerate(image):
        for x, char in enumerate(line):
            if char == '#':
                img.add((offset + x , offset + y))

    return alg, img

def image_dimensions(img):
    xmin = min(img, key = lambda x: x[0])[0] - 1
    xmax = max(img, key = lambda x: x[0])[0] + 2
    ymin = min(img, key = lambda x: x[1])[1] - 1
    ymax = max(img, key = lambda x: x[1])[1] + 2

    return (xmin, xmax), (ymin, ymax)

def generate_sequence(xbase, ybase, img, xrange, yrange, background):
    background = '0' if background == '.' else '1'
    sequence = []
    for y in range(ybase - 1, ybase + 2):
        for x in range(xbase - 1, xbase + 2):
            if   (x, y) in img:      sequence.append('1')
            elif x <= xrange[0]:     sequence.append(background)
            elif x >= xrange[1] - 1: sequence.append(background)
            elif y <= yrange[0]:     sequence.append(background)
            elif y >= yrange[1] - 1: sequence.append(background)
            else:                    sequence.append('0')

    return ''.join(sequence)

def enhance(img, alg, background):
    xrange, yrange = image_dimensions(img)

    improved = set()
    for y in range(*yrange):
        for x in range(*xrange):
            sequence = generate_sequence(x, y, img, xrange, yrange, background)
            offset   = int(sequence, 2)
            value    = alg[offset]

            if value == '#': improved.add((x, y))

    return improved

def simulate(img, alg, iterations):
    for i in range(iterations):
        background = '.' if i % 2 == 0 else alg[0]
        img = enhance(img, alg, background)

    return img

def day20_part1(inputfile):
    alg, img = parse(inputfile)
    img = simulate(img, alg, iterations = 2)
    return len(img)

def day20_part2(inputfile):
    alg, img = parse(inputfile)
    img = simulate(img, alg, iterations = 50)
    return len(img)
