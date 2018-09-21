import sys
sys.path.append("../lib")

from halib import *

keyFile, msgFile, tagFile = parse_argv_MAC(sys.argv)

msg = read_msg(msgFile)
Fk = cipher_gen(keyFile)

tag = build_tag(msg, Fk)

write_msg(tag, tagFile)
