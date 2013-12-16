# -*- coding: utf-8 -*-


def insertion_sort(items):
    """
    Insertion sort
    """
    n = len(items)
    # iterate over every item
    for i in xrange(n):
        j = i
        # if the current item is not in order
        while j > 0 and items[j] < items[j - 1]:
            # exchange those items
            items[j], items[j - 1] = items[j - 1], items[j]
            j -= 1


if __name__ == '__main__':
    import random
    from check_sorting import is_sorted

    items = range(100)
    random.shuffle(items)
    insertion_sort(items)
    assert is_sorted(items)