#Students: Hayden Coffey, Aaron Johnson
#COSC 483

import sys
sys.path.append("lib")
from halib import *

#Parse given arguments
keyFile, msgFile, outFile = parse_argv(sys.argv)

#Read in msg, create Fk, and encrypt
msg = read_msg(msgFile)
Fk = cipher_gen(keyFile)

cipher = prl_enc_CTR(msg, Fk)

write_msg(cipher, outFile)
