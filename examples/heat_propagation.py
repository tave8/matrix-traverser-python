"""

The Problem
You have a matrix of temperatures. A traveler starts at S and wants to reach E.
S    6    2    1
5    5    3    2
4    4    4    3
3    2    1    E
The traveler moves one cell at a time to any adjacent cell.
The traveler has a tolerance — the maximum temperature difference they can handle in a single step. 
If the current cell is temperature 8 and tolerance is 3, they can only move to cells between temperature 5 and 11.

Here is the twist: the tolerance shrinks the further the traveler walks.
The traveler starts fresh and can handle larger temperature differences. As the journey gets longer, 
fatigue sets in and only smaller temperature differences are tolerable.

Does a path from S to E exist?
"""