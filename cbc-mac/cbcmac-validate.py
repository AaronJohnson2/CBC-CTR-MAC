import sys
sys.path.append("../lib")

from halib import *

keyFile, msgFile, tagFile = parse_argv_MAC(sys.argv)

msg = read_msg(msgFile)
tag = read_msg(tagFile)
Fk = cipher_gen(keyFile)

if verify_tag(msg, tag, Fk):
    print("True")
else:
    print("False")
