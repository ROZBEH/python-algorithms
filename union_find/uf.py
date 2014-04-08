# -*- coding: utf-8 -*-
from collections import defaultdict


class UnionFind(object):
    """
    Union find API
    This implementation uses weighted quick union by rank with path compression by halving.
    See http://algs4.cs.princeton.edu/15uf/UF.java.html
    """

    def __init__(self):
        self.id = dict()
        self.rank = defaultdict(int)

    def find(self, p):
        if p in self.id:
            while p != self.id[p]:
                # path compression by halving
                self.id[p] = self.id[self.id[p]]
                p = self.id[p]
        else:
            self.id[p] = p
        return p

    def union(self, p, q):
        i, j = self.find(p), self.find(q)
        if i == j:
            return
        # make the root of the smaller rank point to the root of the larger rank
        if self.rank[i] < self.rank[j]:
            self.id[i] = j
        elif self.rank[i] > self.rank[j]:
            self.id[j] = i
        else:
            self.id[j] = i
            self.rank[i] += 1

    def connected(self, p, q):
        return self.find(p) == self.find(q)


if __name__ == '__main__':
    uf = UnionFind()
    uf.union(1, 0)
    uf.union(2, 1)
    uf.union(3, 2)
    uf.union(5, 4)
    uf.union(6, 5)
    uf.union(7, 5)
    assert uf.find(7) == uf.find(5)
