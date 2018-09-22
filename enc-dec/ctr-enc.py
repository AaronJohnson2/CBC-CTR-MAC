#Students: Hayden Coffey, Aaron Johnson
#COSC 483
import sys
sys.path.append("lib")
from halib import *

#Parse given arguments
keyFile, msgFile, outFile = parse_argv(sys.argv)

#Read in msg, create Fk, and encrypt
msg = read_msg(msgFile)
cipher = prl_enc_CTR(msg, keyFile, 4)

write_msg(cipher, outFile)
