# 2025
## Highlights

Day 4:

![Clearing the warehouse of paper rolls](day04/day04.gif)

Day 7:

<img src="day07/pixel_density.png" title="Flow of light">

### Comments

Day:

1. Safe-dial null position counts.
2. Should have used regex, but did it manually.
3. Serial battery linkages for max jolts. Combinatorials?
4. Looking at neighbourhoods on a surface
5. Counting overlapping set contents.
6. Working with numbers in tabular format rather than as expected.
7. The splitting of light down the surface.
8. Creating shortest path network in 3D space
9. Connecting nodes on plane - looking for largest rectangle

### Tags

Day:

1. rotation, modulo
2. regex, 
3. recursion
4. grid neighbourhood, surface
5. sets, dictionary, limits, overlapping
6. numpy, table, manual number assembly
7. numpy, surface, fractal sum
8. numpy, 3D, pythagorus, network
9. numpy, position ranking, surface

### Errors that cost time

- Used a raw value rather than the modulo/remainder (Day 1)
- I used an equality by accident when I wanted to do an assignment (Day 4)
- I used a dict but overwrote values, lost duplicates that I needed (Day 5)
- Assumptions about regular column spacing were not checked (Day 6)
- Writing multi-digit numbers to a character matrix is bad, "10" becomes "1" (Day 7)
- Operating on a very large surface wasn't possible. There were large gaps. Converted postions to ranked positions as suggested on Reddit. (Day 9)
