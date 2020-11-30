import sys
import argparse

from aoc2020 import *

def show_solution(sol, day):
    msg = 'Solution to day {}, part {}: {}'
    print(msg.format(day, 1, sol[0] ))
    print(msg.format(day, 2, sol[1] ))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('day', help='Puzzle to solve', type=int, choices=range(1,26))
    parser.add_argument('-i', '--input', help='path to input file')
    args = parser.parse_args()

    puzzle = eval('puzzle{}'.format(args.day))

    if args.input: show_solution( puzzle(args.input), args.day )
    else:          show_solution( puzzle(), args.day )
