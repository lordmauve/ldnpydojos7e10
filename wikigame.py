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



    

if __name__ == '__main__':
    import sys
    
    title_map = {}
    title_map_r = {}
    with open('titles.txt') as f:
        for i, ln in enumerate(f):
            title_map[ln.strip().lower()] = i + 1
            title_map_r[i + 1] = ln.strip()

    start = sys.argv[1]
    finish = sys.argv[2]

    start = title_map[start.lower()]
    finish = title_map[finish.lower()]

    g = load_graph()
    path = try_find_path(g, start, finish)

    print 'Path:'
    for n in path:
        print title_map.get(n, n)
