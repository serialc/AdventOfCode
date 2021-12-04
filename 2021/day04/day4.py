import numpy as np

input_file = 'test_input'
input_file = 'input'

class Board:
    dim = [5,5]

    _last_found = -1;
    _finished = False;

    def __init__(self, matrix):
        # numbers
        self.nboard = np.array(matrix, dtype=int)
        # found
        self.fboard = np.zeros(self.dim, dtype=int)

    def sum(self):
        return np.sum(self.nbourd[self.fboard == 1])

    def found(self, value):
        if not self._finished:
            self._last_found = int(value)
            self.fboard[self.nboard == value] = 1

    def already_won(self):
        return self._finished

    def bingo_check(self):
        # check columns
        if np.any(self.fboard.sum(axis=0) == self.dim[0]):
            self._finished = True
            return True

        if np.any(self.fboard.sum(axis=1) == self.dim[1]):
            self._finished = True
            return True
        return False

    def get_score(self):
        return np.sum(self.nboard[self.fboard == 0]) * self._last_found

    def finished(self):
        return self._finished

    def print(self):
        print(self.nboard)

# load data
q = False
state = 0
tboard = []
boards = []
with open(input_file, 'r') as fh:
    for line in fh:
        # clean it
        line = line.strip().lstrip();
        if line == "":
            continue
        
        if q == False:
            q = [int(v) for v in line.split(',')]
            continue

        tboard.append(line.split())

        if len(tboard) == 5:
            boards.append(Board(tboard))
            tboard = []


#print(q)
#[b.print() for b in boards]

        
#### Part 1

# play the game
def playBingo():
    for num in q:
        # call the number, each board checks if they have it
        [b.found(num) for b in boards]

        # every board checks if it has bingo
        for b in boards:
            if b.bingo_check():
                return b

winner = playBingo()

print("Part 1 answer is: ")
print(winner.get_score())

#### Part 2
print("======== Part 2 ===========")

# play the game
def playLoserBingo():
    latest_winner = False
    for num in q:
        # call the number, each board checks if they have it
        [b.found(num) for b in boards]

        # every board checks if it has bingo
        for b in boards:
            if not b.already_won() and b.bingo_check():
                latest_winner = b

        if sum([b.finished() for b in boards]) == len(boards):
            return latest_winner

last_winner = playLoserBingo()

print("Part 2 answer is: ")
print(last_winner.get_score())
