# -*- coding: utf-8 -*-


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
        self.prev_vertex = dict()
        self._build_paths(start, start)
        pass

    def _build_paths(self, start, prev):
        self.visited.append(start)
        self.prev_vertex[start] = prev
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
            vertex = self.prev_vertex[vertex]
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

    path = DepthFirstPaths(g, 0)
    assert list(path.path_to(10)) == [0, 1, 2, 3, 7, 10]
