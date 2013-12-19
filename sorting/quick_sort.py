# -*- coding: utf-8 -*-


def qsort_py(items):
    """
    Quick sort Pythonish version
    Memory inefficient, but nice and stable
    """
    if len(items) > 1:
        return qsort_py([x for x in items[1:] if x < items[0]]) + [items[0]] + qsort_py(
            [x for x in items[1:] if x >= items[0]])
    else:
        return items


def qsort(items):
    """
    Classical quick inline sort with 2-way partitioning (suggested by Tony Hoare in 1961)
    It may run quadratic time in case of many duplicate items
    """
    _sort(items, 0, len(items) - 1)


def qsort_3w(items):
    """
    Quick sort suggested by Edsger Dijkstra
    """
    _sort_3w(items, 0, len(items) - 1)


def _sort_3w(items, lo, hi):
    """
    Recursive sorting function with 3-way partitioning
    """
    if hi <= lo:
        return
    lt = lo
    gt = hi
    pivot = items[lo]
    i = lo
    while i <= gt:
        if items[i] < pivot:
            items[lt], items[i] = items[i], items[lt]
            lt += 1
            i += 1
        elif items[i] > pivot:
            items[gt], items[i] = items[i], items[gt]
            gt -= 1
        else:
            i += 1
    _sort_3w(items, lo, lt - 1)
    _sort_3w(items, gt + 1, hi)


def _sort(items, lo, hi):
    """
    Recursive sorting function
    """
    if hi <= lo:
        return

    pivot = _partition(items, lo, hi)
    _sort(items, lo, pivot - 1)
    _sort(items, pivot + 1, hi)


def _partition(items, lo, hi):
    left = lo + 1
    right = hi
    while True:

        while items[left] < items[lo]:
            # find item on left to swap
            left += 1
            if left >= hi:
                break

        while items[right] > items[lo]:
            # find item on right to swap
            right -= 1
            if right <= lo:
                break

        # if we have already gone through all items
        if left >= right:
            break

        # swap items
        items[left], items[right] = items[right], items[left]

    # swap partitioning item with the biggest on the left side (which is less than lo)
    items[lo], items[right] = items[right], items[lo]
    return right


if __name__ == '__main__':
    import random
    from check_sorting import is_sorted

    items = range(100)
    random.shuffle(items)
    qsort(items)
    assert is_sorted(items)
    random.shuffle(items)
    qsort_3w(items)
    assert is_sorted(items)
    random.shuffle(items)
    items = qsort_py(items)
    assert is_sorted(items)