import numpy as np

# load map
map = np.loadtxt('input.txt', str, comments='%')
mw = len(map[0])
mh = len(map)

def slide(slope):
    global map
    loc = {"x": 0, "y": 0}
    tree_hits = 0

    while loc['y'] != (mh - 1):
        #print(loc['x'], loc['y'])
        # move
        loc['x'] += slope['x']
        loc['y'] += slope['y']

        # adjust if we went off the map
        loc['x'] %= mw
        #print(loc['x'], loc['y'])

        #print(map[loc['y']][loc['x']])
        if map[loc['y']][loc['x']] == '#':
            tree_hits += 1

    return tree_hits

hits_a = slide({"x": 1, "y": 1})
hits_b = slide({"x": 3, "y": 1})
hits_c = slide({"x": 5, "y": 1})
hits_d = slide({"x": 7, "y": 1})
hits_e = slide({"x": 1, "y": 2})

print("Trees hit: " + str(hits_a))
print("Trees hit: " + str(hits_b))
print("Trees hit: " + str(hits_c))
print("Trees hit: " + str(hits_d))
print("Trees hit: " + str(hits_e))

print("Product: " + str(hits_a * hits_b * hits_c * hits_d * hits_e))
