# 2015 (done in August 2026)
## Highlights

![Santa's path](day03/day3_part1.png)
![Santa's and bot's path](day03/day3_part2.png)

<img src="day06/day6_anim.gif" title="Light show toggle" width="300"> <img src="day06/day6_part2.png" title="Light show brightness" width="300">

![Light show path](day18/no_corners.gif)
![Light show with corners on](day18/corners.gif)

### Comments

Day:

6. Managed to do it the hard way so that I can solve it in 3D later (2021).
   Integrated running tests into process.
19. Less fun. The concept is challenging but the data is nice so that the solution is actually trivial. Risk of overengineering.
21. A nice theme. Effort translated directly to progress.
24. When searching for combinations of numbers that sum to a specific value, sort from largest to smallest.

### Tags

Day:

1. character frequency count
2. basic arithmatic
3. surface, directions, numpy for image generation
4. hash function
5. string patterns/matching, probably should have used regex
6. regex, numpy, surface, list bound cutting
7. memoization, recursion, wires
8. arithmatic, encoding/decoding, devil in the details
9. recursion, travelling salesman problem, visit node in optimal sequence
10. recursion, string parsing
11. password odometer, character manipulation
12. json, recursion, parsing, types
13. recursion, bidirectional relations, round table
14. modulo, scoring, race
15. calories, equation, compromise
16. contents matching
17. combinations
18. cellular automata, lights, neighbourhood
19. string concatenations, permutations, recursion
20. permutations, factors, brute force
21. RPG, permutations
22. RPG, permutations
23. assembly, registers, turing tape
24. permutations
25. diagonal processing

### Errors that cost time

- Day 04: Matching two strings of different lengths: line[0:6] == "00000"
- Day 06: Focusing on wrong section of problem due to large data set - use smaller tests!
- Day 13: Used wrong list when retrieving indices. Took a while to find the problem
- Day 17: When doing combinations, remember that we need to sometimes do nothing for a recursion.
- Day 21: I kept using the same boss for every fight, his health was negative. Needed to pass a copy().
- Day 22: Edge cases killed me. 
- Day 24: Tried to solve too much, we don't care about the other bags, just looking for combinations equaling a weight.
- Day 25: Given index starts at 1, not 0!
