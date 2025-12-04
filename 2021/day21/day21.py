import numpy as np

# inputs
spos = [4, 8]
spos = [7, 10]

# Part 1 #######
pos = spos.copy()
sc = [0, 0]
rpt = 3
rollcount = 0
pturn = 0

die = 1
rollcount = 0


def rollD100():
    global die
    global rollcount

    rval = die
    die += 1
    if die > 100:
        die = 1

    rollcount += 1

    return rval


while True:
    # print("Player", pturn + 1, end="")
    roll = rollD100() + rollD100() + rollD100()
    # print(" Rolled", roll, end="")
    pos[pturn] = pos[pturn] + roll
    pos[pturn] %= 10
    # print(" New pos", pos[pturn], end="")
    if pos[pturn] == 0:
        sc[pturn] += 10
    else:
        sc[pturn] += pos[pturn]
    # print(" and score:", sc[pturn])

    # determine next player - alternate
    if pturn == 0:
        pturn = 1
    else:
        pturn = 0

    # check if end of game
    if sc[0] >= 1000 or sc[1] >= 1000:
        break

print("Rolls", rollcount)
print("Scores: p1 p2", sc)

if sc[0] > sc[1]:
    print("Player 1 won")
    print("Part 1 answer is", sc[1] * rollcount)
else:
    print("Player 2 won")
    print("Part 1 answer is", sc[0] * rollcount)

############### Part 2 ################
print("\nPART 2")

game_end_score = 21
pos = spos.copy()

# so one player's turn will spawn 27 universes (3 * 3 * 3)
# with dice sums equal to
# 3,4,5,6,7,8,9
# 1,3,6,7,6,3,1 <- distributions

roll = np.array([3, 4, 5, 6, 7, 8, 9], dtype=int)
dist = np.array([1, 3, 6, 7, 6, 3, 1], dtype=int)


def playTurn(state, games_played, scores, player):

    global game_wins

    # print("state", state, "scores", scores)

    # for each possible roll calculate the updated scores
    # print(roll)
    for i in range(len(roll)):
        # print(i,"Three roll sum", roll[i], "frequency", dist[i])
        new_state = state.copy()
        new_scores = scores.copy()

        played_games = dist[i] * games_played
        new_state[player] = roll[i] + state[player]

        # reduce to 0-9 if 10 and over
        # we set those at 10 to 0 but it's fine
        new_state[player] %= 10

        # get the updated score for this set of games
        if new_state[player] == 0:
            new_scores[player] += +10
        else:
            new_scores[player] += new_state[player]

        # determine if this player has won
        if new_scores[player] > 20:
            game_wins[player] += played_games
            # print("Player", player, "won", played_games)
            # continue to next game
            continue

        # determine next player - alternate
        next_player = 0
        if player == 0:
            next_player = 1

        # (state, played_games, scores, next_player)
        playTurn(new_state.copy(), played_games, new_scores.copy(), next_player)


game_wins = [0, 0]

# playTurn(state, played_games, scores, next_player)
playTurn(pos, 1, [0, 0], 0)

print("How many wins does the player with the most wins have?")
print(game_wins)
