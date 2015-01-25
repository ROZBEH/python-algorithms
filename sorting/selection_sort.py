# -*- coding: utf-8 -*-


def selection_sort(items):
    """
    Selection sort
    """
    n = len(items)
    # iterate over every item
    for i in xrange(n):
        # store index instead of value since value may be huge and expensive to store in memory
        smallest = i
        # find the smallest item from selected remaining items
        for j in xrange(i + 1, n):
            if items[j] < items[smallest]:
                smallest = j
        # exchange the current item with the smallest one
        items[i], items[smallest] = items[smallest], items[i]


if __name__ == '__main__':
    import random
    from check_sorting import is_sorted

    items = range(100)
    random.shuffle(items)
    selection_sort(items)
    assert is_sorted(items)