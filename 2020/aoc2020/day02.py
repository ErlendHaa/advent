

def parse(path):
    with open(path) as f:
        passwords = []
        for x in f.readlines():
            r, n, p = x.split()
            r = list(map(int, r.split('-')))
            passwords.append(( r[0], r[1], n.strip(':'), p ))

        return passwords

def valid_password_v1(password):
    cmin, cmax = password[0], password[1]
    char = password[2]
    pwd  = password[3]

    count = pwd.count(char)

    if (count < cmin or count > cmax): return False
    else:                              return True

def valid_password_v2(password):
    pos1, pos2 = password[0] - 1, password[1] - 1 # one-index -> zero-index
    char = password[2]
    pwd  = password[3]

    if pwd[pos1] == char and pwd[pos2] != char: return True
    if pwd[pos1] != char and pwd[pos2] == char: return True
    else:                                       return False

def puzzle2(path='inputs/day02.txt'):
    passwords = parse(path)
    part1 = len([x for x in passwords if valid_password_v1(x)])
    part2 = len([x for x in passwords if valid_password_v2(x)])

    return part1, part2
