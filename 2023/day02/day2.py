from math import prod

input_file = 'input0'
input_file = 'input'

# if I have 12R, 13G, 14B, sum up game IDs of possible games
glim = rgbdice = {"red": 12, "green": 13, "blue": 14}

results = []
game_dice = {}
with open(input_file, 'r') as fh:
    for l in fh:
        l = l.strip('\n')

        # get the id and games
        gid, rounds = l.split(':')
        gid = int(gid.split(' ')[1])
        rounds = rounds.split(';')

        game_dice[gid] = {"red": 0, "green": 0, "blue": 0}
        for r in rounds:
            # get the count of each dice color for each round
            col_dice = r.lstrip().split(', ')
            for one_col in col_dice:
                dcount, dcol = one_col.split(' ')
                if game_dice[gid][dcol] < int(dcount):
                    game_dice[gid][dcol] = int(dcount)
            # end of round

        # check that the coloured dice count doesn't exceed the limit
        if  glim['red']   >= game_dice[gid]['red'] and \
            glim['green'] >= game_dice[gid]['green'] and \
            glim['blue']  >= game_dice[gid]['blue']:
            results.append(gid)
        # end of this game

print("#### Part 1 ####")
print("Answer is:", str(sum(results)))

#### PART 2 ####
print("============ Part 2 start ================")

print(game_dice)
power_sum = 0
for game in game_dice.values():
    game_prod = prod(game.values())
    power_sum += game_prod

print("#### Part 2 ####")
print("Answer is:", power_sum)
