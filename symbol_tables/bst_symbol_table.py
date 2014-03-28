# -*- coding: utf-8 -*-
from Queue import Queue
from copy import copy
from abstract_symbol_table import AbstractSymbolTable


class BinarySearchTreeSymbolTable(AbstractSymbolTable):
    """
    Symbol table with binary search tree
    """

    class Node(object):

        def __init__(self, key, value):
            self.key = key
            self.value = value
            self.left, self.right = None, None
            self.count = 1

        def __repr__(self):
            return u'<Node({key}, {value})>'.format(key=repr(self.key), value=repr(self.value))

    def __init__(self):
        self.root = None

    def __setitem__(self, key, value):

        def put(node, key, value):
            """
            Recursively iterate through nodes from top to bottom
            and create new node in the correct place.
            """
            if node is None:
                # create new node
                return self.Node(key, value)

            # search in binary tree
            if key < node.key:
                node.left = put(node.left, key, value)
            elif key > node.key:
                node.right = put(node.right, key, value)
            else:
                node.value = value
            node.count = self._size(node.left) + 1 + self._size(node.right)
            return node

        self.root = put(self.root, key, value)

    def __getitem__(self, item):
        node = self.root

        # perform a binary search
        while node is not None:
            if item < node.key:
                node = node.left
            elif item > node.key:
                node = node.right
            else:
                return node.value

        raise IndexError('Item was not found')

    def __contains__(self, item):
        try:
            self[item]
            return True
        except IndexError:
            return False

    def __delitem__(self, key):
        """
        Provides this: del st['apple']
        Hibbard deletion method
        """
        def delete(node, key):
            if node is None:
                return
            if key < node.key:
                node.left = delete(node.left, key)
            elif key > node.key:
                node.right = delete(node.right, key)
            else:
                if node.right is None:
                    # no right child
                    return node.left
                if node.left is None:
                    # no left child
                    return node.right
                # make a copy of what is gonna be removed
                t = copy(node)
                # replace it with the min node to the right
                node = self.min(node.right, True)
                # copy back the right sub-tree with the min node removed
                node.right = self._del_min(t.right)
                # copy back the original left subtree
                node.left = t.left
            # update count number (since this line of code is called recursively - each node will be updated)
            node.count = self._size(node.left) + self._size(node.right) + 1
            return node

        if key in self:
            return delete(self.root, key)
        else:
            raise IndexError('Key was not found')

    def del_min(self):
        """
        Delete the min key
        """
        self._del_min(self.root)

    def _del_min(self, node):
        if node.left is None:
            return node.right
        node.left = self._del_min(node.left)
        node.count = 1 + self._size(node.left) + self._size(node.right)
        return node

    def min(self, node=None, return_node=False):
        """
        Returns the minimal key.
        The minimal key is in the left most node in the tree
        """
        if node is None:
            node = self.root
        while True:
            # find the most left node
            if node.left is not None:
                node = node.left
            else:
                break

        if return_node:
            # if we need node instead of the key (used in __delitem__)
            return node
        else:
            return node.key

    def max(self, node=None, return_node=False):
        """
        Returns the max key
        The max key is in the right most node in the tree
        """
        if node is None:
            node = self.root
        while True:
            # find the most right node
            if node.right is not None:
                node = node.right
            else:
                break

        if return_node:
            # if we need node instead of the key
            return node
        else:
            return node.key

    def floor(self, key):
        """
        Search for the previous closest key
        """
        def _floor(node, key):
            if node is None:
                return

            if key > node.key:
                right = _floor(node.right, key)
                if right is not None:
                    return right
                else:
                    return node
            elif key < node.key:
                return _floor(node.left, key)

            return node

        node = _floor(self.root, key)
        if node is not None:
            return node.key
        else:
            raise IndexError('Floor key is out of range')

    def ceil(self, key):
        """
        Search for the next closest key
        """
        def _ceil(node, key):
            if node is None:
                return

            if key < node.key:
                left = _ceil(node.left, key)
                if left is not None:
                    return left
                else:
                    return node
            elif key > node.key:
                return _ceil(node.right, key)

            return node

        node = _ceil(self.root, key)
        if node is not None:
            return node.key
        else:
            raise IndexError('Ceil key is out of range')

    def rank(self, key):
        """
        How many keys are lower than 'key'?
        """
        def _rank(node, key):
            if node is None:
                return 0
            if key > node.key:
                return 1 + self._size(node.left) + _rank(node.right, key)
            elif key < node.key:
                return _rank(node.left, key)
            else:
                return self._size(node.left)
            
        return _rank(self.root, key)

    def __nonzero__(self):
        """
        Boolean test
        """
        return len(self) > 0

    def __len__(self):
        """
        Returns number of items in the symbol table
        """
        return self._size(self.root)

    def _size(self, node):
        return 0 if node is None else node.count

    def __iter__(self):
        """
        Iterate over all nodes keys in the tree in the natural order
        """
        return iter(self._inorder(self.root))

    def _inorder(self, node=None):
        """
        Traverse the tree in natural order
        """
        if node is None:
            return []

        # recursively traverse through the left subtree
        left = self._inorder(node.left)
        # recursively traverse through the right subtree
        right = self._inorder(node.right)
        return left + [node.key] + right

    def keys(self):
        """
        Returns the breadth-first traversed keys (level by level)
        """
        return [x.key for x in self.nodes()]

    def nodes(self):
        """
        Returns the breadth-first traversed nodes (level by level)
        """
        q = Queue()
        q.put(self.root)
        keys = []
        while not q.empty():
            node = q.get()
            if node.left:
                q.put(node.left)
            if node.right:
                q.put(node.right)
            keys.append(node)
        return keys

    def height(self):
        """
        Calculate a height of the tree
        """

        def _height(node):
            if node is None:
                return 0

            left = _height(node.left)
            right = _height(node.right)
            return 1 + max(left, right)

        return _height(self.root) - 1


if __name__ == '__main__':

    s = BinarySearchTreeSymbolTable()
    s['s'] = 'rr'
    s['e'] = 'ee'
    s['x'] = 'xx'
    s['a'] = 'cc'
    s['r'] = 'mm'
    s['y'] = 'y'
    s['z'] = 'z'
    s['c'] = 'ss'
    s['h'] = 'aa'
    s['m'] = 'hh'

    assert s.height() == 4
    # natural order
    assert list(iter(s)) == ['a', 'c', 'e', 'h', 'm', 'r', 's', 'x', 'y', 'z']
    # breadth-first order
    assert s.keys() == ['s', 'e', 'x', 'a', 'r', 'y', 'c', 'h', 'z', 'm']
    # delete item and rearrange the tree
    del s['e']
    assert s.keys() == ['s', 'h', 'x', 'a', 'r', 'y', 'c', 'm', 'z']