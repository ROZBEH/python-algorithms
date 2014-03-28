# -*- coding: utf-8 -*-
from copy import copy
from bst_symbol_table import BinarySearchTreeSymbolTable


class RedBlackBinarySearchTreeSymbolTable(BinarySearchTreeSymbolTable):
    """
    Symbol table with red-black binary search tree
    Some code is derived from the binary search tree
    Full implementation here: http://algs4.cs.princeton.edu/33balanced/RedBlackBST.java.html
    """

    class Node(object):

        RED = True
        BLACK = False

        def __init__(self, key, value, color):
            self.key = key
            self.value = value
            self.left, self.right = None, None
            self.color = color
            self.count = 1

        def __repr__(self):
            return u'<Node({key}, {value}, {color})>'.format(key=repr(self.key), value=repr(self.value),
                                                             color='RED' if self.color else 'BLACK')

    def _is_red(self, node):
        """
        Check if the node is red
        We can not put this code into Node class since sometimes we need to check the color of None nodes
        """
        if node is None:
            return False
        return node.color == self.Node.RED

    def _rotate_left(self, node):
        """
        Orient a (temporarily) right-leaning red link to lean left
        This method maintains the perfect black balance of the tree
        """
        assert node is not None and self._is_red(node.right)
        x = copy(node.right)
        node.right = x.left
        x.left = node
        x.color = node.color
        node.color = self.Node.RED
        return x

    def _rotate_right(self, node):
        """
        Orient a (temporarily) left-leaning red link to lean right
        This method maintains the perfect black balance of the tree
        """
        assert node is not None and self._is_red(node.left)
        x = copy(node.left)
        node.left = x.right
        x.right = node
        x.color = node.color
        node.color = self.Node.RED
        return x

    def _flip_colors(self, node):
        """
        Recolor to split a temporary 4-node
        """
        # node must have opposite color of its two children
        assert node is not None
        assert (not self._is_red(node) and self._is_red(node.left) and self._is_red(node.right)) or (
            self._is_red(node) and not self._is_red(node.left) and not self._is_red(node.right))

        node.color = self.Node.RED
        node.left.color = self.Node.BLACK
        node.right.color = self.Node.BLACK

    def __setitem__(self, key, value):

        def put(node, key, value):
            """
            Recursively iterate through nodes from top to bottom
            and create new node in the correct place.
            """
            if node is None:
                # create new node at the bottom (all new nodes are RED by default)
                return self.Node(key, value, self.Node.RED)

            # search in binary tree
            if key < node.key:
                node.left = put(node.left, key, value)
            elif key > node.key:
                node.right = put(node.right, key, value)
            else:
                node.value = value

            # further cases are reduced from one to another
            # so they may follow after each other at the worst case
            if self._is_red(node.right) and not self._is_red(node.left):
                # right link can not be RED - rotate it to the left
                # but only if the left link is black (lean left)
                node = self._rotate_left(node)
            if self._is_red(node.left) and self._is_red(node.left.left):
                # two consecutive left links can not be RED
                # we need to balance a 4-node by rotating the node to the right
                node = self._rotate_right(node)
            if self._is_red(node.left) and self._is_red(node.right):
                # both links can not be RED - flip colors so that both of these two links become BLACK
                # and the current node becomes RED
                self._flip_colors(node)
            node.count = self._size(node.left) + 1 + self._size(node.right)

            return node

        self.root = put(self.root, key, value)
        self.root.color = self.Node.BLACK

    def __delitem__(self, key):
        """
        Provides this: del st['apple']
        """

        def delete(node, key):
            if node is None:
                return
            if key < node.key:
                if not self._is_red(node.left) and not self._is_red(node.left.left):
                    print node, node.left, node.left.left, self._is_red(node.left), self._is_red(node.left.left)
                    node = self._move_red_left(node)
                node.left = delete(node.left, key)
            else:
                if self._is_red(node.left):
                    node = self._rotate_right(node)
                if key == node.key and node.right is None:
                    return
                if not self._is_red(node.right) and not self._is_red(node.right.left):
                    node = self._move_red_right(node)
                if key == node.key:
                    x = self.min(node.right, True)
                    node.key = x.key
                    node.value = x.value
                    node.right = self._del_min(node.right)
                else:
                    node.right = delete(node.right, key)
            return self._balance(node)

        # if both children of root are black, set root to red temporarily
        if not (self._is_red(self.root.left) and self._is_red(self.root.right)):
            self.root.color = self.Node.RED

        self.root = delete(self.root, key)
        if self:
            self.root.color = self.Node.BLACK

    def del_min(self):
        """
        Delete the min key
        """
        # if both children of root are black, set root to red temporarily
        if not self._is_red(self.root.left) and not self._is_red(self.root.right):
            self.root.color = self.Node.RED

        self.root = self._del_min(self.root)
        if self:
            self.root.color = self.Node.BLACK

    def _del_min(self, node):
        if node.left is None:
            return node.right
        # if two consecutive left links are black - mode node to the left
        if not self._is_red(node.left) and not self._is_red(node.left.left):
            node = self._move_red_left(node)

        node.left = self._del_min(node.left)
        node.count = 1 + self._size(node.left) + self._size(node.right)
        return self._balance(node)

    def _move_red_left(self, node):
        """
        Assuming that node is red and both node.left and node.left.left
        are black, make node.left or one of its children red.
        """
        assert node is not None
        assert self._is_red(node) and not self._is_red(node.left) and not self._is_red(node.left.left)

        self._flip_colors(node)
        if self._is_red(node.right.left):
            node.right = self._rotate_right(node.right)
            node = self._rotate_left(node)

        return node

    def _move_red_right(self, node):
        """
        Assuming that node is red and both node.right and node.right.left
        are black, make node.right or one of its children red.
        """
        assert node is not None
        assert self._is_red(node) and not self._is_red(node.right) and not self._is_red(node.right.left)

        if self._is_red(node.left.left):
            # TODO: fix assertion fail...
            node = self._rotate_right(node)

        return node

    def _balance(self, node):
        """
        Restore red-black tree invariant
        """
        assert node is not None
        if self._is_red(node.right):
            node = self._rotate_left(node)
        if self._is_red(node.left) and self._is_red(node.left.left):
            node = self._rotate_right(node)
        if self._is_red(node.left) and self._is_red(node.right):
            self._flip_colors(node)

        node.count = 1 + self._size(node.left) + self._size(node.right)
        return node


if __name__ == '__main__':
    s = RedBlackBinarySearchTreeSymbolTable()
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

    # natural order
    assert list(iter(s)) == ['a', 'c', 'e', 'h', 'm', 'r', 's', 'x', 'y', 'z']
    # breadth-first order
    assert s.keys() == ['s', 'm', 'y', 'e', 'r', 'x', 'z', 'c', 'h', 'a']
    # delete item and rearrange the tree
    del s['e']
    assert s.keys() == ['s', 'm', 'y', 'h', 'r', 'x', 'z', 'c', 'a']