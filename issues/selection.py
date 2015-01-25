# -*- coding: utf-8 -*-
import sys
import os
sys.path.append(os.pardir)
from sorting import quick_sort


def selection(items, k):
    """
    Selection issue using _partition function
    """
    lo = 0
    hi = len(items) - 1
    while hi > lo:
        pivot = quick_sort._partition(items, lo, hi)
        if pivot < k:
            lo = pivot + 1
        elif pivot > k:
            hi = pivot - 1
        else:
            return items[k]

    return items[k]


if __name__ == '__main__':
    items = [1, 6, 2, 7, 3]
    s = selection(items, 1)
    print 's=', s, 'items=', items