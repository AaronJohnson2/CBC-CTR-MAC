from Crypto.Cipher import AES
from os import urandom
import sys

BLOCK_SIZE = 16

def cipher_gen(filename):
    try:
        file = open(filename, "r")
    except IOError:
        print("Error: keyfile '" + filename + "' not found.", file=sys.stderr)
        exit()

    key = file.read().replace('\n','')
    hexkey = bytes.fromhex(key)
    Fk = AES.new(hexkey, AES.MODE_ECB)
    file.close()

    return Fk

def read_msg(filename):
    try:
        file = open(filename, "rb")
    except IOError:
        print("Error: msgfile '" + filename + "' not found.", file=sys.stderr)
        exit()

    msg = file.read()
    file.close()
    return msg

def write_msg(msg, filename):
    file = open(filename, "wb")
    file.write(msg)
    file.close()
    return

def split_msg(msg, blockSize):
    #msg = str(msg)
    blocks = []

    q,r = divmod(len(msg), blockSize)

    #Entire Blocks
    for i in range(q):
        tmp = bytearray(blockSize)

        for j in range(blockSize):
            tmp[j] = msg[i*blockSize + j]

        blocks.append(bytes(tmp))
   
    #Partial Block
    tmp = bytearray(r)
    for i in range(r):
        tmp[i] = msg[q * blockSize + i]

    if r:
        blocks.append(bytes(tmp))

    return blocks

def split_pad_msg(msg, blockSize):
    q,r = divmod(len(msg), blockSize)
    blocks = split_msg(msg, blockSize)

    #Padding
    pad = blockSize - r

    if not r:
        blocks.append(bytearray(blockSize))
    else:
        padBlock = bytes(pad)
        blocks[len(blocks)-1] = glue_msg([blocks[len(blocks)-1], padBlock])

    for i in range(r,blockSize):
        blocks[len(blocks)-1][i] = (pad.to_bytes(1, byteorder='big'))[0]

    return blocks

def XOR(s1, s2):
    s = bytearray(len(s1))

    for i in range(len(s1)):
        s[i] = s1[i] ^ s2[i]

    return bytes(s)

def enc_block_CBC(s1,s2,Fk):
    I = XOR(s1,s2)
    return Fk.encrypt(I)

def dec_block_CBC(s1, s2, Fk):
    I = Fk.decrypt(s2)
    return XOR(s1, I)

def enc_CBC(msg, Fk):
    mBlocks = split_pad_msg(msg, BLOCK_SIZE)
    cBlocks = []

    IV = urandom(BLOCK_SIZE)
    cBlocks.append(IV)
    
    for i in range(len(mBlocks)):
        ci = enc_block_CBC(cBlocks[i], mBlocks[i], Fk)
        cBlocks.append(ci)

    return glue_msg(cBlocks)

def dec_CBC(cipher, Fk):
   cBlocks = split_msg(cipher, BLOCK_SIZE) 
   mBlocks = []

   for i in range(1, len(cBlocks)):
       mi = dec_block_CBC(cBlocks[i-1], cBlocks[i], Fk)
       mBlocks.append(mi)

   msg = glue_msg(mBlocks)

   return strip_pad(msg)

#------------CTR Functions--------------------
def block_CTR(s1, s2, Fk):
    I = Fk.encrypt(s1)
    if len(s2) < len(s1):
        I = I[:len(s2)]

    return XOR(I,s2)

def enc_CTR(msg, Fk):
    mBlocks = split_msg(msg, BLOCK_SIZE)
    cBlocks = []
    ctrBlocks = []

    IV = urandom(BLOCK_SIZE)
    cBlocks.append(IV)
    
    CTR = int.from_bytes(IV, byteorder='big')
    for i in range(len(mBlocks)):
        ctrBlocks.append(bytes((CTR + i + 1).to_bytes(16, byteorder='big')))

    for i in range(len(mBlocks)):
        ci = block_CTR(ctrBlocks[i], mBlocks[i], Fk)
        #print(mBlocks[i])
        #print(ci)
        cBlocks.append(ci)

    return glue_msg(cBlocks)

def dec_CTR(cipher, Fk):
   cBlocks = split_msg(cipher, BLOCK_SIZE)
   mBlocks = []
   ctrBlocks = []

   IV = cBlocks[0]
   CTR = int.from_bytes(IV, byteorder='big')
   for i in range(len(cBlocks)-1):
        ctrBlocks.append(bytes((CTR + i + 1).to_bytes(16, byteorder='big')))

   for i in range(len(cBlocks)-1):
        mi = block_CTR(ctrBlocks[i], cBlocks[i+1], Fk)
        #print(mi)
        mBlocks.append(mi)

   return glue_msg(mBlocks)

def glue_msg(blocks):
    cipher = bytearray()
    for i in range(len(blocks)):
        cipher += blocks[i]

    return bytes(cipher)

def strip_pad(padded):
    pad = padded[len(padded)-1]
    msg = padded[:len(padded)-pad]
    return msg
    

def parse_argv(argv):
    try:
        keyFile = argv[argv.index("-k")+1]
        kFlag = True
    except:
        kFlag = False

    try:
        msgFile = argv[argv.index("-i")+1]
        iFlag = True
    except:
        iFlag = False

    try:
        outFile = argv[argv.index("-o")+1]
        oFlag = True
    except:
        oFlag = False

    if(not kFlag or not oFlag or not iFlag):
        print("usage:" ,sys.argv[0], "-k <keyFile> -i <inputFile> -o <outputFile>", file=sys.stderr)
        exit()

    return keyFile, msgFile, outFile