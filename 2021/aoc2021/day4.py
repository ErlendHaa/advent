import re


def parse(inputfile):
    f = open(inputfile)

    numbers = map(int, re.split(',', f.readline().strip('\n')))
    f.readline()

    boards = f.read().split('\n\n')
    boards = [[int(x) for x in re.split('\n| ', b) if x != ''] for b in boards]
    return list(numbers), boards


def updateboard(board, number):
    """Mark number by flipping the sign """
    for i, num in enumerate(board):
        if num != number: continue
        board[i] = -number
    return board

def checkrow(board, row):
    beg    = row
    stride = 5
    return len([x for x in board[beg::stride] if x > 0]) == 0

def checkcol(board, col):
    beg = col * 5
    end = beg + 5
    return len([x for x in board[beg:end] if x > 0]) == 0

def checkboard(board):
    for i in range(5):
        if checkrow(board, i): return True
        if checkcol(board, i): return True

    return False

def unmarkedsum(board):
    return sum([x for x in board if x > 0])

def play(numbers, boards):
    for num in numbers:
        for board in boards:
            updateboard(board, num)
            if checkboard(board): return board, num

def exhaustiveplay(numbers, boards):
    for i, num in enumerate(numbers):
        inplay = []

        for board in boards:
            updateboard(board, num)
            if checkboard(board): continue
            inplay.append(board)

        if len(inplay) == 1:
            # play the last game 'till the end
            return play(numbers[i:], inplay)

        boards = inplay

def day4_part1(inputfile):
    numbers, boards = parse(inputfile)
    winner, num = play(numbers, boards)
    return unmarkedsum(winner) * num

def day4_part2(inputfile):
    numbers, boards = parse(inputfile)
    winner, num = exhaustiveplay(numbers, boards)
    return unmarkedsum(winner) * num

