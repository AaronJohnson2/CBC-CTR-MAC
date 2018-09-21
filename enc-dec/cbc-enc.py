import sys
sys.path.append("../lib")
#Import all written functions
from halib import *

keyFile, msgFile, outFile = parse_argv(sys.argv)

msg = read_msg(msgFile)
Fk = cipher_gen(keyFile)

cipher = enc_CBC(msg, Fk)

write_msg(cipher, outFile)
