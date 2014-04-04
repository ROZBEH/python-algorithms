# -*- coding: utf-8 -*-
from Queue import Queue


class DepthFirstPaths(object):
    """
    Depth-first search graph algorithm.
    It is an ancient algorithm which goal is to not to go the same route twice
    """

    def __init__(self, graph, start):
        assert start in graph
        self.graph = graph
        self.start = start
        self.visited = []
        self.prev_to = dict()
        self._build_paths(start, start)

    def _build_paths(self, start, prev):
        self.visited.append(start)
        self.prev_to[start] = prev
        for v in self.graph.iter_adjacent(start):
            if v not in self.visited:
                self._build_paths(v, start)

    def has_path_to(self, vertex):
        """
        Is there any path from start to vertex?
        """
        return vertex in self.visited

    def path_to(self, vertex):
        """
        Return a path from start to vertex
        """
        if not self.has_path_to(vertex):
            return None
        path = []
        while vertex is not self.start:
            path.append(vertex)
            vertex = self.prev_to[vertex]
        path.append(vertex)
        return reversed(path)


class BreadthFirstPaths(object):
    """
    Breadth-first search graph algorithm.
    We visit each vertex once using Queue, this allows us to compute
    the distance from the start vertex to any vertex in the graph easily
    """

    def __init__(self, graph, start):
        assert start in graph
        self.graph = graph
        self.start = start
        self.visited = []
        self.prev_to = dict()
        self._build_paths()

    def _build_paths(self):
        queue = Queue()
        vertex = self.start
        # add the start vertex to the queue
        queue.put(vertex)
        self.visited.append(vertex)
        self.prev_to[vertex] = self.start
        while not queue.empty():
            # dequeue the queue
            vertex = queue.get()
            # iterate through all the adjacent vertices
            for v in self.graph.iter_adjacent(vertex):
                if not v in self.visited:
                    queue.put(v)
                    self.visited.append(v)
                    self.prev_to[v] = vertex

    def has_path_to(self, vertex):
        """
        Is there any path from start to vertex?
        """
        return vertex in self.visited

    def path_to(self, vertex):
        """
        Return a path from start to vertex
        """
        if not self.has_path_to(vertex):
            return None
        path = []
        while vertex is not self.start:
            path.append(vertex)
            vertex = self.prev_to[vertex]
        path.append(vertex)
        return reversed(path)

if __name__ == '__main__':
    from graph_api import Graph
    g = Graph()
    g.add_edge(0, 0)
    g.add_edge(1, 0)
    g.add_edge(2, 1)
    g.add_edge(3, 2)
    g.add_edge(4, 1)
    g.add_edge(5, 2)
    g.add_edge(6, 2)
    g.add_edge(7, 3)
    g.add_edge(8, 7)
    g.add_edge(9, 7)
    g.add_edge(10, 7)

    dfs = DepthFirstPaths(g, 0)
    assert list(dfs.path_to(10)) == [0, 1, 2, 3, 7, 10]
    bfs = BreadthFirstPaths(g, 0)
    assert list(dfs.path_to(10)) == [0, 1, 2, 3, 7, 10]
