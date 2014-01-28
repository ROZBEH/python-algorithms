# -*- coding: utf-8 -*-


class MaxPQ(object):
    """
    Priority queue API
    """

    def __init__(self, data):
        self.data = data

    def insert(self, item):
        pass

    def del_max(self):
        pass

    @property
    def is_empty(self):
        return len(self.data) == 0

    def get_max(self):
        """
        Returns the largest item
        """
        return self.data[-1]