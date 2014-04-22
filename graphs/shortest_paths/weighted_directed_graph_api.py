# -*- coding: utf-8 -*-


class DirectedEdge(object):
    """
    Weighted directed edge API
    """

    def __init__(self, vertex1, vertex2, weight):
        self.vertex1 = vertex1
        self.vertex2 = vertex2
        self.weight = weight

    def vertex_from(self):
        return self.vertex1

    def vertex_to(self):
        return self.vertex2

    def __cmp__(self, other):
        if self.weight > other.weight:
            return 1
        elif self.weight < other.weight:
            return -1
        else:
            return 0

    def __repr__(self):
        return 'Edge({}, {}, {})'.format(self.vertex1, self.vertex2, self.weight)


class WeightedDigraphAPI(object):
    """
    Weighted graph API which uses weighted edge API
    """

    def __init__(self):
        # dict with adjacent vertices
        self.adjacent = dict()
        self.edges = set()

    def add_edge(self, edge):
        v = edge.vertex_from()
        if v in self.adjacent:
            self.adjacent[v].add(edge)
        else:
            self.adjacent[v] = set([edge])
        self.edges.add(edge)

    def iter_adjacent(self, v):
        return iter(self.adjacent[v])

    def __iter__(self):
        return iter(self.edges)

    def __len__(self):
        return len(self.adjacent)


