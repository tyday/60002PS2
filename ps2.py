# 6.0002 Problem Set 5
# Graph optimization
# Name:
# Collaborators:
# Time:

#
# Finding shortest paths through MIT buildings
#
import unittest
from graph import Digraph, Node, WeightedEdge

#
# Problem 2: Building up the Campus Map
#
# Problem 2a: Designing your graph
#
# What do the graph's nodes represent in this problem? What
# do the graph's edges represent? Where are the distances
# represented?
#
# Answer:
#


# Problem 2b: Implementing load_map
def load_map(map_filename):
    """
    Parses the map file and constructs a directed graph

    Parameters:
        map_filename : name of the map file

    Assumes:
        Each entry in the map file consists of the following four positive
        integers, separated by a blank space:
            From To TotalDistance DistanceOutdoors
        e.g.
            32 76 54 23
        This entry would become an edge from 32 to 76.

    Returns:
        a Digraph representing the map
    """
    g = Digraph()

    # TODO
    with open(map_filename) as f:
        mapdata = f.readlines()
    f.closed
    for line in mapdata:
        a,b,c,d = line.split()
        if a not in g.edges:
            g.add_node(a)
        if b not in g.edges:
            g.add_node(b)
        newE = WeightedEdge(a,b,c,d)
        g.add_edge(newE)
        

    print("Loading map from file...")
    return(g)



# Problem 2c: Testing load_map
# Include the lines used to test load_map below, but comment them out
# print(load_map('test_load_map.txt'))

#
# Problem 3: Finding the Shorest Path using Optimized Search Method
#
# Problem 3a: Objective function
#
# What is the objective function for this problem? What are the constraints?
#
# Answer:
#

# Problem 3b: Implement get_best_path
def get_best_path(digraph, start, end, path, max_dist_outdoors, best_dist,
                  best_path):
    """
    Finds the shortest path between buildings subject to constraints.

    Parameters:
        digraph: Digraph instance
            The graph on which to carry out the search
        start: string
            Building number at which to start
        end: string
            Building number at which to end
        path: list composed of [[list of strings], int, int]
            Represents the current path of nodes being traversed. Contains
            a list of node names, total distance traveled, and total
            distance outdoors.
        max_dist_outdoors: int
            Maximum distance spent outdoors on a path
        best_dist: int
            The smallest distance between the original start and end node
            for the initial problem that you are trying to solve
        best_path: list of strings
            The shortest path found so far between the original start
            and end node.

    Returns:
        A tuple with the shortest-path from start to end, represented by
        a list of building numbers (in strings), [n_1, n_2, ..., n_k],
        where there exists an edge from n_i to n_(i+1) in digraph,
        for all 1 <= i < k and the distance of that path.

        If there exists no path that satisfies max_total_dist and
        max_dist_outdoors constraints, then return None.
    """
    pathlist, incDist,incOut = path
    pathlist = pathlist + [start]
    path = pathlist,incDist,incOut
    #print('Current DFS path:', path)
    if start == end:
        return pathlist,0,0
    for node in digraph.get_edges_for_node(start):
        if node.get_destination() not in pathlist: #avoid cycles
            if best_dist== None or incDist < best_dist: #len(path) < len(best_path):
                newPath, newDistance, newOutdoor = get_best_path(digraph,node.get_destination() , end, path, max_dist_outdoors,best_dist, best_path)
                if newDistance != None:
                    newDistance = newDistance + int(node.get_total_distance())
                    newOutdoor = newOutdoor + int(node.get_outdoor_distance())
                elif newDistance == None:
                    newDistance = int(node.get_total_distance())
                    newOutdoor = int(node.get_outdoor_distance())
                if newPath != None:
                    if best_dist == None: #or newDistance < best_dist:
                        if newOutdoor <= max_dist_outdoors:
                            best_path = newPath 
                            best_dist = newDistance
                            incOut = newOutdoor
                    elif newDistance <= best_dist and newOutdoor <= max_dist_outdoors:
                        best_path = newPath 
                        best_dist = newDistance
                        incOut = newOutdoor
    return best_path, best_dist, incOut
    
# g = load_map('test_load_map.txt')
# path_tuple = ([],0,0)
# print(get_best_path(g,g.getNode('a'),g.getNode('d'),path_tuple,0,None,None))


# Problem 3c: Implement directed_dfs
def directed_dfs(digraph, start, end, max_total_dist, max_dist_outdoors):
    """
    Finds the shortest path from start to end using a directed depth-first
    search. The total distance traveled on the path must not
    exceed max_total_dist, and the distance spent outdoors on this path must
    not exceed max_dist_outdoors.

    Parameters:
        digraph: Digraph instance
            The graph on which to carry out the search
        start: string
            Building number at which to start
        end: string
            Building number at which to end
        max_total_dist: int
            Maximum total distance on a path
        max_dist_outdoors: int
            Maximum distance spent outdoors on a path

    Returns:
        The shortest-path from start to end, represented by
        a list of building numbers (in strings), [n_1, n_2, ..., n_k],
        where there exists an edge from n_i to n_(i+1) in digraph,
        for all 1 <= i < k

        If there exists no path that satisfies max_total_dist and
        max_dist_outdoors constraints, then raises a ValueError.
    """
    # TODO
    path_tuple = ([],0,0)
    returnpath = get_best_path(digraph, digraph.getNode(start), digraph.getNode(end), path_tuple, max_dist_outdoors,None,None)
    path, dist, outdist = returnpath
    if returnpath == None:
        raise ValueError
    if dist == None or dist > max_total_dist:
        raise ValueError
    if outdist == None or outdist > max_dist_outdoors:
        raise ValueError
    print(returnpath)
    return path

def getDistance(digraph, path):
    total_dist = 0
    outdoor_dist = 0
    for i in range(len(path) - 1):
        for edge in digraph.edges[path[i]]:
            if edge.dest == path[i + 1]:
                total_dist += int(edge.get_total_distance())
                outdoor_dist += int(edge.get_outdoor_distance())
    return (total_dist, outdoor_dist)


# g = load_map('test_load_map.txt')
# g = load_map('mit_map.txt')
# testpath = ['1', '3', '10', '4', '12', '24', '34', '36', '32']
# print(getDistance(g,testpath))
# print(directed_dfs(g,g.getNode('1'),g.getNode('32'),1000,0))


# ================================================================
# Begin tests -- you do not need to modify anything below this line
# ================================================================

class Ps2Test(unittest.TestCase):
    LARGE_DIST = 99999

    def setUp(self):
        self.graph = load_map("mit_map.txt")

    def test_load_map_basic(self):
        self.assertTrue(isinstance(self.graph, Digraph))
        self.assertEqual(len(self.graph.nodes), 37)
        all_edges = []
        for _, edges in self.graph.edges.items():
            all_edges += edges  # edges must be dict of node -> list of edges
        all_edges = set(all_edges)
        self.assertEqual(len(all_edges), 129)

    def _print_path_description(self, start, end, total_dist, outdoor_dist):
        constraint = ""
        if outdoor_dist != Ps2Test.LARGE_DIST:
            constraint = "without walking more than {}m outdoors".format(
                outdoor_dist)
        if total_dist != Ps2Test.LARGE_DIST:
            if constraint:
                constraint += ' or {}m total'.format(total_dist)
            else:
                constraint = "without walking more than {}m total".format(
                    total_dist)

        print("------------------------")
        print("Shortest path from Building {} to {} {}".format(
            start, end, constraint))

    def _test_path(self,
                   expectedPath,
                   total_dist=LARGE_DIST,
                   outdoor_dist=LARGE_DIST):
        start, end = expectedPath[0], expectedPath[-1]
        self._print_path_description(start, end, total_dist, outdoor_dist)
        dfsPath = directed_dfs(self.graph, start, end, total_dist, outdoor_dist)
        print("Expected: ", expectedPath)
        print("DFS: ", dfsPath)
        self.assertEqual(expectedPath, dfsPath)

    def _test_impossible_path(self,
                              start,
                              end,
                              total_dist=LARGE_DIST,
                              outdoor_dist=LARGE_DIST):
        self._print_path_description(start, end, total_dist, outdoor_dist)
        with self.assertRaises(ValueError):
            directed_dfs(self.graph, start, end, total_dist, outdoor_dist)

    def test_path_one_step(self):
        self._test_path(expectedPath=['32', '56'])

    def test_path_no_outdoors(self):
        self._test_path(
            expectedPath=['32', '36', '26', '16', '56'], outdoor_dist=0)

    def test_path_multi_step(self):
        self._test_path(expectedPath=['2', '3', '7', '9'])

    def test_path_multi_step_no_outdoors(self):
        self._test_path(
            expectedPath=['2', '4', '10', '13', '9'], outdoor_dist=0)

    def test_path_multi_step2(self):
        self._test_path(expectedPath=['1', '4', '12', '32'])

    def test_path_multi_step_no_outdoors2(self):
        self._test_path(
            expectedPath=['1', '3', '10', '4', '12', '24', '34', '36', '32'],
            outdoor_dist=0)

    def test_impossible_path1(self):
        self._test_impossible_path('8', '50', outdoor_dist=0)

    def test_impossible_path2(self):
        self._test_impossible_path('10', '32', total_dist=100)


if __name__ == "__main__":
    pass
    unittest.main()
