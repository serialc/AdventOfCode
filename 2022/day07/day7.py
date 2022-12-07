import numpy as np

class Dir:
    def __init__(self, name, parent):
        self.name = name
        self.dirs = {}
        self.files = {}
        self.parent = parent
        self.size = 0

    def addDir(self, name):
        self.dirs[name] = Dir(name, self)

    def addFile(self, size, name):
        self.files[name] = size

    def getParent(self):
        return self.parent

    def getChild(self, childname):
        return self.dirs[childname]

    def print(self, indent=''):
        print(indent + '- ' + self.name + ' (dir)')

        for k,v in self.dirs.items():
            v.print(indent + '  ')
        for k,v in self.files.items():
            print('  ' + indent + '- ' + k + '(file, size=' + str(v) + ')')

    def calcDirSizes(self):
        for k,v in self.dirs.items():
            self.size += v.calcDirSizes()
        for k,v in self.files.items():
            self.size += v
        return self.size

    def sumSmallDirs(self):
        sumsd = 0
        for k,v in self.dirs.items():
            sumsd += v.sumSmallDirs()
        if self.size < 100000:
            return self.size + sumsd
        return sumsd

    def findSmallestSuitable(self, min_size):
        if self.size < min_size:
            return None

        smallest_found = self.size
        for k,v in self.dirs.items():
            size = v.findSmallestSuitable(min_size)
            if size is not None and size < smallest_found:
                smallest_found = size

        return smallest_found

with open('input.txt', 'r') as fh:
#with open('test_input.txt', 'r') as fh:

    home = Dir('/', None)
    for line in fh:
        l = line.strip('\n')
        p = l.split(' ')

        if p[0] == '$':
            if p[1] == 'cd':
                if p[2] == '/':
                    curdir = home
                elif p[2] == '..':
                    curdir = curdir.getParent()
                else:
                    curdir = curdir.getChild(p[2])

            if p[1] == 'ls':
                # do nothing, we will read automatically if there's no $
                continue
        else:
            # read mode
            if p[0] == 'dir':
                curdir.addDir(p[1])
            else:
                curdir.addFile(int(p[0]), p[1])

# walk the tree and print its contents
home.print()

hdused = home.calcDirSizes()
print("HD space used: " + str(hdused))

small_dirs_sum = home.sumSmallDirs()

# Part 1
print("#### Part 1 ####")
print("Sum of under 100,000 size directories: " + str(small_dirs_sum))

################################ PART 2 ######################
print('################################ PART 2 ######################')

hdsize = 70000000
spcneeded = 30000000
spctofreeup = spcneeded - (hdsize - hdused)

print("We need to delete the smallest directory larger than " + str(spctofreeup))

smallest_suitable = home.findSmallestSuitable(spctofreeup)

# Part 2
print("#### Part 2 ####")
print("Size of directory to delete: " + str(smallest_suitable))
# First try: 30469934 - miscalculated how much space was needed
