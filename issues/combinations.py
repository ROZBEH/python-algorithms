# -*- coding: utf-8 -*-


def xcombinations(items, length):
    """
    Returns generator with all possible combinations for the given combination length
    """
    if length > 0:
        for i in xrange(len(items)):
            for cs in xcombinations(items[:i] + items[i + 1:], length - 1):
                yield [items[i]] + cs
    else:
        yield []


def combinations(items, length):
    """
    Returns all possible combinations for the given combination length
    """
    result = []
    if length > 0:
        for i in xrange(len(items)):
            if length > 1:
                # search for combinations with length > 0 only
                for cs in combinations(items[:i] + items[i + 1:], length - 1):
                    result.append([items[i]] + cs)
            else:
                result.append([items[i]])
    return result


def xucombinations(items, length):
    """
    Returns generator with unique combinations for the given combination length
    """
    if length > 0:
        for i in xrange(len(items)):
            for cs in xucombinations(items[i + 1:], length - 1):
                yield [items[i]] + cs
    else:
        yield []


def ucombinations(items, length):
    """
    Returns unique combinations for the given combination length
    """
    result = []
    if length > 0:
        for i in xrange(len(items)):
            if length > 1:
                # search for combinations with length > 0 only
                for cs in ucombinations(items[i + 1:], length - 1):
                    result.append([items[i]] + cs)
            else:
                result.append([items[i]])
    return result


def xselections(items, length):
    """
    Returns generator with selections for the given length
    """
    if length > 0:
        for i in xrange(len(items)):
            for ss in xucombinations(items, length - 1):
                yield [items[i]] + ss
    else:
        yield []


def xpermutations(items):
    """
    Returns generator of items permutations
    """
    return xcombinations(items, len(items))

if __name__ == '__main__':
    l = [1, 2, 3, 4]

    print 'All possible combinations of ', l, ':\n'
    cms = combinations(l, 3)
    print cms
    print 'Number of all possible combinations:', len(cms)

    print 'All possible combinations of', l, ' with generator:\n'
    for x in xcombinations(l, 3):
        print x

    assert combinations(l, 3) == list(xcombinations(l, 3))

    print 'Unique combinations of ', l, ':\n'
    ucms = ucombinations(l, 3)
    print ucms
    print 'Number of unique combinations:', len(ucms)

    print 'Unique combinations of', l, ' with generator:\n'
    for x in xucombinations(l, 3):
        print x

    assert ucombinations(l, 3) == list(xucombinations(l, 3))

    print 'Selections of', l, ' with generator:\n'
    for x in xselections(l, 3):
        print x

    print 'Permutations of', l, ' with generator:\n'
    for x in xpermutations(l):
        print x