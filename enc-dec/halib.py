from Crypto.Cipher import AES
from os import urandom

BLOCK_SIZE = 16

def cipher_gen(filename):
    file = open(filename, "r")
    key = file.read().replace('\n','')
    hexkey = bytes.fromhex(key)
    Fk = AES.new(hexkey, AES.MODE_ECB)
    file.close()

    return Fk

def read_msg(filename):
    file = open(filename, "rb")
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
    tmp = bytearray(blockSize)
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
        tmp = blocks[len(blocks)-1]
        blocks.append(bytearray(blockSize))

    for i in range(r,blockSize):
        blocks[len(blocks)-1][i] = (pad.to_bytes(1, byteorder='big'))[0]
       
    #blocks.append(bytes(tmp))

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
    print(len(msg))
    mBlocks = split_pad_msg(msg, BLOCK_SIZE)
    print(len(mBlocks))
    cBlocks = []
    IV = urandom(BLOCK_SIZE)
    cBlocks.append(IV)
    
    for i in range(len(mBlocks)):
        ci = enc_block_CBC(cBlocks[i], mBlocks[i], Fk)
        cBlocks.append(ci)

    return glue_msg(cBlocks)

def glue_msg(blocks):
    cipher = bytearray()
    for i in range(len(blocks)):
        cipher += blocks[i]

    return bytes(cipher)

def dec_CBC(cipher, Fk):
   cBlocks = split_msg(cipher, BLOCK_SIZE) 
   mBlocks = []

   for i in range(1, len(cBlocks)):
       mi = dec_block_CBC(cBlocks[i-1], cBlocks[i], Fk)
       mBlocks.append(mi)

   msg = glue_msg(mBlocks)

   return strip_pad(msg)

def strip_pad(padded):
    pad = padded[len(padded)-1]
    msg = padded[:len(padded)-pad]
    return msg
    #msg = bytearray(padded)
    
    #for i in range(pad):
        #msg[len[msg]-1-i] = 
