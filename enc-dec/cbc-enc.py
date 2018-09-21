import sys

#Import all written functions
from halib import *

#print("Name:",sys.argv[0])
#print("Number:",len(sys.argv))
#print("Arg:",str(sys.argv))

kFlag = False
iFlag = False
oFlag = False

if "-k" in sys.argv:
    try:
        keyFile = sys.argv[sys.argv.index("-k")+1]
        print(keyFile)
        kFlag = True
    except:
        pass

if "-i" in sys.argv:
    try:
        msgFile = sys.argv[sys.argv.index("-i")+1]
        print(msgFile)
        iFlag = True
    except:
        pass

if "-o" in sys.argv:
    try:
        outFile = sys.argv[sys.argv.index("-o")+1]
        print(outFile)
        oFlag = True
    except:
        pass

if(not kFlag or not oFlag or not iFlag):
    print("usage:" ,sys.argv[0], "-k <keyFile> -i <inputFile> -o <outputFile>", file=sys.stderr)
    exit()



#keyFile = "../temp/keyFile1"
msgFile = "../temp/testFile1"
outFile = "testOut"


msg = read_msg(msgFile)
Fk = cipher_gen(keyFile)

cipher = enc_CBC(msg, Fk)

write_msg(cipher, outFile)

#IV = urandom(BLOCK_SIZE)

#mBlocks = split_pad_msg(msg, BLOCK_SIZE)

#c1 = enc_block_CBC(IV,mBlocks[0], Fk)
#print("IV: {}".format(IV))
#print("m1: {}".format(mBlocks[0]))
#print("c1: {}".format(c1))

#write_msg(IV + c1, outFile)

#write_msg(mBlocks[0], "testOut-m")
