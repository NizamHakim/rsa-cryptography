def strToBin(input):
    output = ""
    for i in input:
        output += bin(ord(i))[2:].zfill(8)
    return output

def binToStr(input):
    output = ""
    for i in range(0, len(input), 8):
        output += chr(int(input[i:i+8], 2))
    return output

def keyScheduling(mainKey64):
    effectiveKey56 = ""
    for i in range(64):
        if i % 8 != 7: # dropping 8th's bit
            effectiveKey56 += mainKey64[i]
            
    keys48 = []
    for i in range(16):
        left = effectiveKey56[0:28]
        right = effectiveKey56[28:56]
        if i in [0, 1, 8, 15]:
            left = leftCircularShift(left, 1)
            right = leftCircularShift(right, 1)
        else:
            left = leftCircularShift(left, 2)
            right = leftCircularShift(right, 2)
        effectiveKey56 = left + right
        
        key = ""
        for j in range(56):
            if j % 8 != 7: # compression permutation
                key += effectiveKey56[j]
        keys48.append(key)
        
    return keys48

def leftCircularShift(input, shift):
    return input[shift:] + input[:shift]

def initialPermutation(input):
    permutationTable = [
        58, 50, 42, 34, 26, 18, 10, 2, 
        60, 52, 44, 36, 28, 20, 12, 4, 
        62, 54, 46, 38, 30, 22, 14, 6, 
        64, 56, 48, 40, 32, 24, 16, 8, 
        57, 49, 41, 33, 25, 17,  9, 1, 
        59, 51, 43, 35, 27, 19, 11, 3, 
        61, 53, 45, 37, 29, 21, 13, 5, 
        63, 55, 47, 39, 31, 23, 15, 7
    ]
    output = ""
    for i in permutationTable:
        output += input[i-1]
    return output[0:32], output[32:64]

def inverseInitialPermutation(input):
    permutationTable = [
        40, 8, 48, 16, 56, 24, 64, 32, 
        39, 7, 47, 15, 55, 23, 63, 31, 
        38, 6, 46, 14, 54, 22, 62, 30, 
        37, 5, 45, 13, 53, 21, 61, 29, 
        36, 4, 44, 12, 52, 20, 60, 28, 
        35, 3, 43, 11, 51, 19, 59, 27, 
        34, 2, 42, 10, 50, 18, 58, 26, 
        33, 1, 41,  9, 49, 17, 57, 25
    ]
    output = ""
    for i in permutationTable:
        output += input[i-1]
    return output

def expansionPermutation(input):
    permutationTable = [
        32,  1,  2,  3,  4,  5, 
        4,   5,  6,  7,  8,  9, 
        8,   9, 10, 11, 12, 13, 
        12, 13, 14, 15, 16, 17, 
        16, 17, 18, 19, 20, 21, 
        20, 21, 22, 23, 24, 25, 
        24, 25, 26, 27, 28, 29, 
        28, 29, 30, 31, 32,  1
    ]
    output = ""
    for i in permutationTable:
        output += input[i-1]
    return output

def sBoxSubtitution(input):
    sBoxes = [
        # S1
        [
            [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7], 
            [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8], 
            [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0], 
            [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]
        ],
        # S2
        [
            [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
            [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
            [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
            [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]
        ],
        # S3
        [
            [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
            [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
            [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
            [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]
        ],
        # S4
        [
            [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
            [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
            [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
            [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]
        ],
        # S5
        [
            [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
            [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
            [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
            [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]
        ],
        # S6
        [
            [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
            [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
            [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
            [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]
        ],
        # S7
        [
            [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
            [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
            [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
            [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]
        ],
        # S8
        [
            [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
            [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
            [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
            [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]
        ]
    ]
    inputBoxes = [input[0:6], input[6:12], input[12:18], input[18:24], input[24:30], input[30:36], input[36:42], input[42:48]]
    output = ""
    for sBox, inputBox in zip(sBoxes, inputBoxes):
        row = int(inputBox[0] + inputBox[5], 2) # 1st and 6th bit -> cast to int
        col = int(inputBox[1:5], 2) # 2nd to 5th bit -> cast to int
        output += bin(sBox[row][col])[2:].zfill(4) # get the value from the sBox -> cast to binary
    return output
        
def pBoxTransposition(input):
    permutationTable = [
        16,  7, 20, 21, 29, 12, 28, 17, 
         1, 15, 23, 26,  5, 18, 31, 10, 
         2,  8, 24, 14, 32, 27,  3,  9, 
        19, 13, 30,  6, 22, 11,  4, 25
    ]
    output = ""
    for i in permutationTable:
        output += input[i-1]
    return output

def stringXor(input1, input2):
    output = ""
    for i, j in zip(input1, input2):
        if i == j:
            output += '0'
        else:
            output += '1'
    return output

def encrypt(binaryInput, mainKey64):
    left, right = initialPermutation(binaryInput) # 32 bits each
    keys = keyScheduling(mainKey64)
    for i in range(16):
        expandedRight = expansionPermutation(right) # 48 bits
        xorWithKey = stringXor(expandedRight, keys[i]) # 48 bits
        sBoxOutput = sBoxSubtitution(xorWithKey) # 32 bits
        pBoxOutput = pBoxTransposition(sBoxOutput) # 32 bits
        newRight = stringXor(left, pBoxOutput)
        left = right
        right = newRight
    output = inverseInitialPermutation(right + left)
    return binToStr(output)

def decrypt(binaryInput, mainKey64):
    left, right = initialPermutation(binaryInput) # 32 bits each
    keys = keyScheduling(mainKey64)
    for i in range(16):
        expandedRight = expansionPermutation(right) # 48 bits
        xorWithKey = stringXor(expandedRight, keys[15-i]) # 48 bits
        sBoxOutput = sBoxSubtitution(xorWithKey) # 32 bits
        pBoxOutput = pBoxTransposition(sBoxOutput) # 32 bits
        newRight = stringXor(left, pBoxOutput)
        left = right
        right = newRight
    output = inverseInitialPermutation(right + left)
    return binToStr(output)

def pkcs5Padding(input):
    padding = 8 - (len(input) % 8)
    return input + chr(padding) * padding

def pkcs5Unpadding(input):
    padding = ord(input[-1])
    return input[:-padding]

def ecbEncrypt(input, key):
    padded = pkcs5Padding(input)
    
    blocks = []
    for i in range(0, len(padded), 8):
        blocks.append(padded[i:i+8])
    
    cipherText = ""
    for block in blocks:
        cipherText += encrypt(strToBin(block), strToBin(key))
    return cipherText

def ecbDecrypt(input, key):
    blocks = []
    for i in range(0, len(input), 8):
        blocks.append(input[i:i+8])
    
    padded = ""
    for block in blocks:
        padded += decrypt(strToBin(block), strToBin(key))

    plainText = pkcs5Unpadding(padded)    
    return plainText

def cbcEncrypt(input, key, iv):
    padded = pkcs5Padding(input)
    
    blocks = []
    for i in range(0, len(padded), 8):
        blocks.append(padded[i:i+8])
    
    cipherText = ""
    prevCipherText = strToBin(iv)
    for block in blocks:
        xorWithPrev = stringXor(strToBin(block), prevCipherText)
        cipherTextBlock = encrypt(xorWithPrev, strToBin(key))
        cipherText += cipherTextBlock
        prevCipherText = strToBin(cipherTextBlock)
        
    return cipherText

def cbcDecrypt(input, key, iv):
    blocks = []
    for i in range(0, len(input), 8):
        blocks.append(input[i:i+8])
    
    plainText = ""
    prevCipherText = strToBin(iv)
    for block in blocks:
        decryptedBlock = decrypt(strToBin(block), strToBin(key))
        xorWithPrev = stringXor(strToBin(decryptedBlock), prevCipherText)
        plainText += binToStr(xorWithPrev)
        prevCipherText = strToBin(block)
        
    plainText = pkcs5Unpadding(plainText)
    return plainText