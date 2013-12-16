# -*- coding: utf-8 -*-


def shell_sort(items):
    """
    Shell sort
    """
    n = len(items)
    h = 1
    # compute h with formula proposed by Knuth
    while h < n / 3:
        h = h * 3 + 1

    while h >= 1:
        # iterate over every item
        for i in xrange(n):
            j = i
            # compare the current item with every h item
            while j >= h and items[j] < items[j - h]:
                # exchange those items
                items[j], items[j - h] = items[j - h], items[j]
                j -= h
        # get the value of h for each iteration
        h /= 3


if __name__ == '__main__':
    import random
    from check_sorting import is_sorted

    items = range(100)
    random.shuffle(items)
    shell_sort(items)
    assert is_sorted(items)