
# F -> 0
# B -> 127

# L -> 0
# R -> 7

seats = [ [0]*8 for i in range(128)]
highest_id = 0

with open('input.txt', 'r') as fh:
    for line in fh:

        line = line.rstrip()
        brow = line[0:7].replace('F', '0').replace('B', '1')
        bcol = line[7:].replace('L', '0').replace('R', '1')
        rowint = int(brow, 2)
        colint = int(bcol, 2)
        #print(line)
        #print(rowint)
        #print(colint)
        
        row = 0
        col = 0
        

        # convert seat location to ID
        sid = rowint * 8 + colint
        
        seats[rowint][colint] = sid
        if sid > highest_id:
            highest_id = sid

# done
print("Part 1")
print("Hightest id found is: " + str(highest_id))

print("Part 2")
search_state = 0
for row in range(len(seats)):

    print(seats[row])

    if 0 in seats[row] and search_state < 2:
        for col in range(len(seats[row])):
            if seats[row][col] == 0: 
                if search_state == 1:
                    print("*** Col and row: ", row, col)
                    print("*** Seat id: " + str(row * 8 + col))
                    search_state = 2
                    break
            else:
                search_state = 1

#print(seats)
