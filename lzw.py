#!/usr/bin/python3

from utils_lzw import Trie, Array
import sys
import math
from bitstring import BitArray, BitStream

eFlag = False

# string -> (size, index array)
def lzw_encode(data):
    dic = Trie()
    w = ''
    ret = []
    for c in data:
        if dic.exists(w+c):
            w = w + c
        else:
            dic.add(w+c)
            #print(dic.code(w), w) #
            ret.append(dic.code(w))
            w = c
    #print(dic.code(w), w) #
    ret.append(dic.code(w))
    #print(dic.cnt) #
    return (dic.cnt, ret)

# (size, index array) -> string
def lzw_decode(dicSize, enc):
    dic = Array(dicSize)
    i = 0
    size = len(enc)
    ret = ""
    k = enc[i]
    i = i+1
    entry = dic.at(k)
    #print(entry) #
    ret = ret + entry
    w = entry
    while (i < size):
        k = enc[i]
        if dic.exists(k):
            entry = dic.at(k)
        elif k == dicSize:
            entry = w + w[0]
        else:
            raise ValueError("Invalid Code")
        #print(entry) #
        ret = ret + entry
        dic.add(w+entry[0])
        w = entry
        i = i+1
    return ret

# (size, index array) -> BitArray
def bitfy(dicSize, enc):
    ret = BitArray("uint:8=%s" % dicSize)
    bitSize = math.ceil(math.log(dicSize, 2))
    for d in enc:
        ret += BitArray("uint:%s=%s" % (bitSize, d))
    return ret

# BitArray -> (size, index array)
def unbitfy(encoding):
    encoding = BitStream(encoding)
    dicSize = encoding.read('uint:8')
    bitSize = math.ceil(math.log(dicSize, 2))
    bitLen = len(encoding)
    ret = []
    while encoding.pos < bitLen:
        ret.append(encoding.read("uint:%s" % bitSize))
    return (dicSize, ret)

if __name__ == "__main__":
    # parse arguments
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("infile", type=str, help="input file")
    parser.add_argument("encoding", type=str, help="encoded output file")
    parser.add_argument("outfile", type=str, help="decoded output file")
    parser.add_argument("-e", action="store_true", help="print on screen")
    args = parser.parse_args()

    # set flags
    eFlag = args.e

    # read input file
    data = None
    try:
        f = open(args.infile, 'r')
        data = f.read()
    except:
        print("Error opening infile:", sys.exc_info()[0])
    else:
        f.close()

    # lzw_encode
    dicSize, enc = lzw_encode(data)
    encoding = bitfy(dicSize, enc)

    # write encoded output file
    try:
        f = open(args.encoding, 'wb')
        encoding.tofile(f)
    except:
        print("Error opening encoding:", sys.exc_info()[0])
    else:
        f.close()

    # lzw_decode
    dicSize, enc = unbitfy(encoding)
    outfile = lzw_decode(dicSize, enc)

    # write decoded output file
    try:
        f = open(args.outfile, 'w')
        f.write(outfile)
    except:
        print("Error opening outfile:", sys.exc_info()[0])
    else:
        f.close()
