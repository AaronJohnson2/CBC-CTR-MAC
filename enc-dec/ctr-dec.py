#Students: Hayden Coffey, Aaron Johnson
#COSC 483
import sys
sys.path.append("lib")
from halib import *

#Parse given arguments
keyFile, msgFile, outFile = parse_argv(sys.argv)

#Read in cipher, create Fk, and decrypt
cipher = read_msg(msgFile)
msg = prl_dec_CTR(cipher, keyFile, 4)

write_msg(msg, outFile)
