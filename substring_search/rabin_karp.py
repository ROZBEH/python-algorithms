# -*- coding: utf-8 -*-


def search(string, pattern):
    """
    Rabin-Karp substring search algorithm based on hashing substrings.
    It runs O(7N) on average and has no backup.
    """
    m = len(pattern)
    n = len(string)
    # random long prime
    q = 997
    # radix
    r = 256

    def hash(s):
        h = 0
        for i in xrange(len(s)):
            h = (r * h + ord(s[i])) % r
        return h

    rm = 1
    # precompute R^(M-1)
    for i in xrange(m):
        rm = (r * rm) % q
    pattern_hash = hash(pattern)
    string_hash = hash(string)
    if pattern_hash == string_hash:
        # match found: pattern and given text are the same
        return 0
    for i in xrange(m, n):
        string_hash = (string_hash + q - rm * ord(string[i-m]) % q) % q
        string_hash = (string_hash * r + ord(string[i])) % q
        if pattern_hash == string_hash:
            return i - m + 1
    return -1


if __name__ == '__main__':
    string = 'aabacaababacaa'
    # TODO: fix the algorithm hash calculation since smth goes wrong
    assert search(string, 'ababac') == 6