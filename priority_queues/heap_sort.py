# -*- coding: utf-8 -*-


def heap_sort(items):
    """
    Heap sort using binary heap
    """
    n = len(items)

    def _sink(index, n):
        """
        Sink item down to the bottom until it is in the right place in the heap
        """
        while index * 2 + 1 < n:
            j = index * 2 + 1
            # choose the biggest child (left or right)
            if j + 1 < n and items[j + 1] > items[j]:
                # right child is bigger than left
                j += 1
            if items[index] < items[j]:
                # exchange item with the biggest child
                items[index], items[j] = items[j], items[index]
                index = j
            else:
                break

    # heapify the list: build a valid binary heap inplace
    for i in xrange(n / 2, -1, -1):
        _sink(i, n)

    # sort list by exchanging max element with the last
    while n > 0:
        items[0], items[n - 1] = items[n - 1], items[0]
        n -= 1
        # "sink" the first element in the right place
        _sink(0, n)


if __name__ == '__main__':
    import random
    from sorting.check_sorting import is_sorted

    items = range(10)
    random.shuffle(items)
    heap_sort(items)
    assert is_sorted(items)