import os, string, sys

import copy
from collections import deque
from Queue import *
from itertools import *
from copy import *

# appends padding spaces if the number is smaller than the largest value
# e.g. if the largest val=1245, 1 will be represented as '1   '
def format_num(n, maxSpaces):
    strNum = str(n)
    return strNum + ' ' * (maxSpaces - len(strNum))

# Just a wrapper over python dict to preserve things
# like height, width; also a pretty printing function provided
class Grid:
    def __init__(self, w, h, d):
        self.width = w
        self.height = h
        self.d = d
    
    # pretty print the grid using the number formatter
    def pretty_print_grid(self):
        nSpaces = len(str(max(self.d.values())))
        strDelim = '|' + ('-' + (nSpaces * ' ')) * self.width + '|'
        print strDelim
        for x in range(self.width):
            print '|' + ' '.join([format_num(self.d[(x, y)], nSpaces) for y in range(self.height)]) + '|'
        print strDelim

# The grid is basically a dictionary. We can treat this as a graph where each node has 4 neighbors.
# Each neighbor contributes an in-edge as well as an out-edge.
# You might want to use this to construct you solution
class Graph:
    def __init__(self, grid):
        self.grid = grid
    
    def vertices(self):
        return self.grid.d.keys()
    
    def adj(self, (x, y)):
        return [u for u in [(x+1, y), (x-1, y), (x, y+1), (x, y-1)] if u in self.grid.d.keys()]
    
    # put the value val for vertex u
    def putVal(self, u, val):
        self.grid.d[u] = val
    
    def getVal(self, u):
        return self.grid.d[u]


#defines a search node class which represents a vertex and the total distance travelled so far
class searchNode:
    def __init__(self, vertex, parent_node = None, cost = 0):
        self.vertex = vertex
        self.parent = parent_node
        self.cost = cost

    def path(self):
        l = list()
        l.append(self.vertex)
        cost = 0
        parent = self.parent
        while parent:
            l.append(parent.vertex)
            cost += 1
            parent = parent.parent

        return (cost, l)
        


#measure of manhattan distance between two points
def manhattan(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


# Takes the grid and the points as arguments and returns a list of paths
# The grid represents the entire chip
# Each path represents the wire used to connect components represented by points
# Each path connects a pair of points in the points array; avoiding obstacles and other paths
# while minimizing the total path length required to connect all points
# If the points cannot be connected the function returns None
def find_paths(grid, points):
    graph = Graph(grid)
    sorted_points = list()
    #add a measure of distance to each pair of points
    for pair in points:
        sorted_points.append( (manhattan(pair[0], pair[1]), pair[0], pair[1]) )
    #sort points on this distance
    sorted_points.sort()

    #permute all possible orderings
    permutation = list(permutations(sorted_points))
    best_score = float("+infinity")
    best_paths = None

    
    for order in permutation:
        new = copy(graph)
        current_score = 0
        current_paths = list()
        for wire in order:
            #BFS on current wire. Looks at length of optimal solution
            info = BFS(new, wire[1], wire[2])

            if info == None:
                break
            else:
                current_score += info[0]
                current_paths.append(info[1])
                #add wire to graph
                for point in info[1]:
                    new.putVal(point, -1)
                    
        if current_score < best_score:
            best_score = current_score
            best_paths = current_paths
            
    return best_paths

            
    
 
    
def BFS(graph, start, goal):
    #initialize objects
    explored = set()
    frontier = Queue()
    frontier_states = set()
    initial_node = searchNode(start)
    frontier.put(initial_node)
    frontier_states.add(start)

    #search until exhausted all possible paths
    while not frontier.empty():

        #add new node to explored
        node = frontier.get()
        frontier_states.remove(node.vertex)
        explored.add(node.vertex)
        
        #check if path is complete
        if node.vertex == goal:
            return node.path()
            
        #if goal not found, continue search
        else:
            #generate children
            for vertex in graph.adj(node.vertex):
                #if the vertex is both new and not an obstacle
                if not vertex in explored and not vertex in frontier_states and graph.getVal(vertex) == 0 or vertex == goal:
                    child = searchNode(vertex, node, node.cost + 1)
                    frontier.put(child)
                    frontier_states.add(vertex)
            
    return None
                    

        
            
        

# check that the paths do not cross each other, or the obstacles; returns False if any path does so
def check_correctness(paths, obstacles):
    s = set()
    for path in paths:
        for (x, y) in path:
            if (x, y) in s: return False
            for o in obstacles:
                if (o[0] <= x <= o[2]) and (o[1] <= y <= o[3]):
                    return False
            s.add((x, y))
    return True

def main():
    # read all the chip related info from the input file
    with open(sys.argv[1]) as f:
        # first two lines are grid width and height
        w = int(f.readline()); h = int(f.readline())
        
        # third line is the number of obstacles; following numObst lines are the obstacle co-ordinates
        numObst = int(f.readline())
        obstacles = []
        for n in range(numObst):
            line = f.readline()
            obstacles.append([int(x) for x in line.split()])
        
        # read the number of points and their co-ordinates
        numPoints = int(f.readline())
        points = []
        for n in range(numPoints):
            line = f.readline()
            pts = [int(x) for x in line.split()]
            points.append(((pts[0], pts[1]), (pts[2], pts[3])))
    grid = dict(((x, y), 0) for x in range(w) for y in range(h))
    # lay out the obstacles
    for o in obstacles:
        for x in range(o[0], o[2] + 1):
            for y in range(o[1], o[3] + 1):
                grid[(x, y)] = -1
    
    cnt = 1 # route count
    for (s, d) in points:
        grid[s] = cnt; grid[d] = cnt
        cnt += 1
    
    numPaths = cnt - 1
    g = Grid(w, h, grid)
        
#     g.pretty_print_grid()

    paths = find_paths(g, points)
    if paths is None:
        print "Cannot connect all the points!"
    else:
        # check the correctness
        if not check_correctness(paths, obstacles):
            raise ("Incorrect solution, some path cross each other or the obstacles!")
        print "Paths:"
        totLength = 0
        for p in paths:
            print p
            totLength += len(p)
        print "Total Length: " + str(totLength)
    
if __name__ == "__main__":
    main()

