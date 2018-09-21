#halib - Hayden Aaron Library
#COSC 483
from Crypto.Cipher import AES
from os import urandom
from multiprocessing import Pool
import sys

#Block size algorithms operate on
BLOCK_SIZE = 16

#Create and return pseudorandom function from keyfile
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

#Read in byte data from file
def read_msg(filename):
    try:
        file = open(filename, "rb")
    except IOError:
        print("Error: msgfile '" + filename + "' not found.", file=sys.stderr)
        exit()

    msg = file.read()
    file.close()
    return msg

#Write byte data to file
def write_msg(msg, filename):
    file = open(filename, "wb")
    file.write(msg)
    file.close()
    return

#Split and return message into blocks without padding
def split_msg(msg, blockSize):
    blocks = []
    q,r = divmod(len(msg), blockSize)

    #Entire Blocks
    for i in range(q):
        tmp = bytearray(blockSize)

        for j in range(blockSize):
            tmp[j] = msg[i*blockSize + j]

        blocks.append(bytearray(tmp))
   
    #Partial Block
    tmp = bytearray(r)
    for i in range(r):
        tmp[i] = msg[q * blockSize + i]

    if r:
        blocks.append(bytearray(tmp))

    return blocks

#Return msg split into blocks with padding
def split_pad_msg(msg, blockSize):
    q,r = divmod(len(msg), blockSize)
    blocks = split_msg(msg, blockSize)

    pad = blockSize - r

    if not r:
        blocks.append(bytearray(blockSize))
    else:
        padBlock = bytearray(pad)
        blocks[len(blocks)-1] = glue_msg([blocks[len(blocks)-1], padBlock])

    for i in range(r,blockSize):
        blocks[len(blocks)-1][i] = (pad.to_bytes(1, byteorder='big'))[0]

    return blocks

#Return XOR of two given byte arrays
def XOR(s1, s2):
    s = bytearray(len(s1))

    for i in range(len(s1)):
        s[i] = s1[i] ^ s2[i]

    return s

#------------CBC Functions--------------------
#Single block encoding for CBC, CBC-MAC
def enc_block_CBC(s1,s2,Fk):
    I = XOR(s1,s2)
    return Fk.encrypt(bytes(I))

#Single block decoding for CBC
def dec_block_CBC(s1, s2, Fk):
    I = Fk.decrypt(bytes(s2))
    return XOR(s1, I)

#Encode given message with CBC and pseudorandom Fk
def enc_CBC(msg, Fk):
    mBlocks = split_pad_msg(msg, BLOCK_SIZE)
    cBlocks = []

    IV = urandom(BLOCK_SIZE)
    cBlocks.append(IV)
    
    for i in range(len(mBlocks)):
        ci = enc_block_CBC(cBlocks[i], mBlocks[i], Fk)
        cBlocks.append(ci)

    return glue_msg(cBlocks)

#Decode given message with CBC and pseudorandom Fk
def dec_CBC(cipher, Fk):
   cBlocks = split_msg(cipher, BLOCK_SIZE) 
   mBlocks = []

   for i in range(1, len(cBlocks)):
       mi = dec_block_CBC(cBlocks[i-1], cBlocks[i], Fk)
       mBlocks.append(mi)

   msg = glue_msg(mBlocks)

   return strip_pad(msg)

#------------CTR Functions--------------------
#Single block encoding/decoding for CTR
def block_CTR(s1, s2, Fk):
    I = Fk.encrypt(bytes(s1))
    if len(s2) < len(s1):
        I = I[:len(s2)]

    return XOR(I,s2)

#Encode given message with CTR and pseudorandom Fk
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
        cBlocks.append(ci)

    return glue_msg(cBlocks)

#Decode given message with CTR and pseudorandom Fk
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
        mBlocks.append(mi)

   return glue_msg(mBlocks)

#Parallel Implementation of enc_CTR
def prl_enc_CTR(msg, Fk, pNum):
    p = Pool(processes=pNum)
    cipher = p.map(enc_CTR, (msg, Fk))
    p.close()

    return cipher

#Parallel Implementation of dec_CTR
def prl_dec_CTR(cipher, Fk, pNum):
    p = Pool(processes=pNum)
    msg = p.map(dec_CTR, (cipher, Fk))
    p.close()

    return msg
#---------------------------------------------

#Concatenate given list of byte strings
def glue_msg(blocks):
    cipher = bytearray()
    for i in range(len(blocks)):
        cipher += blocks[i]

    return cipher

#Strip padding from padded msg
def strip_pad(padded):
    pad = padded[len(padded)-1]
    msg = padded[:len(padded)-pad]
    return msg

#Parse command line arguments for CBC, CTR
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

#---------CBC-MAC Functions-------------------
#Parse command line arguments for CBC-MAC
def parse_argv_MAC(argv):
    try:
        keyFile = argv[argv.index("-k")+1]
        kFlag = True
    except:
        kFlag = False

    try:
        msgFile = argv[argv.index("-m")+1]
        iFlag = True
    except:
        iFlag = False

    try:
        outFile = argv[argv.index("-t")+1]
        oFlag = True
    except:
        oFlag = False

    if(not kFlag or not oFlag or not iFlag):
        print("usage:" ,sys.argv[0], "-k <keyFile> -m <msgFile> -t <tagFile>", file=sys.stderr)
        exit()

    return keyFile, msgFile, outFile

#Build CBC-MAC tag for given msg
def build_tag(msg, Fk):
    mBlocks = split_pad_msg(msg, BLOCK_SIZE)
    N = len(msg)
    m_prev = Fk.encrypt(N.to_bytes(16, byteorder='big'))

    for i in range(len(mBlocks)):
        tag = enc_block_CBC(m_prev, mBlocks[i], Fk)
        m_prev = tag

    return tag

#Verify integrity of given tagged msg
def verify_tag(msg, tag, Fk):
    if tag == build_tag(msg, Fk):
        return True
    else:
        return False
#---------------------------------------------
