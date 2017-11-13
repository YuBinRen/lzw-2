#!/usr/bin/python3

from utils_lzw import Trie, Array
import sys
import math
import time
from subprocess import call
from bitstring import BitArray, BitStream

# encode string data into index array
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

# decode index array to string data
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

# turn index array to bit array
# (size, index array) -> BitArray
def bitfy(dicSize, enc):
    ret = BitArray("uint:8=%s" % dicSize)
    bitSize = math.ceil(math.log(dicSize, 2))
    for d in enc:
        ret += BitArray("uint:%s=%s" % (bitSize, d))
    return ret

# turn bit array to index array
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

def print40(buf):
    chars_per_line = 40
    for i in range(0, len(buf), chars_per_line):
        print(buf[i:i+chars_per_line])


if __name__ == "__main__":
    # parse arguments
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("infile", type=str, help="input file")
    parser.add_argument("encoding", type=str, help="encoded output file")
    parser.add_argument("outfile", type=str, help="decoded output file")
    parser.add_argument("-e", action="store_true", help="print on screen")
    args = parser.parse_args()

    # read input file
    data = None
    try:
        f = open(args.infile, 'r')
        data = f.read()
    except:
        print("Error opening infile:", sys.exc_info()[0])
    else:
        f.close()

    # print input for encoding
    if args.e:
        print("## Input of Encoding:")
        print('-' * 40)
        print40(data)
        print('-' * 40 + '\n')

    # lzw_encode
    enc_start = time.time()
    dicSize, enc = lzw_encode(data)
    encoding = bitfy(dicSize, enc)
    enc_end = time.time()
    enc_size = len(encoding)

    # print statistics for encoding
    if args.e:
        print("## Encoding Statistics:")
        print('-' * 40)
        print("# Encoding Time: %.8s secs" % (enc_end - enc_start))
        print("# Encoded File Size: %s bits" % enc_size)
        print("# Encoded File Size: %s bytes" % math.ceil(enc_size/8.0))
        print("# Original File Size: %s bytes" % (len(data)))
        print('-' * 40 + '\n')

    # write encoded output file
    try:
        f = open(args.encoding, 'wb')
        encoding.tofile(f)
    except:
        print("Error opening encoding:", sys.exc_info()[0])
    else:
        f.close()

    # lzw_decode
    dec_start = time.time()
    dicSize, enc = unbitfy(encoding)
    outfile = lzw_decode(dicSize, enc)
    dec_end = time.time()

    # print statistics for decoding
    if args.e:
        print("## Decoding Statistics:")
        print('-' * 40)
        print("# Decoding Time: %.8s secs" % (dec_end - dec_start))
        print('-' * 40 + '\n')
        print("## Result of Diff:")
        print("## 'diff %s %s'" % (args.infile, args.outfile))
        print('-' * 40)
        if call(["diff", args.infile, args.outfile]) != 0:
            print("!! Input and Output differs.")
        print('-' * 40 + '\n')

    # print output for decoding
    if args.e:
        print("## Output of Decoding:")
        print('-' * 40)
        print40(outfile)
        print('-' * 40)

    # write decoded output file
    try:
        f = open(args.outfile, 'w')
        f.write(outfile)
    except:
        print("Error opening outfile:", sys.exc_info()[0])
    else:
        f.close()
