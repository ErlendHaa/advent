
def parse(inputfile):
    return [line.strip('\n') for line in open(inputfile).readlines()]

openchars    = { '(', '[', '{', '<'}
closingchars = { ')', ']', '}', '>'}

scores = {
    ')' : 3,
    ']' : 57,
    '}' : 1197,
    '>' : 25137,
    '(' : 1,
    '[' : 2,
    '{' : 3,
    '<' : 4
}

def matches(opening, closing):
    if opening == '(' and closing == ')': return True
    if opening == '[' and closing == ']': return True
    if opening == '{' and closing == '}': return True
    if opening == '<' and closing == '>': return True
    return False

def process(chunk):
    stack = []
    corrupted = None

    for char in chunk:
        if char in openchars:
            stack.append(char)
        elif char in closingchars:
            if matches(stack[-1], char):
                stack.pop()
            else:
                corrupted = char
                break

    return stack, corrupted

def totalscore(stack):
    totalscore = 0
    for char in reversed(stack):
        totalscore *= 5
        totalscore += scores[char]
    return totalscore

def day10_part1(inputfile):
    chunks = parse(inputfile)

    score = 0
    for chunk in chunks:
        _, corrupted = process(chunk)
        if not corrupted: continue
        score += scores[corrupted]

    return score

def day10_part2(inputfile):
    chunks = parse(inputfile)

    totalscores = []
    for chunk in chunks:
        stack, corrupted = process(chunk)
        if corrupted: continue
        if len(stack) == 0: continue
        totalscores.append(totalscore(stack))

    return sorted(totalscores)[len(totalscores) // 2]
