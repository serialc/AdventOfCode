# 2025
## Highlights

Day 4:

![Clearing the warehouse of paper rolls](day04/day04.gif)

Day 7:
![Flow of light](day07/pixel_density.png)

### Comments

Day:

1. Safe-dial null position counts.
2. Should have used regex, but did it manually.
3. Serial battery linkages for max jolts. Combinatorials?
4. Looking at neighbourhoods on a surface
 - To make the animated gif `convert -delay 0.2 -loop 0 *.png day04.gif`
5. Counting overlapping set contents.
6. Working with numbers in tabular format rather than as expected.
7. The splitting of light down the surface.

### Tags

Day:

1. rotation, modulo
2. regex, 
3. recursion
4. grid neighbourhood, surface
5. sets, dictionary, limits, overlapping
6. numpy, table, manual number assembly
7. numpy, surface, fractal sum

### Errors that cost time

- Used a raw value rather than the modulo/remainder (Day 1)
- I used an equality by accident when I wanted to do an assignment (Day 4)
- I used a dict but overwrote values, lost duplicates that I needed (Day 5)
- Assumptions about regular column spacing were not checked (Day 6)
- Writing multi-digit numbers to a character matrix is bad, "10" becomes "1" (Day 7)
