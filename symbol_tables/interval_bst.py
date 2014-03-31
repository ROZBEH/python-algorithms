# -*- coding: utf-8 -*-


class IntervalBST(object):
    """
    Binary search tree which stores intervals like (1, 10) instead of key-value pairs
    This data structure allows to find overlapping intervals quickly, but may run O(sqrt(N)) in the worst case.
    However, red-black interval BST will guarantee O(logN) efficiency due to perfectly balanced tree.
    """

    class Node(object):

        def __init__(self, lo, hi):
            self.lo = lo
            self.hi = hi
            self.max = hi
            self.left = None
            self.right = None

        def intersects(self, lo, hi):
            return self.lo <= lo <= self.hi or self.lo <= hi <= self.hi

        def __repr__(self):
            return 'Node({}, {})'.format(repr(self.lo), repr(self.hi))

    def __init__(self):
        self.root = None

    def put(self, lo, hi):

        def _put(node, lo, hi):
            if node is None:
                return self.Node(lo, hi)
            if lo < node.lo:
                node.left = _put(node.left, lo, hi)
                # update max
                node.max = max(self._max(node.left), self._max(node))
            elif lo > node.lo:
                node.right = _put(node.right, lo, hi)
                # update max
                node.max = max(self._max(node.right), self._max(node))
            else:
                # we do not allow to have intervals with the same lo value
                raise ValueError('Interval with lower bound "{}" already exists'.format(lo))

            return node

        self.root = _put(self.root, lo, hi)

    def _max(self, node):
        return 0 if node is None else node.max

    def search(self, lo, hi):
        node = self.root

        while node is not None:
            if node.intersects(lo, hi):
                return node
            elif node.left is None:
                node = node.right
            elif node.left.max < lo:
                node = node.right
            else:
                node = node.left

        return None


if __name__ == '__main__':

    it = IntervalBST()
    it.put(17, 19)
    it.put(5, 18)
    it.put(21, 24)
    it.put(4, 8)
    it.put(15, 18)
    it.put(7, 10)
    it.put(16, 22)

    i1 = it.search(17, 19)
    assert i1.lo == 17 and i1.hi == 19
    i2 = it.search(21, 23)
    assert i2.lo == 16 and i2.hi == 22