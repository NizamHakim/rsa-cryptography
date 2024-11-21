import random

def getPrimeSeries(totient):
    primes = [True for i in range(totient)]
    p = 2
    while p * p <= totient:
        if primes[p]:
            for i in range(p * p, totient, p):
                primes[i] = False
        p += 1
        
    results = []
    for i in range(2, totient):
        if primes[i]: 
            results.append(i)
            
    return results

def extendedEuclidean(a, b):
    if b == 0:
        return a, 1, 0
    else:
        g, x1, y1 = extendedEuclidean(b, a % b)
        x = y1
        y = x1 - (a // b) * y1
        return g, x, y

def modularInverse(e, totient):
    g, x, y = extendedEuclidean(e, totient)
    if g != 1:
        raise ValueError("No modular inverse exists")
    else:
        return x % totient

def getKeyPair(p, q):
    n = p * q
    totient = (p - 1) * (q - 1)
    primes = getPrimeSeries(totient)
    e = random.choice(primes)
    d = modularInverse(e, totient)
    return {'n': n, 'e': e}, {'n': n, 'd': d}

def encrypt(message, key: dict):
    n, e = key['n'], key['e']
    encrypted = ''
    for char in message:
        encrypted += chr(pow(ord(char), e, n))
    return encrypted

def decrypt(encrypted, key: dict):
    n, d = key['n'], key['d']
    decrypted = ''
    for char in encrypted:
        decrypted += chr(pow(ord(char), d, n))
    return decrypted