import sys

from halib import *

keyFile, msgFile, outFile = parse_argv(sys.argv)

msg = read_msg(msgFile)
Fk = cipher_gen(keyFile)
