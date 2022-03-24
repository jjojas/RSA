'''
RSA (Rivest-Shamir-Adleman) Algorithm

Encryption
'''

from typing import List
import math


def baseEncrypt(m: int, e: int, n: int) -> int:
    '''
    Base RSA Encryption algorithm
    '''
    return pow(m, e, n)
    
def convertBytetoIntArray(bytesInput: bytes, digitDiv: int) -> List[int]:
    result = []
    binInput = bin(int.from_bytes(bytesInput, "big"))[2:]

    for index in range(0, len(binInput), digitDiv):
        result.append(int(binInput[index : index + digitDiv], 2))
    result.append(len(binInput) % digitDiv)

    return result
    
def convertIntArraytoByte(inputList: List[int], digit: int) -> bytes:
    binary = ''.join([bin(val)[2:].zfill(digit) for val in inputList]) 
    
    intResult = int(binary, 2)
    result = intResult.to_bytes((len(binary) + 7) // 8, "big")

    return result

def digitDivider(n: int) -> int:
    return math.floor(math.log2(n))

def maxBitLength(n: int) -> int:
    return (n-1).bit_length()

def encryptFile(fileName: str, e: int, n: int):
    '''
    File encryption
    '''
    file = open(fileName, "rb")
    plainBytes = file.read()
    file.close()
    
    digitDiv = digitDivider(n)
    intValue = convertBytetoIntArray(plainBytes, digitDiv)
    cipherInt = [baseEncrypt(val, e, n) for val in intValue]
    cipherBytes = convertIntArraytoByte(cipherInt, maxBitLength(n))

    ext = fileName.split("/")[-1]
    file = open(f"files/encrypted_{ext}", "wb")
    file.write(cipherBytes)
    file.close()

# Public Key (E, N): (7,209)
# Private Key (D, N): (283,209)
# encryptFile("main.py",7,209)
# encryptFile("files/legenda.png",7,209)
# encryptFile("files/legenda2.png",5,39203)
# encryptFile("files/util2.mkv",79,3337)
# convertBytetoIntArray(b'\xfc\x00', 5)
# convertIntArraytoByte([2,2])