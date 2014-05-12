# -*- coding: utf-8 -*-
from tries.ternary_tries import TernarySt
from bitio import BitReader, BitWriter


class LZW(object):
    """
    LZW data compression scans for repeated sequences from left to right
    and created short replacements for long prefixes.
    It runs O(N) and uses ternary search trie to store the prefixes.
    It does not store the actual symbol table because it may be restored
    during the extraction.
    Symbol table may grow large, so we use limits for it (4096 keys by default).
    """

    def __init__(self, file, radix=256, codeword_width=12, codeword_limit=4096):
        self.file = file
        self.radix = radix
        # bits to use to store one character
        self.codeword_width = codeword_width
        # number of codewords = 2^codeword_width
        self.codeword_limit = codeword_limit

    def compress(self, output_file):
        """
        Compress data from input file and write compressed data to the output file.
        """
        # create a ternary search trie and fill it with single ASCII characters
        st = TernarySt()
        for i in xrange(self.radix):
            st[chr(i)] = i
        code = self.radix + 1
        # read all the data from the input file (not optimal, but easy to code)
        data = self.file.read()
        bw = BitWriter(output_file)
        while len(data) > 0:
            lp = st.longest_prefix(data)
            # write the value of the prefix to output
            bw.writebits(st[lp], self.codeword_width)
            if len(lp) < len(data) and code < self.codeword_limit:
                # add new prefix to the symbol table
                st[data[:len(lp) + 1]] = code
                code += 1
            data = data[len(lp):]
        bw.writebits(self.radix, self.codeword_width)
        # output_file.close()

    def extract(self, output_file):
        """
        Restore the compressed data
        """
        # create a ternary search trie and fill it with single ASCII characters
        st = dict()
        for i in xrange(self.radix):
            st[i] = chr(i)
        i += 1  # i = 256 - reserved as an EOF signal
        br = BitReader(self.file)
        codeword = int(br.readbits(self.codeword_width))
        val = st[codeword]
        while True:
            # write unpacked value
            output_file.write(val)
            codeword = int(br.readbits(self.codeword_width))
            if codeword == self.radix:
                # EOF
                break
            if i == codeword:
                # special case hack (when we don't have the needed key in st, but we have just met in input)
                new_value = val + val[0]
            else:
                new_value = st[codeword]
            if i < self.codeword_limit:
                i += 1
                st[i] = val + new_value[0]
            val = new_value
        # output_file.close()


if __name__ == '__main__':
    from StringIO import StringIO

    original_file = StringIO('abracadabrabrabra')
    lzw = LZW(original_file)
    compressed_file = StringIO()
    lzw.compress(compressed_file)

    compressed_file.seek(0)
    lzw2 = LZW(compressed_file)
    restored_file = StringIO()
    lzw2.extract(restored_file)
    restored_file.seek(0)
    assert restored_file.read() == 'abracadabrabrabra'

