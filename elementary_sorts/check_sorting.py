# -*- coding: utf-8 -*-


def is_sorted(items, descending=False):
    for i in xrange(len(items)):
        if i > 0 and descending is False and items[i] < items[i - 1]:
            return False
        elif i > 0 and descending and items[i] > items[i - 1]:
            return False

    return True