# -*- coding: utf-8 -*-


def search(string, pattern):
    """
    Boyer-Moore substring search algorithm.
    It runs ~O(N/M) on average (N=len(haystack), M=len(needle)),
    using no backups going through the text from left to right,
    but going through the pattern from right to left jumping over the text pointer from 1 to M characters.
    So it is the fastest substring search algorithm in practice, but it may run O(N*M) in the worst case
    when there are lots of duplicates in the text.
    """
    m = len(pattern)
    n = len(string)
    # build the skip table for ASCII
    right = [-1] * 256
    # match the pattern chars with their position in the pattern
    for i in xrange(m):
        right[ord(pattern[i])] = i
    # iterate over the whole text jumping over the "skip" chars
    while i <= n - m:
        skip = 0
        for j in xrange(m - 1, -1, -1):
            # if there is a mismatch
            if ord(pattern[j]) != ord(string[i + j]):
                # change the skip value (so it is always >= 1)
                skip = max(1, j - right[ord(string[i + j])])
                break
        if skip == 0:
            return i
        i += skip
    return -1


if __name__ == '__main__':
    string = 'aabacaababacaa'
    assert search(string, 'ababac') == 6