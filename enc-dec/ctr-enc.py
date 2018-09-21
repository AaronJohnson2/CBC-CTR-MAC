import sys
sys.path.append("../lib")
from halib import *

keyFile, msgFile, outFile = parse_argv(sys.argv)

msg = read_msg(msgFile)
Fk = cipher_gen(keyFile)

cipher = enc_CTR(msg, Fk)

write_msg(cipher, outFile)
