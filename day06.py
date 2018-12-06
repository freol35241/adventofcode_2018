"""
--- Day 6: Chronal Coordinates ---
The device on your wrist beeps several times, and once again you feel like you're falling.

"Situation critical," the device announces. "Destination indeterminate. Chronal interference detected. Please specify new target coordinates."

The device then produces a list of coordinates (your puzzle input). Are they places it thinks are safe or dangerous? It recommends you check manual page 729. The Elves did not give you a manual.

If they're dangerous, maybe you can minimize the danger by finding the coordinate that gives the largest distance from the other points.

Using only the Manhattan distance, determine the area around each coordinate by counting the number of integer X,Y locations that are closest to that coordinate (and aren't tied in distance to any other coordinate).

Your goal is to find the size of the largest area that isn't infinite. For example, consider the following list of coordinates:

1, 1
1, 6
8, 3
3, 4
5, 5
8, 9
If we name these coordinates A through F, we can draw them on a grid, putting 0,0 at the top left:

..........
.A........
..........
........C.
...D......
.....E....
.B........
..........
..........
........F.
This view is partial - the actual grid extends infinitely in all directions. Using the Manhattan distance, each location's closest coordinate can be determined, shown here in lowercase:

aaaaa.cccc
aAaaa.cccc
aaaddecccc
aadddeccCc
..dDdeeccc
bb.deEeecc
bBb.eeee..
bbb.eeefff
bbb.eeffff
bbb.ffffFf
Locations shown as . are equally far from two or more coordinates, and so they don't count as being closest to any.

In this example, the areas of coordinates A, B, C, and F are infinite - while not shown here, their areas extend forever outside the visible grid. However, the areas of coordinates D and E are finite: D is closest to 9 locations, and E is closest to 17 (both including the coordinate's location itself). Therefore, in this example, the size of the largest area is 17.

What is the size of the largest area that isn't infinite?
"""

data = """262, 196
110, 109
58, 188
226, 339
304, 83
136, 356
257, 50
315, 148
47, 315
73, 130
136, 91
341, 169
334, 346
285, 248
76, 233
334, 64
106, 326
48, 207
64, 65
189, 183
300, 247
352, 279
338, 287
77, 277
220, 152
77, 295
49, 81
236, 294
321, 192
43, 234
180, 69
130, 122
166, 225
301, 290
49, 176
62, 156
346, 55
150, 138
214, 245
272, 241
50, 283
104, 70
215, 184
339, 318
175, 123
250, 100
134, 227
96, 197
312, 174
133, 237"""

import numpy as np
from scipy.spatial.distance import cityblock

data = data.splitlines()
ixs = []
for row in data:
    row = row.split(', ')
    ixs.append([int(row[0]), int(row[1])])

ixs = np.array(ixs)

max_x = max(ixs[:,0]) + 1
max_y = max(ixs[:,1]) + 1

number_of_blocks = np.zeros(len(ixs))

for i_x in range(max_x):
    for i_y in range(max_y):
        distances = []
        for ix in ixs:
            dist = cityblock(ix, [i_x, i_y])
            distances.append(dist)

        min_dist = min(distances)
        indices = np.array(distances) == min_dist

        indices = indices.astype('float64')

        if np.sum(indices) > 1:
            continue

        if i_x == max_x-1 or i_x == 0 or i_y == 0 or i_y == max_y-1:
            indices = indices * max_x*max_y


        number_of_blocks += indices


number_of_blocks[number_of_blocks>max_x*max_y] = 0

print(max(number_of_blocks))

"""
--- Part Two ---
On the other hand, if the coordinates are safe, maybe the best you can do is try to find a region near as many coordinates as possible.

For example, suppose you want the sum of the Manhattan distance to all of the coordinates to be less than 32. For each location, add up the distances to all of the given coordinates; if the total of those distances is less than 32, that location is within the desired region. Using the same coordinates as above, the resulting region looks like this:

..........
.A........
..........
...###..C.
..#D###...
..###E#...
.B.###....
..........
..........
........F.
In particular, consider the highlighted location 4,3 located at the top middle of the region. Its calculation is as follows, where abs() is the absolute value function:

Distance to coordinate A: abs(4-1) + abs(3-1) =  5
Distance to coordinate B: abs(4-1) + abs(3-6) =  6
Distance to coordinate C: abs(4-8) + abs(3-3) =  4
Distance to coordinate D: abs(4-3) + abs(3-4) =  2
Distance to coordinate E: abs(4-5) + abs(3-5) =  3
Distance to coordinate F: abs(4-8) + abs(3-9) = 10
Total distance: 5 + 6 + 4 + 2 + 3 + 10 = 30
Because the total distance to all coordinates (30) is less than 32, the location is within the region.

This region, which also includes coordinates D and E, has a total size of 16.

Your actual region will need to be much larger than this example, though, instead including all locations with a total distance of less than 10000.

What is the size of the region containing all locations which have a total distance to all given coordinates of less than 10000?
"""

region = np.zeros((max_x, max_y))

for i_x in range(max_x):
    for i_y in range(max_y):
        distances = []
        for ix in ixs:
            dist = cityblock(ix, [i_x, i_y])
            distances.append(dist)

        tot_dist = sum(distances)

        if tot_dist < 10000:
            region[i_x, i_y] = 1



print(np.sum(region))
        