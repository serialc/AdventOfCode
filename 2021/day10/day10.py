inputf = 'test_input'
inputf = 'input'

bmatch = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">"
    }

points = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137
    }

cpoints = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4,
    }

tpoints = 0
scores = []

def processBrackets(bline):
    global tpoints

    stack = []
    for b in bline:
        if b in bmatch:
            stack.append(b)
        else:
            # it's a closing bracket
            last = stack.pop()
            if b != bmatch[last]:
                #print("Expected ", bmatch[last], "not", b)
                tpoints += points[b]
                #line fails
                return

    # unstack
    score = 0
    while len(stack) != 0:
        b = stack.pop()
        score = score * 5 + cpoints[bmatch[b]]
    scores.append(score)


### Read input data
with open(inputf, 'r') as fh:
    for line in fh:
        line = line.strip()
        b = list(line)
        processBrackets(b)


### Part 1
print("Part1")
print(tpoints)

### Part 2
print("Part2")
print(sorted(scores)[int(len(scores)/2)])
