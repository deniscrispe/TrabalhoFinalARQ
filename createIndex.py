import struct
import hashlib
import os

def h(key):
    global hashSize
    return int(hashlib.sha1(key).hexdigest(), 16) % hashSize

hashSize = 17035841
indexFormat = "11sLL"
indexStruct = struct.Struct(indexFormat)
keyColumnIndex = 5
fileName = "bolsa.csv"
indexName = "bolsa-hash.dat"

fi = open(indexName, "wb")
emptyIndexRecord = indexStruct.pack("", 0, 0)
for i in range(0, hashSize):
    fi.write(emptyIndexRecord)
fi.close()

f = open(fileName, "r")
fi = open(indexName, "r+b")#hash

fi.seek(0, os.SEEK_END)
fileIndexSize = fi.tell()
print ("IndexFileSize", fileIndexSize)

f.readline()

recordNumber = 0
while True:
    recordNumber = f.tell()
    line = f.readline()
    if line == "": # EOF
        break
    record = line.split(";")
    p = h(record[keyColumnIndex].replace('"',''))
    fi.seek(p * indexStruct.size, os.SEEK_SET)
    indexRecord = indexStruct.unpack(fi.read(indexStruct.size))
    fi.seek(p * indexStruct.size, os.SEEK_SET)
    if indexRecord[0][0] == "\0":
        fi.write(indexStruct.pack(record[keyColumnIndex].replace('"',''), recordNumber, 0))
    else:
        nextPointer = indexRecord[2]
        fi.write(indexStruct.pack(indexRecord[0],indexRecord[1],fileIndexSize))
        fi.seek(0,os.SEEK_END)
        fi.write(indexStruct.pack(record[keyColumnIndex].replace('"',''),recordNumber,nextPointer))
        fileIndexSize = fi.tell()
    recordNumber += 1
f.close()
fi.close()




