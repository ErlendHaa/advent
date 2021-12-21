from itertools   import product
from collections import Counter
from functools   import lru_cache


def parse(inputfile):
    return (int(k.strip('\n')[-1]) for k in open(inputfile).readlines())

class Dice:
    def __init__(self):
        self.rolls = 0

    def __next__(self):
        cur = self.rolls
        self.rolls += 1
        return cur % 100 + 1

def move(pos, steps):
    return (pos + steps - 1) % 10 + 1

def update(pos, score, dice):
    steps  = sum(next(dice) for _ in range(3))
    pos    = move(pos, steps)
    score += pos
    return pos, score

def simulate(p1, p2, score1 = 0, score2 = 0):
    dice = Dice()

    while True:
        p1, score1 = update(p1, score1, dice)
        if score1 > 1000: break

        p2, score2 = update(p2, score2, dice)
        if score2 > 1000: break

    return min(score1, score2), dice.rolls

@lru_cache(maxsize = None)
def universes(pos1, pos2, score1 = 0, score2 = 0):
    if score1 >= 21: return 1, 0
    if score2 >= 21: return 0, 1

    wins = (0, 0)
    distribution = Counter(sum(p) for p in product(range(1,4), repeat = 3))
    for steps, count in distribution.items():
        pos   = move(pos1, steps)
        score = score1 + pos

        p2wins, p1wins = universes(pos2, pos, score2, score)
        wins = (wins[0] + p1wins * count, wins[1] + p2wins * count)

    return wins

def day21_part1(inputfile):
    p1, p2 = parse(inputfile)
    score, rolls = simulate(p1, p2)
    return score * rolls

def day21_part2(inputfile):
    p1, p2 = parse(inputfile)
    wins = universes(p1, p2)
    return max(wins)
