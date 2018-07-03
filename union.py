import struct
import hashlib
import os

hashSize = 17035841

def h(key):
    global hashSize
    return int(hashlib.sha1(key).hexdigest(), 16) % hashSize

indexFormat = "11sLL"
indexStruct = struct.Struct(indexFormat)
keyColumnIndex = 5

a = open("bolsa.csv", "r")
b = open("bolsa2.csv", "r")
hashA = open("bolsa-hash.dat", "r+b")
aUnionB = open("unionFile.dat", "a+")

aUnionB.write(a.readline())

while True:
    line = a.readline()
    if line == "": # EOF
        break
    aUnionB.write(line)

while True:
    line = b.readline()
    if line == "": # EOF
        break
    record = line.split(";")
    nisProcurado = record[keyColumnIndex].replace('"','')
    p = h(nisProcurado)
    offset = p* indexStruct.size
    n = 1
    while True:
        hashA.seek(offset, os.SEEK_SET)
        indexRecord = indexStruct.unpack(hashA.read(indexStruct.size))
        if indexRecord[0] == str(nisProcurado):
            break
        offset = indexRecord[2]
        if offset == 0:
            aUnionB.write(line)
            break
        n += 1
a.close()
b.close()
hashA.close()
aUnionB.close()