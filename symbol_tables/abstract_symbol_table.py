# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod


class AbstractSymbolTable(object):
    """
    Abstract symbol table class.
    Defines interface methods like python's dict has
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def __getitem__(self, item):
        """
        Provides this: print st['apple']
        """
        pass

    @abstractmethod
    def __setitem__(self, key, value):
        """
        Provides this: st['apple'] = 'fruit'
        """
        pass

    @abstractmethod
    def __delitem__(self, key):
        """
        Provides this: del st['apple']
        """
        pass

    @abstractmethod
    def select(self, index):
        """
        Selects n-th item from symbol table
        """
        pass

    @abstractmethod
    def min(self):
        """
        Returns the minimal key
        """
        pass

    @abstractmethod
    def max(self):
        """
        Returns the max key
        """
        pass

    @abstractmethod
    def floor(self, key):
        """
        Search for the previous closest key
        """
        pass

    @abstractmethod
    def ceil(self, key):
        """
        Search for the next closest key
        """
        pass

    @abstractmethod
    def __nonzero__(self):
        """
        Boolean test
        """
        pass

    @abstractmethod
    def __len__(self):
        """
        Returns number of items in the symbol table
        """
        pass

    @abstractmethod
    def __iter__(self):
        pass