
def load_graph():
    g = {}

    lines = list(open('links-simple-sorted.txt'))

    ints = {}

    def intint(x):
        x = int(x)
        return ints.setdefault(x, x)

    for ln in lines:
        node = intint(ln.split(':')[0])
        g[node] = []

    for i, ln in enumerate(lines):
        node = intint(ln.split(':')[0])
        links = ln.split(':')[1]
        for link in links.strip().split():
            ilink = intint(link)
            if ilink in g:
                g[node].append(ilink)

        if i % 1000 == 0:
            print i / float(len(lines))

    return g


def try_find_path(g, start, finish):
    inf = float('inf')
    costs = {k: inf for k in g}
    costs[start] = 0
    from_direction = {}
    queue = set([start])
    seen = set()
    cost = costs.get

    while queue:
        here = min(queue, key=cost)
        cost_to_neighbours = cost(here) + 1
        for neighbour in g[here]:
            if cost_to_neighbours < cost(neighbour):
                costs[neighbour] = cost_to_neighbours
                from_direction[neighbour] = here
            if neighbour == finish:
                break
            if neighbour not in seen:
                seen.add(neighbour)
                queue.add(neighbour)
        if len(queue) % 10 == 0:
            pct = len(seen) * 100.0 / len(g)
            print "%0.1f%%" % pct

    if finish not in from_direction:
        raise ValueError('No route from {} to {}'.format(start, finish))

    path = [finish]
    here = finish
    while here != start:
        here = from_direction[here]
        path.append(here)
    return reversed(path)


if __name__ == '__main__':
    title_map = {}
    title_map_r = {}
    print "Loading titles..."
    with open('titles.txt') as f:
        for i, ln in enumerate(f, start=1):
            title_map[ln.strip().lower()] = i
            title_map_r[i] = ln.strip()
    print "Loaded %d titles..." % len(title_map)

    print "Loading links..."
    import cPickle as pickle
    try:
        g = pickle.load(open('graph.pck', 'rb'))
    except IOError:
        g = load_graph()
        with open('graph.pck', 'wb') as f:
            pickle.dump(g, f, -1)

    while True:
        while True:
            start = raw_input('From> ')
            try:
                start = title_map[start.lower()]
            except KeyError:
                print "Invalid page"
                continue
            else:
                break
        while True:
            finish = raw_input('To> ')
            try:
                finish = title_map[finish.lower()]
            except KeyError:
                print "Invalid page"
                continue
            else:
                break

        path = try_find_path(g, start, finish)

        print 'Path:'
        for n in path:
            print title_map_r.get(n, n)
