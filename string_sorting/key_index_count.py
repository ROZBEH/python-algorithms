# -*- coding: utf-8 -*-


def key_index_sort(items, maxnum):
    """
    Key index counting sorts the list with NO compares at all.
    It is stable and runs ~O(11N + 4R) list accesses to sort N items between 0 and R - 1
    """
    assert max(items) == maxnum - 1
    # how many times each number occurs in the list
    count = [0] * maxnum

    # count each number
    for i in xrange(len(items)):
        count[items[i]] += 1

    # compute cumulates
    for r in xrange(maxnum):
        sum = 0 if r == 0 else count[r - 1]
        count[r] += sum

    # fill in the aux array (this approach is used by Sedgewick)
    # aux = [0] * len(a)
    # count = [0] + count
    # fill in the aux list
    # for i in xrange(len(a)):
    #     aux[count[a[i]]] = a[i]
    #     count[a[i]] += 1

    # alternative way to rearrange the original list which uses no extra space
    r = 0
    for c in xrange(len(count)):
        sub = 0 if c == 0 else count[c - 1]
        diff = count[c] - sub
        for d in xrange(diff):
            a[r] = c
            r += 1

if __name__ == '__main__':
    a = [3, 0, 2, 5, 5, 1, 3, 1, 5, 1, 4, 0]

    key_index_sort(a, 6)
    assert a == [0, 0, 1, 1, 1, 2, 3, 3, 4, 5, 5, 5]
