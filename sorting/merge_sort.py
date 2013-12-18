# -*- coding: utf-8 -*-


def merge_sort_py(items):
    """
    Merge sort Pythonish version
    Memory inefficient, but nice
    """
    if len(items) < 2:
        return items
    mid = len(items) / 2

    return _merge_lists(merge_sort_py(items[:mid]), merge_sort_py(items[mid:]))


def _merge_lists(left, right):
    """
    Merge two lists with ascending ordered items
    """
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result += left[i:]
    result += right[j:]
    return result


def merge_sort(items):
    """
    Classical merge sort
    """
    _sort(items, items[:], 0, len(items) - 1)


def merge_sort_bu(items):
    """
    Bottom-up merge sort
    No recursion is used
    """
    aux = items[:]
    size = 1
    while size < len(items):
        lo = 0
        while lo < len(items) - size:
            mid = lo + size - 1
            hi = min(lo + size * 2 - 1, len(items) - 1)
            _merge(items, aux, lo, mid, hi)

            lo += size * 2

        size *= 2


def _sort(items, aux, lo, hi):
    """
    Recursive sorting function
    """
    if hi <= lo:
        return

    mid = lo + (hi - lo) / 2
    # sort left part
    _sort(items, aux, lo, mid)
    # sort right part
    _sort(items, aux, mid + 1, hi)
    # merge parts
    _merge(items, aux, lo, mid, hi)


def _merge(items, aux, lo, mid, hi):
    """
    Merge
    """
    for k in xrange(lo, hi + 1):
        aux[k] = items[k]
    i = lo
    j = mid + 1
    for k in xrange(lo, hi + 1):
        if i > mid:
            # left part exhausted - use right part
            items[k] = aux[j]
            j += 1
        elif j > hi:
            # right part exhausted - use left part
            items[k] = aux[i]
            i += 1
        elif aux[j] < aux[i]:
            # right item is less than left - use right item
            items[k] = aux[j]
            j += 1
        else:
            # left items is less than right - use left item
            items[k] = aux[i]
            i += 1


if __name__ == '__main__':
    import random
    from check_sorting import is_sorted

    items = range(100)
    random.shuffle(items)
    merge_sort(items)
    assert is_sorted(items)
    random.shuffle(items)
    merge_sort_bu(items)
    assert is_sorted(items)
    random.shuffle(items)
    items = merge_sort_py(items)
    assert is_sorted(items)