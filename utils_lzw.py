#!/usr/bin/python3

alphabet = "\
abcdefghijklmnopqrstuvwxyz\
ABCDEFGHIJKLMNOPQRSTUVWXYZ\
0123456789?! ,.:;\n"

class Trie():
    """Trie used for encoding"""
    def __init__(self):
        self.root = {}
        self.cnt = 0
        #self.dic = {} #
        for c in alphabet:
            self.root[c] = (self.cnt, {})
            #self.dic[c] = self.cnt #
            self.cnt = self.cnt + 1

    def exists(self, string):
        '''
        return string in self.dic
        '''
        curr = self.root
        for c in string:
            if c in curr:
                code, curr = curr[c]
            else:
                return False
        return True

    def add(self, string):
        '''
        self.dic[string] = self.cnt
        self.cnt = self.cnt + 1
        return None
        '''
        curr = self.root
        for c in string[:-1]:
            if c in curr:
                code, curr = curr[c]
            else:
                raise ValueError("No previous pattern in trie")
        if string[-1] in curr:
            raise ValueError("Pattern already in trie")
        curr[string[-1]] = (self.cnt, {})
        self.cnt = self.cnt + 1
        return None

    def code(self, string):
        '''
        return self.dic[string]
        '''
        curr = self.root
        code = None
        for c in string:
            if c in curr:
                code, curr = curr[c]
            else:
                raise KeyError(string)
        if code == None:
            raise KeyError(string)
        return code

class Array():
    """Array used for decoding"""
    def __init__(self, size):
        self.arr = [None for i in range(size)]
        self.cnt = 0
        self.size = size
        for c in alphabet:
            self.arr[self.cnt] = c
            self.cnt = self.cnt + 1

    def at(self, k):
        return self.arr[k]

    def exists(self, k):
        return k < self.cnt

    def add(self, string):
        self.arr[self.cnt] = string
        self.cnt = self.cnt + 1
        return None
