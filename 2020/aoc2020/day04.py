
def parse(path):
    with open(path) as f:
        passports = []
        passport = {}

        for line in f.readlines():
            if not line.rstrip():
                passports.append(passport)
                passport = {}

            for pair in line.split():
                key, value = pair.split(':')
                passport[key]  = value

        passports.append(passport)
        return passports

def valid_year(value, min_year, max_year):
    if   int(value) < min_year: return False
    elif int(value) > max_year: return False
    else: return True


def valid_heigth(value):
    if len(value) < 4: return False
    hgt, units = int(value[:-2]), value[-2:]

    if units == 'cm' and hgt >= 150 and hgt <= 193: return True
    if units == 'in' and hgt >= 59  and hgt <= 76:  return True

    return False

def valid_hair_color(value):
    if len(value) != 7:   return False
    if value[0]   != '#': return False

    fmt = '0123456789abcdef'
    for char in value[1:]:
        if char not in fmt: return False

    return True

def valid_eye_color(value):
    colors = ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']
    return value in colors

def valid_pid(value):
    if len(value) != 9: return False
    try: value = int(value)
    except ValueError: return False
    return True

def valid_passport(passport, validate_fields=False):
    keys = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']

    for key in keys:
        if key not in passport: return False

        if not validate_fields: continue

        value = passport[key]
        if   key == 'byr' and not valid_year( value, 1920, 2002 ): return False
        elif key == 'iyr' and not valid_year( value, 2010, 2020 ): return False
        elif key == 'eyr' and not valid_year( value, 2020, 2030 ): return False
        elif key == 'hgt' and not valid_heigth( value ):           return False
        elif key == 'hcl' and not valid_hair_color( value ):       return False
        elif key == 'ecl' and not valid_eye_color( value ):        return False
        elif key == 'pid' and not valid_pid( value ):              return False

    return True


def puzzle4(path='inputs/day04.txt'):
    passports = parse(path)

    part1 = len([x for x in passports if valid_passport(x)])
    part2 = len([x for x in passports if valid_passport(x, validate_fields=True)])

    return part1, part2
