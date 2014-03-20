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
    Priority queue with binary heap data structure
    """
    def __init__(self):
        self.data = [None]

    def insert(self, item):
        self.data.append(item)
        self._swim(len(self) - 1)

    def _swim(self, k):
        while k > 1 and self.data[k] > self.data[k / 2]:
            self.data[k], self.data[k / 2] = self.data[k / 2], self.data[k]
            k /= 2

    def _sink(self, k):
        while k * 2 < len(self):
            j = k * 2
            if j + 1 < len(self) and self.data[j] < self.data[j + 1]:
                j += 1
            if self.data[k] >= self.data[j]:
                break
            else:
                self.data[k], self.data[j] = self.data[j], self.data[k]
            k = j

    def del_max(self):
        max = self.data[1]
        self.data[1], self.data[len(self) - 1] = self.data[len(self) - 1], self.data[1]
        self._sink(1)
        self.data.pop()
        return max

    @property
    def is_empty(self):
        return len(self) == 0

    def __len__(self):
        return len(self.data)

    def __iter__(self):
        return iter(self.data)