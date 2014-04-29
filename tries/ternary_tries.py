# -*- coding: utf-8 -*-


class TernarySt(object):
    """
    Ternary trie symbol table.
    It runs O(L + lnL) for insertion and search hit.
    It runs O(lnL) for searching if item was not found.
    It uses only 4N space (each node has 3 pointer to its children)
    """

    class Node(object):

        def __init__(self, char=None, value=None):
            self.char = char
            self.value = value
            self.has_value = False
            # pointers to children nodes
            self.left = None
            self.middle = None
            self.right = None

    def __init__(self):
        self.root = None

    def __setitem__(self, key, value):

        def put(node, l, key, value):
            char = ord(key[l])
            if node is None:
                node = self.Node(char)
            if char < node.char:
                node.left = put(node.left, l, key, value)
            elif char > node.char:
                node.right = put(node.right, l, key, value)
            else:
                if l < len(key) - 1:
                    node.middle = put(node.middle, l + 1, key, value)
                else:
                    node.value = value
                    node.has_value = True

            return node

        self.root = put(self.root, 0, key, value)

    def __getitem__(self, item):
        node = self.get_node(self.root, 0, item)
        if node.has_value:
            return node.value
        else:
            raise KeyError(item)

    def get_node(self, node, l, item):
        char = ord(item[l])
        if node is None:
            raise KeyError(item)
        if char < node.char:
            return self.get_node(node.left, l, item)
        elif char > node.char:
            return self.get_node(node.right, l, item)
        else:
            if l < len(item) - 1:
                return self.get_node(node.middle, l + 1, item)
            else:
                return node

    def __delitem__(self, key):

        def delete(node, l, key):
            char = ord(key[l])
            if node is None:
                node = self.Node(char)
            if char < node.char:
                node.left = delete(node.left, l, key)
            elif char > node.char:
                node.right = delete(node.right, l, key)
            else:
                if l < len(key) - 1:
                    node.middle = delete(node.middle, l + 1, key)
                else:
                    node.value = None
                    node.has_value = False
            # if all the children links are null - remove this node
            if not any([node.left, node.middle, node.right]) and not node.has_value:
                node = None
            return node

        children = delete(self.root, 0, key)
        self.root = children if children is not None else self.Node()

    def __iter__(self):
        """
        Iterate over items (key, value) pairs
        """

        return self.collect(self.root, '')

    def items_with_prefix(self, prefix):
        """
        Items which keys start with the prefix
        """
        node = self.get_node(self.root, 0, prefix)
        # look at the middle subtree only (since only it has exact matches)
        return self.collect(node.middle, prefix)

    def collect(self, node, key):
        """
        Iterator over all the children nodes of the given node
        """
        if node is None:
            return
        # go over the left subtree
        for item in self.collect(node.left, key):
            yield item
        if node.has_value:
            yield (key + chr(node.char), node.value)
        # go over the middle subtree and add the current node char to the key variable
        for item in self.collect(node.middle, key + chr(node.char)):
            yield item
        # go over the right subtree
        for item in self.collect(node.right, key):
            yield item

    def longest_prefix(self, prefix):

        def search(node, prefix, length, d):
            if node is None:
                return length
            if node.has_value and ord(prefix[d]) == node.char:
                length = d + 1
            if len(prefix) - 1 == d:
                return length
            return max(search(node.left, prefix, length, d), search(node.middle, prefix, length, d + 1), search(node.right, prefix, length, d))


        return prefix[:search(self.root, prefix, 0, 0)]

if __name__ == '__main__':

    st = TernarySt()
    t = 'she sells sea shells by the shore'
    for n, word in enumerate(t.split()):
        st[word] = n

    del st['she']
    assert list(iter(st)) == [('by', 4), ('sea', 2), ('sells', 1), ('shells', 3), ('shore', 6), ('the', 5)]
    assert list(st.items_with_prefix('s')) == [('sea', 2), ('sells', 1), ('shells', 3), ('shore', 6)]
    assert st.longest_prefix('wood') == ''
    assert st.longest_prefix('shoreline') == 'shore'
    assert st.longest_prefix('seashore') == 'sea'
