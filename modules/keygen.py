
def checkPrime(n : int) -> bool:
    if (n == 1):
        return False
    i = 2
    while (i*i <= n):
        if (n%i ==0):
            return False
        i += 1
    return True

def genPrivateKey(p : int, q : int ,e : int) -> str:
    '''
    Membangkitkan kunci privat
    '''
    d = 0
    if (checkPrime(p) and checkPrime(q)):
        n = p*q
        toit = (p-1)*(q-1)
        d = 0.5
        k = 1
        while (d%1 != 0):
            d = (1+k*toit)/e
            k += 1
        return (e,int(d))
    else:
        raise Exception("P or Q is not a prime number!")

if __name__ == "__main__":
    print(genPrivateKey(47,71,79))
    # print(checkPrime(int(input())))