# -*- coding: utf-8 -*-


def lrs(string):
    """
    Finds the longest repeated string in a sequence (string)
    """
    # build suffixes
    suffixes = []
    for i in xrange(len(string)):
        suffixes.append(string[i:])
    # sort the suffixes
    suffixes.sort()

    def lcp(str1, str2):
        l = 0
        for i in xrange(min(len(str1), len(str2))):
            if str1[i] == str2[i]:
                l += 1
            else:
                break
        return l

    result = ''
    for n in xrange(len(suffixes) - 1):
        l = lcp(suffixes[n], suffixes[n + 1])
        if l > len(result):
            result = suffixes[n][:l]
    return result


if __name__ == '__main__':
    s = 'racaaghgnacaagtwodaceefsfffqqss'
    assert lrs(s) == 'acaag'
