from os import urandom
import sys

#Import all written functions
from halib import *

#print("Name:",sys.argv[0])
#print("Number:",len(sys.argv))
#print("Arg:",str(sys.argv))


keyFile = "../temp/keyFile1"
msgFile = "testOut"
outFile = "testOut-dec"

cipher = read_msg(msgFile)
Fk = cipher_gen(keyFile)

msg = dec_CBC(cipher, Fk)

write_msg(msg, outFile)
#cBlocks = split_msg(cipher, BLOCK_SIZE)
#IV = cBlocks[0]

#m1 = dec_block_CBC(IV, cBlocks[1], Fk)

#print("IV: {}".format(IV))
#print("m1: {}".format(m1))
#print("c1: {}".format(cBlocks[1]))

#write_msg(m1, outFile)
