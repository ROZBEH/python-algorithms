# -*- coding: utf-8 -*-


class DepthFirstOrder(object):
    """
    Topological sort of the graph if it does not have loops
    Depth first search is used with slightly modifications
    """

    def __init__(self, graph):
        self.graph = graph
        self.visited = []
        self.reversed_post = []
        for v in self.graph:
            if v not in self.visited:
                self._dfs(v)

    def _dfs(self, vertex):
        self.visited.append(vertex)
        for v in self.graph.iter_adjacent(vertex):
            if v not in self.visited:
                self._dfs(v)
        # before exiting dfs - add the vertex to the list
        self.reversed_post.append(vertex)

    def __iter__(self):
        return reversed(self.reversed_post)


class DepthFirstOrderDigraph(DepthFirstOrder):
    """
    Topological sort of the DAG
    """

    def _dfs(self, vertex):
        self.visited.append(vertex)
        # iterate over edges not vertices since it is a DAG
        for edge in self.graph.iter_adjacent(vertex):
            v = edge.vertex_to()
            if v not in self.visited:
                self._dfs(v)
        # before exiting dfs - add the vertex to the list
        self.reversed_post.append(vertex)

if __name__ == '__main__':
    from graph_api import Graph
    g = Graph()
    g.add_edge(0)
    g.add_edge(5, 2)
    g.add_edge(6, 2)
    g.add_edge(1, 0)
    g.add_edge(4, 1)
    g.add_edge(7, 3)
    g.add_edge(8, 7)
    g.add_edge(2, 1)
    g.add_edge(3, 2)
    g.add_edge(9, 7)
    g.add_edge(10, 7)

    do = DepthFirstOrder(g)
    assert list(iter(g)) == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]