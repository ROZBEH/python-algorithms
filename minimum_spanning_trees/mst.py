# -*- coding: utf-8 -*-
from Queue import Queue
from priority_queues.pq_api import MinPQ
from union_find.uf import UnionFind


class KruskalMST(object):
    """
    Kruskal's algorithm for finding minimum spanning trees
    It is kind of a greedy algorithm which runs in ElogE where E is the number of edges.
    """

    def __init__(self, graph):
        self.graph = graph
        self.weight = 0
        # the resulting minimum spanning tree
        self.mst = Queue()
        self.edges = MinPQ()
        for e in graph:
            self.edges.push(e)
        uf = UnionFind()
        while self.edges and self.mst.qsize() < len(graph) - 1:
            edge = self.edges.pop()
            v = edge.either()
            w = edge.other(v)
            if not uf.connected(v, w):
                uf.union(v, w)
                self.mst.put(edge)
                self.weight += edge.weight

    def __iter__(self):
        return iter(self.mst)


class PrimsMST(object):
    """
    Prims lazy MST
    Another kind of a greedy algorithm which runs ELogE
    """

    def __init__(self, graph):
        self.graph = graph
        self.weight = 0
        # the resulting minimum spanning tree
        self.mst = Queue()
        self.edges = MinPQ()
        self.visited = []
        # visit the root vertex (starting point)
        self._visit(0)

        while self.edges:
            edge = self.edges.pop()
            v = edge.either()
            w = edge.other(v)
            if v in self.visited and w in self.visited:
                continue
            else:
                self.mst.put(edge)
                self.weight += edge.weight
                if v not in self.visited:
                    self._visit(v)
                if w not in self.visited:
                    self._visit(w)

    def _visit(self, vertex):
        self.visited.append(vertex)
        for e in self.graph.iter_adjacent(vertex):
            if e.other(vertex) not in self.visited:
                self.edges.push(e)

    def __iter__(self):
        return iter(self.mst)


if __name__ == '__main__':
    from weighted_graph_api import WeightedGraphAPI, Edge

    graph = WeightedGraphAPI()
    graph.add_edge(Edge(4, 5, 0.35))
    graph.add_edge(Edge(4, 7, 0.37))
    graph.add_edge(Edge(5, 7, 0.28))
    graph.add_edge(Edge(0, 7, 0.16))
    graph.add_edge(Edge(1, 5, 0.32))
    graph.add_edge(Edge(0, 4, 0.38))
    graph.add_edge(Edge(2, 3, 0.17))
    graph.add_edge(Edge(1, 7, 0.19))
    graph.add_edge(Edge(0, 2, 0.26))
    graph.add_edge(Edge(1, 2, 0.36))
    graph.add_edge(Edge(1, 3, 0.29))
    graph.add_edge(Edge(2, 7, 0.34))
    graph.add_edge(Edge(6, 2, 0.40))
    graph.add_edge(Edge(3, 6, 0.52))
    graph.add_edge(Edge(6, 0, 0.58))
    graph.add_edge(Edge(6, 4, 0.93))

    mst = KruskalMST(graph)
    assert mst.weight == 1.81

    mst = PrimsMST(graph)
    assert mst.weight == 1.81