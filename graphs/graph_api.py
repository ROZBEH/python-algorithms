# -*- coding: utf-8 -*-


class Graph(object):
    """
    Undirected graph API with adjacency-list data structure which uses (Edges + Verticies) memory
    """

    def __init__(self):
        self.adjacent = dict()

    def add_edge(self, v, w=None):
        """
        Add a vertex and an edge
        """
        if w is not None:
            if v in self.adjacent:
                self.adjacent[v].add(w)
            else:
                self.adjacent[v] = set([w])
            if w in self.adjacent:
                self.adjacent[w].add(v)
            else:
                self.adjacent[w] = set([v])
        else:
            self.adjacent[v] = set()

    def degree(self, v):
        """
        Number of adjacent vertices
        """
        return len(self.adjacent[v])

    def max_degree(self):
        """
        Max degree of the graph
        """
        maxd = 0
        for v, adj in self.adjacent.iteritems():
            m = len(adj)
            if m > maxd:
                maxd = m
        return maxd

    def self_loops_count(self):
        # TODO: check this code
        count = 0
        for v, adj in self.adjacent.iteritems():
            if v in adj:
                count += 1
        return count / 2

    def iter_adjacent(self, v):
        return iter(self.adjacent[v])

    def __contains__(self, item):
        return item in self.adjacent

    def __len__(self):
        return len(self.adjacent)

    def __iter__(self):
        return self.adjacent.iterkeys()


class Digraph(Graph):
    """
    Directed graph API which is similar to undirected graph API
    """

    def add_edge(self, v, w=None):
        """
        Add a vertex and an edge
        """
        if w is not None:
            if v in self.adjacent:
                self.adjacent[v].add(w)
            else:
                self.adjacent[v] = set([w])
        else:
            self.adjacent[v] = set()


if __name__ == '__main__':
    g = Graph()
    g.add_edge(0)
    g.add_edge(1, 0)
    g.add_edge(2, 1)
    g.add_edge(3, 2)
    g.add_edge(4, 1)
    g.add_edge(5, 2)
    g.add_edge(6, 2)
    g.add_edge(7, 3)
    assert g.degree(2) == g.max_degree()

    g = Digraph()
    g.add_edge(0)
    g.add_edge(1, 0)
    g.add_edge(2, 1)
    g.add_edge(3, 2)
    g.add_edge(4, 1)
    g.add_edge(5, 2)
    g.add_edge(6, 2)
    g.add_edge(7, 3)
    assert g.degree(2) == g.max_degree()