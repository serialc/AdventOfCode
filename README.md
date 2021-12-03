# Advent of Code
My [Advent of Code](https://adventofcode.com/) solutions

Starting a new year? Create all the directories for each day with `mkdir day{01..25}`.

## 2021
### Highlights

### Comments

### Tags
I note some consepts that are required to solve the chalenges for each day.
If I need to reapply I can find code bits.

Day:

1. diff, lag, filter
2. path\_finding
3. recursion, matrices

## 2020
### Highlights
![A hexagonal cellular automata](2020/day24/tiles_anim.gif "A hexagonal cellular automata")
![Sea Monster Map](2020/day20/seamonsters.png "Sea Monster map")

### Comments
They're not all necessarily efficient solutions.

The trickiest days/problems for me were based on efficiency problems. While I could solve the test sets, the problem set took too long to run:

* Day 25: Cracking encryption - Needed to populate array once with sequential transforms once rather than testing possible loop values against public key.
* Day 23: Cups reorganization - Rather than use an array and making changes, I needed to use a linked-list data structure comprised of a hash/dict that simply pointed to next cup. Each turn then only had a remove and insert update rather than searching and updating the array.
* Day 19: Missed logic catch - Detected junk at the end of a string but counting logic flow didn't catch it. Took a long time to find error. 
