Project 2 Floodit

My first attempt of the flood funcion was a simple BFS algorithm which searches all 
adjacent tiles to those already in the flooded list. If the tile was the color I was looking for,
and if it wasn't already on the list,I added it to the list and continued the search until I've 
seen all elements in the list.

However, this approach involved a linear search each time I looked at a tile to check if it was
in the list or not. Thus, I needed a way to cut this time down. 

In flood2, I turned the list into a set, therefore I could have constant time in making my check and 
reducing O(flood) by a factor of n.

The graphs of each function are given in an excel file named ResponseGraph.xlsx
It appears that the firstion function is quadradic while the new is linear. 

This makes sense as the old function included two linear searches, nested, while the new only 
has one linear search
