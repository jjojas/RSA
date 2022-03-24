'''
RSA (Rivest-Shamir-Adleman) Algorithm

Decryption
'''

from typing import List
import math

def baseDecrypt(c: int, d: int, n: int) -> int:
    '''
    Fungsi basis dekripsi RSA menggunakan kunci privat (d,n)
    '''
    return pow(c, d, n)

def binaryPadding(bits: str, n: int) -> str :
    '''
    Menambahkah padding '0' sebanyak n bit.
    '''
    while len(bits) % n != 0:
        bits = '0'+bits
    return bits
    
def convertBytetoIntArray(bytesInput: bytes, digitDiv: int) -> List[int]:
    '''
    Konversi Byte ke Array of Integer
    '''
    result = []
    binInput = bin(int.from_bytes(bytesInput, "big"))[2:]
    binInput = binaryPadding(binInput, digitDiv)

    for index in range(0, len(binInput), digitDiv):
        result.append(int(binInput[index : index + digitDiv], 2))

    return result

def convertIntArraytoByte(inputList: List[int], digit: int) -> bytes:
    '''
    Konversi Array of Integer menjadi Byte
    '''
    binary = ''
    for i, val in enumerate(inputList):
        if i != len(inputList)-2 :
            binary+=bin(val)[2:].zfill(digit)
        else:
            binary+=bin(val)[2:].zfill(inputList[-1])
            break

    intResult = int(binary, 2)
    result = intResult.to_bytes((len(binary) + 7) // 8, "big", signed=False)

    return result

def digitDivider(n: int) -> int:
    '''
    Menentukan panjang digit/bit awal
    '''
    return math.floor(math.log2(n))

def maxBitLength(n: int) -> int:
    '''
    Menentukan panjang bit maksimal membagi enkripsi binary [0...n-1]
    '''
    return (n-1).bit_length()

def decryptFile(fileName: str, d: int, n: int):
    '''
    Operasi dekripsi file berdasarkan kunci publik (d,n)
    File disimpan dalam direktori /files/
    '''
    file = open(fileName, "rb")
    cipherBytes = file.read()
    file.close()
    
    digitDiv = digitDivider(n)
    intValue = convertBytetoIntArray(cipherBytes, maxBitLength(n))
    plainInt = [baseDecrypt(val, d, n) for val in intValue]
    plainBytes = convertIntArraytoByte(plainInt, digitDiv)

    ext = fileName.split("/")[-1]
    file = open(f"files/decrypted_{ext}", "wb")
    file.write(plainBytes)
    file.close()