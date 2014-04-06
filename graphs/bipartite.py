# -*- coding: utf-8 -*-
from collections import defaultdict


class BipartiteGraph(object):
    """
    Check if the graph is bipartite: divide graph into 2 halves so that an edge of every vertex
    points to the vertex of another subset (half)
    """

    def __init__(self, graph):
        self.graph = graph
        self.color = defaultdict(bool)
        self.visited = []
        self.prev_to = dict()
        self.is_bipartite = True
        # odd-length cycle
        self.cycle = []

        for v in self.graph.vertices():
            if v not in self.visited:
                self._dfs(v)

    def _dfs(self, vertex):
        """
        Depth-first search is used to iter over all the vertices
        and mark their color
        """
        self.visited.append(vertex)
        for adj in self.graph.iter_adjacent(vertex):
            if adj not in self.visited:
                # found uncolored vertex, so recur
                self.prev_to[adj] = vertex
                self.color[adj] = not self.color[vertex]
                self._dfs(adj)
            elif self.color[adj] == self.color[vertex]:
                # if vertex-adj create an odd-length cycle, find it
                self.is_bipartite = False
                self.cycle = []
                self.cycle.append(adj)
                x = vertex
                while x != adj:
                    try:
                        x = self.prev_to[x]
                        self.cycle.append(x)
                    except KeyError:
                        break
                self.cycle.append(adj)
                return


if __name__ == '__main__':

    from graph_api import Graph

    g = Graph()
    g.add_edge(0)
    g.add_edge(1, 0)
    g.add_edge(2, 0)
    g.add_edge(6, 0)
    g.add_edge(5, 0)
    g.add_edge(3, 1)
    g.add_edge(3, 2)
    g.add_edge(4, 2)
    g.add_edge(4, 6)
    g.add_edge(5, 0)
    g.add_edge(5, 4)

    bp = BipartiteGraph(g)
    assert bp.is_bipartite

