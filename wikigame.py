import random
import heapq
from collections import deque


def load_graph():
    g = {}

    lines = list(open('links-simple-sorted.txt'))

    for ln in lines:
        node = int(ln.split(':')[0])
        g[node] = []

    for i, ln in enumerate(lines):
        node = int(ln.split(':')[0])
        links = ln.split(':')[1]
        for link in links.strip().split():
            ilink = int(link)
            if ilink in g:
                g[node].append(int(link))

        if i % 1000 == 0:
            print i / float(len(lines))

    return g


def try_find_path(g, start, finish):
    costs = {start: 0}
    from_direction = {}
    visited = set()
    inf = float('inf')
    queue = set([start])

    while queue:
        here = min(queue, key=costs.get)
        queue.remove(here)
        visited.add(here)
        cost_to_neighbours = costs[next] + 1
        for neighbour in g[here]:
            current_cost = costs.get(neighbour, inf)
            if cost_to_neighbours < current_cost:
                costs[neighbour] = cost_to_neighbours
                from_direction[neighbour] = here
            if neighbour not in visited:
                queue.append(neighbour)

    if finish not in from_direction:
        raise ValueError('No route from {} to {}'.format(start, finish))

    path = [finish]
    here = finish
    while here != start:
        here = from_direction[here]
        path.append(here)
    return reversed(path)


if __name__ == '__main__':
    import cPickle as pickle
    try:
        g = pickle.load(open('graph.pck', 'rb'))
    except IOError:
        g = load_graph()
        with open('graph.pck', 'wb') as f:
            pickle.dump(g, 'graph.pck', -1)

    pages = list(g)
    print try_find_path(g, random.choice(pages), random.choice(pages))
