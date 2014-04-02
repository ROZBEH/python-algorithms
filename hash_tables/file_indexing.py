# -*- coding: utf-8 -*-
import re


class Finder(object):
    """
    Build an index of the given text files to perform a rapid search within the given files
    """
    def __init__(self, symbol_table_class):
        self.data = symbol_table_class()

    def add_to_index(self, filename):
        with open(filename) as fp:
            for word in re.split('\W+', fp.read()):
                word = word.lower()
                if word in self.data:
                    self.data[word].add(filename)
                else:
                    self.data[word] = set([filename])

    def find(self, keyword):
        try:
            return self.data[keyword.lower()]
        except KeyError:
            return None

if __name__ == '__main__':
    import os
    from separate_chaining import SeparateChainingHashST

    finder = Finder(SeparateChainingHashST)
    # find all .py files and add them to an index
    for root, dirs, files in os.walk(os.path.curdir):
        pyfiles = [f for f in files if f.endswith('.py')]
        for p in pyfiles:
            finder.add_to_index(os.path.join(root, p))

    print finder.find('todo')