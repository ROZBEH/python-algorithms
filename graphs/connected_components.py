# -*- coding: utf-8 -*-
from topological_sort import DepthFirstOrder


class ConnectedComponents(object):
    """
    Search for connected components (connected set of vertices).
    Build "index" in linear time, answer the connectivity query in constant time.
    """

    def __init__(self, graph):
        self.graph = graph
        self.visited = []
        self.components = dict()
        # components counter
        self.count = 0
        for v in self.graph:
            if v not in self.visited:
                self.dfs(v)
                self.count += 1

    def dfs(self, vertex):
        """
        Depth-first search
        """
        self.visited.append(vertex)
        # add this vertex to component set
        self.components[vertex] = self.count
        for a in self.graph.iter_adjacent(vertex):
            if a not in self.visited:
                self.visited.append(a)
                # add this vertex to component set
                self.components[a] = self.count
                self.dfs(a)

    def __len__(self):
        return self.count + 1

    def connected(self, v, w):
        return self.id(v) == self.id(w)

    def id(self, v):
        return self.components[v]


class StrongConnectedComponents(ConnectedComponents):
    """
    Strong connected components for directed graph.
    Kosaraju Sharir method.
    It looks practically the same as the Connected Components, but iterates over
    the reversed postorder of vertices given by the topological sort
    """

    def __init__(self, graph):
        self.graph = graph
        self.visited = []
        self.components = dict()
        # components counter
        self.count = 0
        do = DepthFirstOrder(graph)
        for v in do:
            if v not in self.visited:
                self.dfs(v)
                self.count += 1


if __name__ == '__main__':
    from graph_api import Graph

    g = Graph()
    g.add_edge(0)
    g.add_edge(1, 0)
    g.add_edge(2, 1)
    g.add_edge(3, 2)
    g.add_edge(4, 1)
    g.add_edge(5, 2)
    g.add_edge(6, 2)
    g.add_edge(7, 7)
    g.add_edge(8, 7)
    g.add_edge(9, 7)
    g.add_edge(10, 7)
    g.add_edge(11, 11)
    g.add_edge(12, 11)

    cc = ConnectedComponents(g)
    assert len(cc) == 4