# -*- coding: utf-8 -*-
from collections import defaultdict
from Queue import PriorityQueue
from bitio import BitReader, BitWriter


class Huffman(object):
    """
    Huffman prefix-free data compression.
    It runs O(N + RlogR) and uses binary tries to store the prefixes.
    """

    class Node(object):
        """
        A node in the Huffman binary trie.
        """

        def __init__(self, char, frequency, left=None, right=None):
            self.char = char
            self.left = left
            self.right = right
            self.frequency = frequency

        @property
        def is_leaf(self):
            return self.left is None and self.right is None

        def __cmp__(self, other):
            return self.frequency - other.frequency

        def __repr__(self):
            return chr(self.char) if self.char > 0 else '<empty>'

    def __init__(self, file, radix=256):
        self.file = file
        self.radix = radix

    def compress(self, output_file):
        """
        Compress data from input file and write compressed data to the output file.
        """
        # read input and count chars
        freq = defaultdict(int)
        length = 0
        while True:
            # read one char from a file
            char = self.file.read(1)
            if char:
                length += 1
                freq[ord(char)] += 1
            else:
                # EOF
                break

        # build Huffman trie
        root = self._build_trie(freq)
        # build symbol table for chars and their binary representation
        st = dict()
        self._build_code(st, root, '')
        bw = BitWriter(output_file)
        # write the Huffman trie binary representation to the file
        self._write_trie(root, bw)
        # write number of bytes in original uncompressed message
        bw.writebits(length, 8)
        # use Huffman code to encode input
        for i in xrange(length):
            self.file.seek(i)
            code = st[ord(self.file.read(1))]
            for c in code:
                if c == '0':
                    bw.writebit(False)
                else:
                    bw.writebit(True)
                    # close the output file
                    # output_file.close()

    def extract(self, output_file):
        """
        Restore the compressed data
        """
        br = BitReader(self.file)
        root = self._read_trie(br)
        # number of bytes to write
        length = int(br.readbits(8))
        bw = BitWriter(output_file)
        # decode using the Huffman trie
        for i in xrange(length):
            node = root
            while not node.is_leaf:
                bit = br.readbit()
                if bit:
                    node = node.right
                else:
                    node = node.left
            # write the character to output
            bw.writebits(node.char, 8)
            # output_file.close()

    def _read_trie(self, br):
        bit = br.readbit()
        if bit:
            # it is a leaf, so read the next 8 bits and create the node
            return self.Node(int(br.readbits(8)), -1)
        else:
            # it is an intermediary node
            return self.Node(0, -1, self._read_trie(br), self._read_trie(br))

    def _write_trie(self, node, bw):
        if node.is_leaf:
            # put "1" at the beginning of the leaf node char
            bw.writebit(True)
            # put node character in 8 bits representation
            bw.writebits(node.char, 8)
        else:
            # put "0" for the intermediary node (as a delimiter)
            bw.writebit(False)
            self._write_trie(node.left, bw)
            self._write_trie(node.right, bw)

    def _build_trie(self, frequency):
        """
        Build a binary trie and return its root node
        """
        nodes = PriorityQueue()
        for char, freq in frequency.iteritems():
            if freq > 0:
                nodes.put(self.Node(char, freq))

        # merge two smallest tries
        while nodes.qsize() > 1:
            left = nodes.get()
            right = nodes.get()
            parent = self.Node(0, left.frequency + right.frequency, left, right)
            nodes.put(parent)

        # return the root node
        return nodes.get()

    def _build_code(self, st, node, s):
        """
        Build a symbol table from a Huffman trie.
        Each key has a binary value.
        """
        if not node.is_leaf:
            self._build_code(st, node.left, s + '0')
            self._build_code(st, node.right, s + '1')
        else:
            st[node.char] = s


if __name__ == '__main__':
    from StringIO import StringIO

    original_file = StringIO('abracadabra!')
    h = Huffman(original_file)
    compressed_file = StringIO()
    h.compress(compressed_file)

    compressed_file.seek(0)
    h2 = Huffman(compressed_file)
    restored_file = StringIO()
    h2.extract(restored_file)
    restored_file.seek(0)
    assert restored_file.read() == 'abracadabra!'

