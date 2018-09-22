#Students: Hayden Coffey, Aaron Johnson
#COSC 483

import sys
sys.path.append("lib")
from halib import *

#Parse given arguments
keyFile, msgFile, outFile = parse_argv(sys.argv)

#Read in cipher, and decrypt in parallel
cipher = read_msg(msgFile)
msg = prl_dec_CTR(cipher, keyFile, CORE_NUM)

write_msg(msg, outFile)
