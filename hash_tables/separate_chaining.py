# -*- coding: utf-8 -*-


class SeparateChainingHashST(object):
    """
    Separate chaining hash symbol table implementation
    """

    class Node(object):

        def __init__(self, key, value):
            self.key = key
            self.value = value
            self.next = None

        def __repr__(self):
            return '<Node({}, {})>'.format(self.key, self.value)

    def __init__(self):
        # it should be a list, but python lists do not support __setitem__
        # which we need to set an item with a specific key
        self.chains = {}

    def positive_hash(self, key):
        """
        Compute positive hash (some hashes may be negative)
        """
        return hash(key) & 0x7fffffff

    def __setitem__(self, key, value):
        phash = self.positive_hash(key)
        try:
            node = self.chains[phash]
            while node is not None:
                if node.key == key:
                    # update existing node value
                    node.value = value
                    return
                node = node.next
            node.next = self.Node(key, value)
        except KeyError:
            # no such hash is found - create new node
            self.chains[phash] = self.Node(key, value)
            return

    def __getitem__(self, item):
        phash = self.positive_hash(item)
        try:
            node = self.chains[phash]
        except KeyError:
            # no such hash -> no such item
            raise KeyError(repr(item))

        while node is not None:
            if node.key == item:
                return node.value
            node = node.next
        raise KeyError(repr(item))

    def __delitem__(self, key):
        phash = self.positive_hash(key)
        try:
            node = self.chains[phash]
        except KeyError:
            # no such hash -> no such item
            raise KeyError(repr(key))

        while node is not None:
            if node.key == key:
                self.chains[phash] = node.next
                return
            elif node.next and node.next.key == key:
                if node.next.next:
                    node.next = node.next.next
                else:
                    node.next = None
                return
            node = node.next
        raise KeyError(repr(key))


if __name__ == "__main__":
    st = SeparateChainingHashST()
    st['ca'] = 'ca'
    st['ac'] = 'ac'
    st['aca'] = 'aca'
    del st['ca']
    assert st['ac'] == 'ac'

