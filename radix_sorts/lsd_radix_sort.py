# -*- coding: utf-8 -*-


def lsd_radix_sort(strings, length):
    """
    LSD radix sort. Stable string sorting algorithm which runs O(W*N)
    where W is the length of all the strings (the length must be equal)
    and N is the number of strings to be sorted.
    """
    # use ASCII table bounds
    radix = 256
    aux = [0] * len(strings)
    # do key-indexed counting for each digit from right to left
    for d in xrange(length - 1, -1, -1):
        count = [0] * radix
        # count each number
        for i in xrange(len(strings)):
            count[ord(strings[i][d])] += 1
        # compute cumulates
        for c in xrange(len(count)):
            s = 0 if c == 0 else count[c - 1]
            count[c] += s
        # fill in the aux list for each of the digit column
        for i in xrange(len(strings)):
            aux[count[ord(strings[i][d]) - 1]] = strings[i]
            count[ord(strings[i][d]) - 1] += 1
        # copy all data from aux to original list
        for i in xrange(len(strings)):
            strings[i] = aux[i]


if __name__ == '__main__':
    a = ['adb', 'bac', 'dab', 'ceb', 'bbb', 'cea', 'eac']
    lsd_radix_sort(a, 3)
    assert a == ['adb', 'bac', 'bbb', 'cea', 'ceb', 'dab', 'eac']