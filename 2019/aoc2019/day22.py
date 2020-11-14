from collections import deque

CUT   = 0
TABLE = 1
STACK = 2

def parse(fpath):
    shuffle = []
    with open(fpath) as f:
        for line in f.readlines():
            sub = line.strip('\n').split(' ')
            if   'cut'       in line: shuffle.append((CUT,   int(sub[-1])))
            elif 'increment' in line: shuffle.append((TABLE, int(sub[-1])))
            elif 'stack'     in line: shuffle.append((STACK, None))

    return shuffle

def deal2stack(stack):
    stack.reverse()
    return stack

def cut(stack, n):
   stack.rotate(-n)
   return stack

def deal2table(stack, n):
    cards = len(stack)
    table = [0] * cards

    pos = 0
    for card in stack:
        table[pos % cards] = card
        pos += n

    return deque(table)

def shuffle(deck, rules):
    for rule, n in rules:
        if   rule == TABLE: deck = deal2table(deck, n)
        elif rule == STACK: deck = deal2stack(deck)
        elif rule == CUT:   deck = cut(deck, n)

    return deck

def track(card_pos, rules):
    for rule, n in rules:
        if   rule == TABLE: deck = deal2table(deck, n)
        elif rule == STACK:
            card_pos = ncards - card_pos
        elif rule == CUT:
            card_pos += n


def puzzle22(path='inputs/day22.txt'):
    rules = parse(path)
    deck  = deque(range(10007))
    deck = shuffle(deck, rules)

    part1 = [i for i, card in enumerate(deck) if card == 2019][0]
    return part1, 'Not solved'
