import sys
import argparse

from .day1  import *
from .day2  import *
from .day3  import *
from .day4  import *
from .day5  import *
from .day6  import *
from .day7  import *
from .day8  import *
from .day9  import *
from .day10 import *
from .day11 import *
from .day12 import *
from .day13 import *
from .day14 import *
from .day15 import *
from .day16 import *
from .day17 import *
from .day20 import *
from .day21 import *

def print_solution(day, part, solution):
    print(f'Solution to day {day}, part {part}: {solution}')

def default_input(day):
    return f'inputs/day{day}.txt'

def execute_puzzle(day, part, inputpath):
    try:
        puzzle = eval(f'day{args.day}_part{part}')
    except NameError:
        print(f'NotImplemented: Solution for day {day}, part {part}')
        return None

    return puzzle(inputpath)

def arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('day',
        help    = 'puzzle to solve',
        type    = int,
        choices = range(1, 26)
    )
    parser.add_argument('-p', '--part',
        help    = 'part to solve',
        nargs   = '*',
        type    = int,
        choices = [1, 2],
        default = [1, 2]
    )
    parser.add_argument('-i', '--input',
        help    = 'path to input file',
        default = None
    )
    return parser.parse_args()

if __name__ == '__main__':
    args = arguments()

    inputpath = args.input if args.input else default_input(args.day)

    for part in args.part:
        solution = execute_puzzle(args.day, part, inputpath)
        if solution is None: continue
        print_solution(args.day, part, solution)
