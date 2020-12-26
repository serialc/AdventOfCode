# AoC2020
My Advent of Code 2020 solutions

## Highlights
![A hexagonal cellular automata](/day24/tiles_anim.gif "A hexagonal cellular automata")
![Sea Monster Map](/day20/seamonsters.png "Sea Monster map")

## Comments
They're not all necessarily efficient solutions.

The trickiest days/problems for me were based on efficiency problems. While I could solve the test sets, the problem set took too long to run:

* Day 25: Cracking encryption - Needed to populate array once with sequential transforms once rather than testing possible loop values against public key.
* Day 23: Cups reorganization - Rather than use an array and making changes, I needed to use a linked-list data structure comprised of(a hash/dict that simply pointed to next cup. Each turn then only had a remove and insert update rather than searching and updating the array.
