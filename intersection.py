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

b = open("bolsa2.csv", "r")
hashA = open("bolsa-hash.dat", "r+b")
aIntersectionB = open("intersectionFile.dat", "a+")

aIntersectionB.write(b.readline())

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
            aIntersectionB.write(line)
            break
        offset = indexRecord[2]
        if offset == 0:
            break
        n += 1
b.close()
hashA.close()
aIntersectionB.close()