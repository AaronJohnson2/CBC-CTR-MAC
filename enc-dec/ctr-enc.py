#Students: Hayden Coffey, Aaron Johnson
#COSC 483

import sys
sys.path.append("lib")
from halib import *

#Parse given arguments
keyFile, msgFile, outFile = parse_argv(sys.argv)

#Read in msg, and encrypt in parallel
msg = read_msg(msgFile)
cipher = prl_enc_CTR(msg, keyFile, CORE_NUM)

write_msg(cipher, outFile)
