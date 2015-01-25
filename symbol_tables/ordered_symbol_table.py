# -*- coding: utf-8 -*-
from abstract_symbol_table import AbstractSymbolTable


class OrderedSymbolTable(AbstractSymbolTable):
    """
    Symbol tables implementation with binary search
    It goes LogN time for search, but N for insertion
    """
    def __init__(self):
        self.keys = []
        self.values = []

    def __getitem__(self, item):
        if self:
            if isinstance(item, slice):
                # slicing support
                result = []
                for x in xrange(self.search(item.start), self.search(item.stop) + 1, item.step if item.step else 1):
                    result.append((self.keys[x], self.values[x]))
                return result
            else:
                return self.values[self.search(item)]
        else:
            raise IndexError('Symbol table is empty')

    def __contains__(self, item):
        try:
            self[item]
            return True
        except KeyError:
            return False

    def __setitem__(self, key, value):
        """
        Place new item in ordered place using kind of insertion sort
        Since we need to keep all keys in order
        """
        if len(self) == 0:
            self.keys.append(key)
            self.values.append(value)
        else:
            i = 0
            n = len(self)
            while i < n:
                if key < self.keys[i]:
                    # append this item to the end
                    self.keys.append(self.keys[i])
                    self.values.append(self.values[i])
                    # replace the item with the new one
                    self.keys[i] = key
                    self.values[i] = value
                    break
                elif key == self.keys[i]:
                    # just update the value
                    self.values[i] = value
                    return
                i += 1

            # if new item was inserted
            if len(self) > n:
                # put the replaced item in the right place
                k = len(self) - 1
                while k > 0 and self.keys[k] < self.keys[k - 1]:
                    self.keys[k], self.keys[k - 1] = self.keys[k - 1], self.keys[k]
                    k -= 1
            else:
                # insert the new key to the end since it is the biggest one
                self.keys.append(key)
                self.values.append(value)

    def __delitem__(self, key):
        k = self.search(key)
        del self.keys[k]
        del self.values[k]

    def select(self, index):
        """
        Select n-th item from symbol table
        """
        try:
            return self.keys[index]
        except IndexError:
            raise KeyError(repr(index))

    def min(self):
        """
        Returns the minimal key
        """
        return self.keys[0]

    def max(self):
        """
        Returns the max key
        """
        return self.keys[len(self) - 1]

    def floor(self, key):
        """
        Search for the previous closest key
        """
        lo = 0
        hi = len(self) - 1
        mid = lo + (hi - lo) / 2
        while lo <= hi:
            mid = lo + (hi - lo) / 2
            if key > self.keys[mid]:
                lo = mid + 1
            elif key < self.keys[mid]:
                hi = mid - 1
            else:
                return self.keys[mid]

        if mid > 0:
            return self.keys[mid - 1]
        else:
            raise KeyError(repr(key))

    def ceil(self, key):
        """
        Search for the next closest key
        """
        lo = 0
        hi = len(self) - 1
        mid = lo + (hi - lo) / 2
        while lo <= hi:
            mid = lo + (hi - lo) / 2
            if key > self.keys[mid]:
                lo = mid + 1
            elif key < self.keys[mid]:
                hi = mid - 1
            else:
                return self.keys[mid]

        if key < self.keys[mid]:
            return self.keys[mid]
        else:
            raise KeyError(repr(key))

    def size(self, key_start, key_stop):
        """
        Returns number of items between start and stop keys (included)
        """
        start = self.ceil(key_start)
        stop = self.floor(key_stop)
        return len(self[start:stop])

    def search(self, key):
        """
        Binary search for a key position in the key list
        """
        lo = 0
        hi = len(self) - 1
        while lo <= hi:
            mid = lo + (hi - lo) / 2
            if key > self.keys[mid]:
                lo = mid + 1
            elif key < self.keys[mid]:
                hi = mid - 1
            else:
                return mid

        raise KeyError(repr(key))

    def __nonzero__(self):
        return len(self.keys) > 0

    def __len__(self):
        return len(self.keys)

    def __iter__(self):
        return iter(self.keys)

if __name__ == '__main__':

    s = OrderedSymbolTable()
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
    # delete item and rearrange the tree
    del s['e']
    assert s.keys == ['a', 'c', 'h', 'm', 'r', 's', 'x', 'y', 'z']