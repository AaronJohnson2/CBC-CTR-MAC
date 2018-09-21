import sys
sys.path.append("lib")
from halib import *

keyFile, msgFile, outFile = parse_argv(sys.argv)

cipher = read_msg(msgFile)
Fk = cipher_gen(keyFile)

msg = dec_CTR(cipher, Fk)

write_msg(msg, outFile)
