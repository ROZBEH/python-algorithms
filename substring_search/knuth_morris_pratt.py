# -*- coding: utf-8 -*-


def search(string, pattern):
    """
    Knuth-Morris-Pratt substring search.
    It uses finite state machine to detect symbol matches.
    If we get to the last state then this is the whole match of the string.
    Each iteration over a pattern's symbol we move over the states of the machine.
    Overall run-time analysis: O(N+M) where N is the length of the string (haystack)
    and M is the length of the pattern. Brute-force algorithm runs O(N*M).
    """
    # radix = number of the unique symbols (it may be set to 256 manually if needed)
    r = len(set(pattern))
    def _ord(s):
        return ord(s) % r

    def build_dfa(pattern):
        """
        This function builds a dfa look up table
        where all the transitions between states a stored.
        The size is R*len(pattern)
        """
        # create R * M array
        dfa = [[0] * len(pattern)]
        for q in xrange(r - 1):
            dfa.append(dfa[q][:])
        dfa[_ord(pattern[0])][0] = 1
        x = 0
        for i in xrange(1, len(pattern)):
            for c in xrange(r):
                # copy mismatch cases
                dfa[c][i] = dfa[c][x]
            # set match case
            dfa[_ord(pattern[i])][i] = i + 1
            # update restart state
            x = dfa[_ord(pattern[i])][x]
        return dfa

    dfa = build_dfa(pattern)
    n = len(string)
    m = len(pattern)
    i = j = 0
    while i < n and j < m:
        j = dfa[_ord(string[i])][j]
        i += 1
    # if the state is the last - it is a complete match
    if j == m:
        return i - m
    else:
        return -1

if __name__ == '__main__':
    string = 'aabacaababacaa'
    assert search(string, 'ababac') == 6