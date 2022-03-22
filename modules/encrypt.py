'''
RSA (Rivest-Shamir-Adleman) Algorithm

Encryption
'''

def baseEncrypt(m: int, e: int, n: int) -> int:
    '''
    Base RSA Encryption algorithm
    '''
    return (m**e) % n
    

def encryptFile(fileName: str, e: int, n: int):
    '''
    File encryption
    '''
    file = open(fileName, "rb")
    plainBytes = file.read()
    file.close()

    intValue = int.from_bytes(plainBytes, "big", signed=False)
    cipherInt = baseEncrypt(intValue, e, n)
    cipherBytes = intValue.to_bytes((cipherInt.bit_length() + 7) // 8, "big", signed=False)

    ext = fileName.split("/")[-1]
    file = open(f"files/encrypted{ext}", "wb")
    file.write(cipherBytes)
    file.close()

encryptFile("main.py",7,209)