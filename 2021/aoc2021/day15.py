from queue import PriorityQueue

def construct_graph(inputfile):
    graph = {}
    for y, line in enumerate(open(inputfile).readlines()):
        for x, cost in enumerate(line.strip('\n')):
            graph[(x,y)] = int(cost)

    return graph, (x + 1, y + 1)

def expand_graph(graph, stride):
    xstride, ystride = stride

    expanded = {}
    for (xbase, ybase), costbase in graph.items():
        for xoff in range(5):
            for yoff in range(5):
                x    = xbase + xoff * xstride
                y    = ybase + yoff * ystride
                cost = costbase + xoff + yoff

                expanded[(x, y)] = cost if cost <= 9 else cost % 9

    return expanded, (xstride * 5, ystride * 5)

def neighbors(node, graph):
    x, y = node
    candidates = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
    return [c for c in candidates if c in graph]

def find_path(graph, start, goal):
    frontier = PriorityQueue()
    frontier.put((0, start))

    came_from   = { start : None }
    cost_so_far = { start : 0    }

    while not frontier.empty():
        _, current = frontier.get()
        if current == goal: break

        for node in neighbors(current, graph):
            cost = cost_so_far[current] + graph[node]

            if node not in cost_so_far or cost < cost_so_far[node]:
                frontier.put((cost, node))
                cost_so_far[node] = cost
                came_from[node]   = current

    return came_from

def cost_of_path(path, graph, start, goal):
    cost = 0
    current = goal
    while current != start:
        cost   += graph[current]
        current = path[current]

    return cost

def getgoal(size):
    return (size[0] - 1, size[1] - 1)

def day15_part1(inputfile):
    graph, size = construct_graph(inputfile)

    start = (0, 0)
    goal  = getgoal(size)
    path  = find_path(graph, start, goal)
    return cost_of_path(path, graph, start, goal)

def day15_part2(inputfile):
    graph, size = construct_graph(inputfile)
    graph, size = expand_graph(graph, size)

    start = (0, 0)
    goal  = getgoal(size)
    path  = find_path(graph, start, goal)
    return cost_of_path(path, graph, start, goal)

