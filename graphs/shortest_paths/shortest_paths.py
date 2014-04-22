# -*- coding: utf-8 -*-
from collections import defaultdict
from priority_queues.pq_api import MinPQ
from graphs.topological_sort import DepthFirstOrderDigraph


class DijkstraSP(object):
    """
    Dijkstra digraph shortest path algorithm which runs ELogV,
    where E is a number of edges and V is a number of vertices
    """

    def __init__(self, graph, start):
        self.graph = graph
        self.start = start
        self.edge_to = dict()
        # in the beginning dist to every vertex is a positive infinity
        self.dist_to = defaultdict(lambda: float('inf'))
        # TODO: this should be IndexedMinPQ instead
        # the implementation is here: http://algs4.cs.princeton.edu/24pq/IndexMinPQ.java.html
        self.pq = MinPQ()

        # set the distance to the starting point to 0
        self.dist_to[start] = 0
        self.pq.push(start)
        while self.pq:
            v = self.pq.pop()
            for edge in self.graph.iter_adjacent(v):
                # relax every adjacent edge
                self.relax(edge)

    def relax(self, edge):
        v = edge.vertex_from()
        w = edge.vertex_to()
        if self.dist_to[w] > self.dist_to[v] + edge.weight:
            self.dist_to[w] = self.dist_to[v] + edge.weight
            self.edge_to[w] = edge
            if w not in self.pq:
                self.pq.push(w)
            else:
                # TODO: update the priority queue here (decrease key)
                pass

    def path_to(self, v):
        if v in self.edge_to:
            path = [v]
            e = self.edge_to[v]
            while e.vertex_from() != self.start:
                path.append(e.vertex_from())
                e = self.edge_to[e.vertex_from()]
            path.append(self.start)
            return reversed(path)
        else:
            return


class AcyclicSP(object):
    """
    DAG shortest path algorithm which runs E + V,
    where E is a number of edges and V is a number of vertices
    It iterates over the vertices in topological order
    """

    def __init__(self, graph, start):
        self.graph = graph
        self.start = start
        self.edge_to = dict()
        # in the beginning dist to every vertex is a positive infinity
        self.dist_to = defaultdict(lambda: float('inf'))

        # set the distance to the starting point to 0
        self.dist_to[start] = 0
        # perform a topological sort
        topological = DepthFirstOrderDigraph(graph)
        for v in topological:
            # relax every adjacent edge
            for edge in graph.iter_adjacent(v):
                self.relax(edge)

    def relax(self, edge):
        v = edge.vertex_from()
        w = edge.vertex_to()
        if self.dist_to[w] >= self.dist_to[v] + edge.weight:
            self.dist_to[w] = self.dist_to[v] + edge.weight
            self.edge_to[w] = edge

    def path_to(self, v):
        if v in self.edge_to:
            path = [v]
            e = self.edge_to[v]
            while e.vertex_from() != self.start:
                path.append(e.vertex_from())
                e = self.edge_to[e.vertex_from()]
            path.append(self.start)
            return reversed(path)
        else:
            return


if __name__ == '__main__':
    from graphs.shortest_paths.weighted_directed_graph_api import WeightedDigraphAPI, DirectedEdge

    graph = WeightedDigraphAPI()
    graph.add_edge(DirectedEdge(4, 5, 0.35))
    graph.add_edge(DirectedEdge(4, 7, 0.37))
    graph.add_edge(DirectedEdge(5, 7, 0.28))
    graph.add_edge(DirectedEdge(0, 7, 0.16))
    graph.add_edge(DirectedEdge(1, 5, 0.32))
    graph.add_edge(DirectedEdge(0, 4, 0.38))
    graph.add_edge(DirectedEdge(0, 1, 0.5))
    graph.add_edge(DirectedEdge(2, 3, 0.17))
    graph.add_edge(DirectedEdge(1, 7, 0.19))
    graph.add_edge(DirectedEdge(0, 2, 0.26))
    graph.add_edge(DirectedEdge(1, 2, 0.36))
    graph.add_edge(DirectedEdge(1, 3, 0.29))
    graph.add_edge(DirectedEdge(2, 7, 0.34))
    graph.add_edge(DirectedEdge(6, 2, 0.40))
    graph.add_edge(DirectedEdge(3, 6, 0.52))
    graph.add_edge(DirectedEdge(6, 0, 0.58))
    graph.add_edge(DirectedEdge(6, 4, 0.93))
    graph.add_edge(DirectedEdge(7, 6, 0.34))

    sp = DijkstraSP(graph, 0)
    assert list(sp.path_to(5)) == [0, 4, 5]

    # Directed Acyclic Graph
    graph = WeightedDigraphAPI()
    graph.add_edge(DirectedEdge(0, 1, 5))
    graph.add_edge(DirectedEdge(1, 3, 15))
    graph.add_edge(DirectedEdge(1, 2, 12))
    graph.add_edge(DirectedEdge(1, 7, 4))
    graph.add_edge(DirectedEdge(3, 6, 9))
    graph.add_edge(DirectedEdge(0, 7, 8))
    graph.add_edge(DirectedEdge(7, 2, 7))
    graph.add_edge(DirectedEdge(7, 5, 6))
    graph.add_edge(DirectedEdge(2, 6, 11))
    graph.add_edge(DirectedEdge(0, 4, 9))
    graph.add_edge(DirectedEdge(4, 7, 5))
    graph.add_edge(DirectedEdge(4, 5, 4))
    graph.add_edge(DirectedEdge(4, 6, 20))
    graph.add_edge(DirectedEdge(5, 2, 1))
    graph.add_edge(DirectedEdge(5, 6, 13))

    sp = AcyclicSP(graph, 0)
    assert list(sp.path_to(6)) == [0, 4, 5, 2, 6]