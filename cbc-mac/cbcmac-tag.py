#Students: Hayden Coffey, Aaron Johnson
#COSC 483

import sys
sys.path.append("lib")
from halib import *

#Parse given arguments
keyFile, msgFile, tagFile = parse_argv_MAC(sys.argv)

#Read in msg, create Fk, and generate tag
msg = read_msg(msgFile)
Fk = cipher_gen(keyFile)

tag = build_tag(msg, Fk)

write_msg(tag, tagFile)
