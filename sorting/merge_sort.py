# -*- coding: utf-8 -*-


def merge_sort(items):
    """
    Merge sort
    """
    if len(items) < 2:
        return items
    mid = len(items) / 2

    return _merge(merge_sort(items[:mid]), merge_sort(items[mid:]))


def _merge(left, right):
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

if __name__ == '__main__':
    import random
    from check_sorting import is_sorted

    items = range(100)
    random.shuffle(items)
    items = merge_sort(items)
    assert is_sorted(items)