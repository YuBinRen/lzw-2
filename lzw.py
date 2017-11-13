#!/usr/bin/python3

from utils_lzw import Trie, Array
import sys

log = False

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

# (size, index array) -> bitstream
def bitfy(dicSize, enc):
    pass

# bitstream -> (size, index array)
def unbitfy(encoding):
    pass

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("infile", type=str, help="input file")
    parser.add_argument("encoding", type=str, help="encoded output file")
    parser.add_argument("outfile", type=str, help="decoded output file")
    parser.add_argument("-e", action="store_true", help="print on screen")
    args = parser.parse_args()

    # set logging options
    log = args.e

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
    encoding = bitfy(lzw_encode(data))

    # write encoded output file
    try:
        pass
        #f = open(args.encoding, 'wb')
        #f.write(encoding)
    except:
        print("Error opening encoding:", sys.exc_info()[0])
    else:
        f.close()

    # lzw_decode
    outfile = lzw_decode(unbitfy(encoding))

    # write decoded output file
    try:
        pass
        #f = open(args.outfile, 'w')
        #f.write(outfile)
    except:
        print("Error opening outfile:", sys.exc_info()[0])
    else:
        f.close()
