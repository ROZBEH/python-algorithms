# -*- coding: utf-8 -*-
from sorting.check_sorting import is_sorted


def binary_search(items, needed):
    """
    Binary search implementation without recursion
    """
    lo, hi = 0, len(items) - 1
    while lo <= hi:
        mid = lo + (hi - lo) / 2
        if needed < items[mid]:
            # switch to the left part
            hi = mid - 1
        elif needed > items[mid]:
            # switch to the right part
            lo = mid + 1
        else:
            # item is found
            return mid
    # pointers have crossed and item is not found
    return None


def binary_search_recursive(items, needed, _lo=0, _hi=None):
    """
    Binary search implementation with recursion
    """
    if _hi is None:
        _hi = len(items) - 1
    mid = _lo + (_hi - _lo) / 2
    while _lo <= _hi:
        if needed < items[mid]:
            return binary_search_recursive(items, needed, _lo=_lo, _hi=mid - 1)
        elif needed > items[mid]:
            return binary_search_recursive(items, needed, _lo=mid + 1, _hi=_hi)
        else:
            return mid
    return None


if __name__ == 'main':
    items = range(1000)
    # just to show that binary search requires sorted input
    assert is_sorted(items)
    assert binary_search(items, 10) == 9
    assert binary_search_recursive(items, 1) == 1