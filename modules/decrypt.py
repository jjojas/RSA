'''
RSA (Rivest-Shamir-Adleman) Algorithm

Decryption
'''

from typing import List
import math


def baseDecrypt(c: int, d: int, n: int) -> int:
    '''
    Base RSA Encryption algorithm
    '''
    return (c**d) % n

def binaryPadding(bits: str, n: int) -> str :
    while len(bits) % n != 0:
        bits = '0'+bits
    return bits
    
def convertBytetoIntArray(bytesInput: bytes, digitDiv: int) -> List[int]:
    result = []
    binInput = bin(int.from_bytes(bytesInput, "big"))[2:]
    # binInput = binInput.zfill(len(bytesInput)*digitDiv)
    binInput = binaryPadding(binInput, digitDiv)

    for index in range(0, len(binInput), digitDiv):
        # print("iter",binInput[index : index + digitDiv])
        result.append(int(binInput[index : index + digitDiv], 2))

    return result

def convertIntArraytoByte(inputList: List[int], digit: int) -> bytes:
    # binary = ''.join([bin(val)[2:].zfill(digit) for val in inputList]) 
    # print(inputList)
    # print("len", len(inputList))
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
    return math.floor(math.log2(n))

def maxBitLength(n: int) -> int:
    return (n-1).bit_length()

def decryptFile(fileName: str, d: int, n: int):
    '''
    File decryption
    '''
    file = open(fileName, "rb")
    cipherBytes = file.read()
    file.close()

    
    # intValue = int.from_bytes(plainBytes, "big", signed=False)
    # print("value:",intValue)
    # cipherInt = baseEncrypt(intValue, e, n)
    # print("cipher:",cipherInt)
    # cipherBytes = intValue.to_bytes((cipherInt.bit_length() + 7) // 8, "big", signed=False)
    
    digitDiv = digitDivider(n)
    intValue = convertBytetoIntArray(cipherBytes, maxBitLength(n))
    plainInt = [baseDecrypt(val, d, n) for val in intValue]
    plainBytes = convertIntArraytoByte(plainInt, digitDiv)

    ext = fileName.split("/")[-1]
    file = open(f"files/decrypted_{ext}", "wb")
    file.write(plainBytes)
    file.close()

# Public Key (E, N): (7,209)
# Private Key (D, N): (283,209)
# encryptFile("main.py",7,209)
# decryptFile("files/encrypted_main.py",283,209)
# decryptFile("files/encrypted_legenda.png",283,209)
# decryptFile("files/encrypted_legenda2.png",1019,3337)
# decryptFile("files/encrypted_util2.mkv",1019,3337)
# convertBytetoIntArray(b'\xfc\x00', 5)
# convertIntArraytoByte([2,2])