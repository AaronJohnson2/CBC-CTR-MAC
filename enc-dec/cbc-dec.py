import sys

#Import all written functions
from halib import *

keyFile, msgFile, outFile = parse_argv(sys.argv)

cipher = read_msg(msgFile)
Fk = cipher_gen(keyFile)

msg = dec_CBC(cipher, Fk)

write_msg(msg, outFile)
