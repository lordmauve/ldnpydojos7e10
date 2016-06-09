def load_graph():
    g = {}

    lines = list(open('wikipedia.txt'))

    for ln in lines:
        node = int(ln.split(':')[0])
        g[node] = []

    for i, ln in enumerate(lines):
        node = int(ln.split(':')[0])
        links = ln.split(':')[1]
        for link in links.strip().split():
            g[node].append(int(link))

        if i % 1000 == 0:
            print i / float(len(lines))

    return g



def try_find_path(g, start, finish):
    paths = [[start]] 

    while True:
        newpaths = []
        for path in paths:
            end = path[-1]
            for ln in g[end]:
                if ln == finish:
                    return path + [finish]
                if ln not in path:
                    newpaths.append(path + [ln])

        paths = newpaths
        paths = paths[:10000]

        print len(paths[0])

    

g = load_graph()
print try_find_path(g, 4, 100)
