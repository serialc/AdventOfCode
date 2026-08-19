# Advent of Code
My [Advent of Code](https://adventofcode.com/) solutions

[2020](/2020)
[2021](/2021)
[2022](/2022)
[2023](/2023)
[2024](/2024)
[2025](/2025)

## Highlights

### 2015 (in August 2026)

![Santa's path](2015/day03/day3_part1.png)

![Santa's and bot's path](2015/day03/day3_part2.png)


### 2025
![Clearing the warehouse of paper rolls](2025/day04/day04.gif)

<img src="2025/day07/pixel_density.png" title="Flow of light">

### 2023
![Follow the pipe](2023/day10/day10.gif)

### 2021
![Possible probe trajectories for target area](2021/day17/probe_paths.png "Possible probe trajectories for target area")

![Path through low-ceiling cave](2021/day15/cave_risk_test_input.png "Path through low-ceiling cave")

![Path through low-ceiling cave](2021/day15/cave_risk_input.png "Path through low-ceiling cave")

<img src="2021/day05/seafloor.png" width="25%" height="25%" title="Good luck crossing the vents on the seafloor">

![Dumbo octopuses flashing](2021/day11/octopus.gif "Dumbo octopuses flashing")

![Ridges and vents on the seafloor](2021/day09/ridges_seafloor.png "Ridges and vents on the seafloor")

### 2020
![A hexagonal cellular automata](2020/day24/tiles_anim.gif "A hexagonal cellular automata")
![Sea Monster Map](2020/day20/seamonsters.png "Sea Monster map")


## Tips for me

### Create animated gifs
Use terminal:

    convert -delay 10 -loop 0 *.png anim.gif

The 0 means infinite.

### Create all my day folders

Starting a new year?  
Create all the directories for each day with:

    mkdir day{01..25}

### Using VE

Using virtual environment and package now:

Create the VE:

    python -m venv venv

Activate VE: 

    . venv/bin/activate

Install local and active project:

    pip install -e . (path to package to install)

I will likely need install other dependencies that are not present in VE:

    pip install numpy

Deactivate VE:

    deactivate
