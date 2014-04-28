# -*- coding: utf-8 -*-


class RWaySt(object):
    """
    R-way trie symbol table.
    It runs O(L) for insertion and search hit.
    It may run sublinear time O(LogL) for searching if item was not found
    since it stops searching after the first symbol mismatch.
    Also it uses (R + 1)N space where R is a radix (256 for ASCII and 65535 for Unicode)
    which may use huge amount of space while processing a lot of items.
    """

    class Node(object):

        def __init__(self, value=None):
            self.value = value
            self.has_value = False
            # we use ASCII table by default
            self.children = [None] * 256

        def __getitem__(self, item):
            return self.children[item]

        def __setitem__(self, key, value):
            self.children[key] = value

    def __init__(self):
        self.root = self.Node()

    def __setitem__(self, key, value):

        def put(node, l, key, value):
            if node is None:
                node = self.Node()
            if l == len(key):
                node.value = value
                node.has_value = True
            else:
                c = ord(key[l])
                node[c] = put(node[c], l + 1, key, value)
            return node

        self.root = put(self.root, 0, key, value)

    def __getitem__(self, item):
        node = self.root
        for i in xrange(len(item)):
            node = node[ord(item[i])]
            if node is None:
                raise KeyError(item)
        if node.has_value:
            return node.value
        else:
            raise KeyError(item)

    def __delitem__(self, key):

        def delete(node, l, key):
            if node is None:
                raise KeyError(key)
            if l == len(key):
                node.value = None
                node.has_value = False
            else:
                c = ord(key[l])
                node[c] = delete(node[c], l + 1, key)
            # if all the children links are null - remove this node
            if not any(node.children) and not node.has_value:
                node = None
            return node

        children = delete(self.root, 0, key)
        self.root = children if children is not None else self.Node()

    def __iter__(self):
        """
        Iterate over items (key, value) pairs
        """
        def it(node, l, key):
            for n, node in enumerate(node.children):
                if node is not None:
                    if node.has_value:
                        yield (key + chr(n), node.value)
                    # Python 2 does not support "yield from" statement, so we do this:
                    for item in it(node, l + 1, key + chr(n)):
                        yield item

        return it(self.root, 0, '')




if __name__ == '__main__':

    st = RWaySt()
    st['s'] = 'S'
    st['shell'] = 'SHELL'
    st['she'] = 'SHE'
    assert st['s'] == 'S'
    assert st['shell'] == 'SHELL'
    del st['she']
    assert list(iter(st)) == [('s', 'S'), ('shell', 'SHELL')]
