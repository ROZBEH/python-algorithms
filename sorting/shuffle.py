# -*- coding: utf-8 -*-


def shuffle(items):
    """
    Shuffle items
    """
    import random
    n = len(items)
    for i in xrange(n):
        # generate random in from 0 to i
        r = random.randint(0, i)
        # exchange items with index i and r
        items[i], items[r] = items[r], items[i]


if __name__ == '__main__':
    from check_sorting import is_sorted

    items = range(100)
    shuffle(items)
    assert not is_sorted(items)