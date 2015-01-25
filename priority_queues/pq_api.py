# -*- coding: utf-8 -*-


class UnorderedMaxPQ(object):
    """
    Unordered Max PQ
    Items are appended without ordering when insert
    """

    def __init__(self):
        self.data = list()

    def insert(self, item):
        self.data.append(item)

    def del_max(self):
        max = 0
        n = len(self)
        for i in xrange(1, n):
            if self.data[i] > self.data[max]:
                max = i
        self.data[max], self.data[n - 1] = self.data[n - 1], self.data[max]
        return self.data.pop()

    @property
    def is_empty(self):
        return len(self) == 0

    def __len__(self):
        return len(self.data)

    def __iter__(self):
        return iter(self.data)


class MaxPQ(object):
    """
    Max oriented priority queue with binary heap data structure
    """
    def __init__(self):
        self.data = []

    def push(self, item):
        self.data.append(item)
        self._swim(len(self) - 1)

    def _swim(self, k):
        while k > 0 and self.data[k] > self.data[k / 2]:
            self.data[k], self.data[k / 2] = self.data[k / 2], self.data[k]
            k /= 2

    def _sink(self, k):
        while k * 2 + 1 < len(self):
            j = k * 2 + 1
            if j + 1 < len(self) and self.data[j] < self.data[j + 1]:
                j += 1
            if self.data[k] >= self.data[j]:
                break
            else:
                self.data[k], self.data[j] = self.data[j], self.data[k]
            k = j

    def pop(self):
        max = self.data[0]
        self.data[0], self.data[len(self) - 1] = self.data[len(self) - 1], self.data[0]
        self.data.pop()
        self._sink(0)
        return max

    @property
    def max(self):
        return self.data[0]

    def __nonzero__(self):
        return len(self) > 0

    def __len__(self):
        return len(self.data)

    def __iter__(self):
        return iter(self.data)


class MinPQ(object):
    """
    Min oriented priority queue with binary heap data structure
    """
    def __init__(self):
        self.data = []

    def push(self, item):
        self.data.append(item)
        self._swim(len(self) - 1)

    def _swim(self, k):
        while k > 0 and self.data[k] < self.data[k / 2]:
            self.data[k], self.data[k / 2] = self.data[k / 2], self.data[k]
            k /= 2

    def _sink(self, k):
        while k * 2 + 1 < len(self):
            j = k * 2 + 1
            if j + 1 < len(self) and self.data[j + 1] < self.data[j]:
                j += 1
            if self.data[k] <= self.data[j]:
                break
            else:
                self.data[k], self.data[j] = self.data[j], self.data[k]
            k = j

    def pop(self):
        min = self.data[0]
        self.data[0], self.data[len(self) - 1] = self.data[len(self) - 1], self.data[0]
        self.data.pop()
        self._sink(0)
        return min

    @property
    def min(self):
        return self.data[0]

    def __nonzero__(self):
        return len(self) > 0

    def __len__(self):
        return len(self.data)

    def __iter__(self):
        return iter(self.data)