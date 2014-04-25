# -*- coding: utf-8 -*-


def msd_radix_sort(strings):
    """
    MSD radix sort. Stable string sorting algorithm which runs O(W*N)
    where W is the length of all the strings (the length must be equal)
    and N is the number of strings to be sorted.
    It uses extra space for count array and aux array.
    """

    def sort(strings, aux, d, lo, hi):
        if hi <= lo:
            return
        print 'lo=',lo, 'hi=',hi, 'd=', d
        # use ASCII table bounds
        radix = 256
        #
        count = [0] * radix
        # count each number
        for i in xrange(lo, hi + 1):
            try:
                count[ord(strings[i][d])] += 1
            except IndexError:
                # TODO: deal with short words
                # (Sedgewick proposed to add extra character "-1" to the end of every string)
                pass
        # compute cumulates
        for c in xrange(radix):
            s = 0 if c == 0 else count[c - 1]
            count[c] += s
        for i in xrange(lo, hi + 1):
            try:
                aux[count[ord(strings[i][d]) - 1]] = strings[i]
                count[ord(strings[i][d]) - 1] += 1
            except IndexError:
                # TODO: deal with short words
                pass
        for i in xrange(lo, hi + 1):
            strings[i] = aux[i - lo]
        print strings
        # sort subarrays recursively
        for r in xrange(radix - 1):
            sort(strings, aux, d + 1, lo + count[r], lo + count[r + 1] - 1)

    aux = [0] * len(strings)
    sort(strings, aux, 0, 0, len(strings) - 1)


if __name__ == '__main__':
    a = ['she', 'sells', 'seashells', 'by', 'the', 'sea', 'shore',
         'the', 'shells', 'she', 'sells', 'are', 'surely', 'seashells']
    msd_radix_sort(a)
    assert a == 'are by seashells seashells sells sells she she shells shore surely the the'.split()