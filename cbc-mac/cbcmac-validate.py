#Students: Hayden Coffey, Aaron Johnson
#COSC 483

import sys
sys.path.append("lib")
from halib import *

#Parse given arguments
keyFile, msgFile, tagFile = parse_argv_MAC(sys.argv)

#Read in msg and verify integrity
msg = read_msg(msgFile)
tag = read_msg(tagFile)
Fk = cipher_gen(keyFile)

if verify_tag(msg, tag, Fk):
    print("True")
else:
    print("False")
