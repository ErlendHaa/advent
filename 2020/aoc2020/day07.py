from collections import defaultdict
import re

def parse(path):
    graph = defaultdict(list)
    with open(path) as f:
        for line in f.readlines():
            line = re.split('contain |, ', line.strip('.\n'))
            node = ' '.join(line[0].split(' ')[:2]).rstrip()

            for child in line[1:]:
                child = child.split(' ')
                try:
                    w = int(child[0])
                except ValueError:
                    graph[node] = []
                    break

                v = ' '.join(child[1:3]).rstrip()
                graph[node].append( (v, w) )

    return graph


def contains(bag, target, graph):
    if bag == target: return True
    for v, _ in graph[bag]:
        if contains(v, target, graph): return True

    return False

def content(bag, graph):
    size = 1
    for v, w in graph[bag]:
        size = size + (w * content(v, graph))

    return size

def puzzle7(path='inputs/day07.txt'):
    graph = parse(path)

    part1 = len([x for x in graph.keys() if contains(x, 'shiny gold', graph)])
    part1 -= 1 # Skip the one where shiny gold is the root node

    part2 = content('shiny gold', graph)
    return part1, part2
