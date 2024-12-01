# 2021

## Highlights
![Possible probe trajectories for target area](day17/probe_paths.png "Possible probe trajectories for target area")

![Path through low-ceiling cave](day15/cave_risk_test_input.png "Path through low-ceiling cave")

![Path through low-ceiling cave](day15/cave_risk_input.png "Path through low-ceiling cave")

<img src="day05/seafloor.png" width="25%" height="25%" title="Good luck crossing the vents on the seafloor">

![Dumbo octopuses flashing](day11/octopus.gif "Dumbo octopuses flashing")

![Ridges and vents on the seafloor](day09/ridges_seafloor.png "Ridges and vents on the seafloor")

Matrix folding of transparent sheet to produce the following:
```
.##....##..##..#..#.###...##..###..###..
#..#....#.#..#.#.#..#..#.#..#.#..#.#..#.
#.......#.#....##...###..#..#.#..#.###..
#.......#.#....#.#..#..#.####.###..#..#.
#..#.#..#.#..#.#.#..#..#.#..#.#....#..#.
.##...##...##..#..#.###..#..#.#....###..
```

## Comments

* Day 05: There must be an easier way to determine coordinates between two diagonal points.
* Day 06: First part is programmed simply conceptually but is inefficient - particular given that it's modeling exponential growth. Need to consider computational efficiency from the start next time.
* Day 07: Need to consider the statistical properties of distributions and what's being asked rather than reimplement existing operations (i.e., mean and median).
* Day 08: What a beast. A bloated beast of nested loops trying to create the logic equivalent of solving a sodoku.
* Day 09: Over-engineered.
* Day 12: Bind bending at first - recursion usually is.
* Day 13: Bug in input I believe - asymmetric fold.
* Day 14: Required alternative thinking, flipping the task backwards. Building a dict of all possibilities back up. Then selecting the appropriate items. Also, I need to be more careful when using lists as they pass by reference and not value.
* Day 16: Quite a nice recursive calculator. Too much reading to figure out the requirements.

## Tricky problems

* Day 08: A grind, but not as hard as Day 14. 
* Day 14: Need to carefully work the problem out from the reverse direction.
* Day 15: Careful, your path doesn't go only down and right.
* Day 18: Tried to use recursion. That failed. Restarted but with a tree. Better but painful.

## Tags
Concepts used or required to solve the challenges:

Day:

1. diff, lag, filter
2. path finding
3. recursion, matrices
4. classes, matrices
5. mapping, matrices
6. efficiency
7. statistics
8. logic, sodoku-solving-like, classes
9. cellular automata, matrices
10. stack
11. cellular automata, matrices
12. recursion
13. matrices, folding
14. optimization, efficiency
15. mapping, matrices, routing efficiency
16. RTFM, recursion
17. geometry, trajectory
18. tree, classes
19. 3D rotation, matrices
20. matrices, filter, binary, cellular automata
