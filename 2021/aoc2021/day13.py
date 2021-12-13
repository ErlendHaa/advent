
def parse(inputfile):
    sheet, folds = open(inputfile).read().split('\n\n')

    sheet = set([
        tuple(int(x) for x in line.split(','))
        for line
        in sheet.split('\n')
    ])

    prefix = 'fold along '
    folds = [
        fold[len(prefix):].split('=')
        for fold
        in folds.split('\n')
        if len(fold) > 0
    ]

    return sheet, list(map(lambda x: (x[0], int(x[1])), folds))

def foldsheet(sheet, fold):
    direction, foldat = fold

    updated = set()
    for x, y in sheet:
        if direction == 'x' and x > foldat: x = 2*foldat - x
        if direction == 'y' and y > foldat: y = 2*foldat - y
        updated.add((x, y))

    return updated

def draw(sheet):
    xmax, ymax = (max(s) for s in zip(*sheet))

    output = []
    for y in range(ymax + 1):
        output.append('\n')
        for x in range(xmax + 1):
            if (x, y) in sheet: output.append('#')
            else:               output.append('.')

    return ''.join(output)


def day13_part1(inputfile):
    sheet, folds = parse(inputfile)
    return len(foldsheet(sheet, folds[0]))

def day13_part2(inputfile):
    sheet, folds = parse(inputfile)
    for f in folds:
        sheet = foldsheet(sheet, f)

    return draw(sheet)


