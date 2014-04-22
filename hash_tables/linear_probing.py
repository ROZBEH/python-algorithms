# -*- coding: utf-8 -*-


class LinearProbingHashST(object):
    """
    Linear probing hash symbol table implementation
    """

    def __init__(self, size):
        self.size = size
        self.keys = [None] * size
        self.values = [None] * size

    def positive_hash(self, key):
        """
        Compute positive hash (some hashes may be negative)
        """
        return hash(key) & 0x7fffffff % self.size

    def __setitem__(self, key, value):
        phash = self.positive_hash(key)
        if self.keys[phash] is None:
            self.keys[phash] = key
            self.values[phash] = value
        else:
            index = phash + 1 if phash < self.size - 1 else 0
            while self.keys[index] is not None:
                if index == phash:
                    raise MemoryError('Table is full')
                index = index + 1 if index < self.size - 1 else 0
            self.keys[index] = key
            self.values[index] = value

    def __getitem__(self, item):
        phash = self.positive_hash(item)
        index = phash
        while self.positive_hash(self.keys[index]) != phash:
            if index == phash:
                raise KeyError(repr(item))
            index = phash + 1 if phash < self.size - 1 else 0
        return self.values[index]

    def __delitem__(self, key):
        # TODO: implement this
        raise NotImplemented

    def __contains__(self, item):
        try:
            self[item]
            return True
        except KeyError:
            return False


if __name__ == "__main__":
    st = LinearProbingHashST(10)
    st['a'] = st.positive_hash('a')
    st['e'] = st.positive_hash('e')
    st['y'] = st.positive_hash('y')
    st['b'] = st.positive_hash('b')
    st['r'] = st.positive_hash('r')
    st['v'] = st.positive_hash('v')
    st['q'] = st.positive_hash('q')
    st['t'] = st.positive_hash('t')
    st['i'] = st.positive_hash('i')
    st['o'] = st.positive_hash('o')
    assert st['q'] == 0