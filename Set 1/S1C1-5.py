#Set 1 Challenge 1: Convert hex to b64
def hex_2_b64(hex_str):
    # hex -> base64
    b64 = b64encode(bytes.fromhex(hex_str)).decode()
    return b64

#Set 1 Challenge 2: Fixed XOR
a = '1c0111001f010100061a024b53535009181c'
a = bin(int(a, 16))
b = '686974207468652062756c6c277320657965'
b = bin(int(b, 16))
output = int(a,2)^int(b,2)
output = hex(output)
output = output[2:] #hex output yields 0x at the beginning of the string

print(output)

#Set 1 Challenge 3: Single-byte XOR cipher

#References:
##https://www.codementor.io/@arpitbhayani/deciphering-single-byte-xor-ciphertext-17mtwlzh30
##https://www.megacolorboy.com/posts/the-cryptopals-crypto-challenges-set-1--singlebyte-xor-cipher/
##https://cedricvanrompay.gitlab.io/cryptopals/challenges/01-to-08.html

#FillFactor used to decode string. Hexadecimal representation of ASCII characters are two digits long.
##Fill factor used to repeat the ASCII character to match the length of the encoded string during
##the XOR operation
#####e.g.: target string = '1a2b3c4d' (four ASCII characters), key = 5e (one character)
#####             target string: 1a2b3c4d
#####      key with fill factor: 5e5e5e5e

a = '1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'
fillFactor = int(len(a)/2)

eng_alphabet_freq = {
    'a': 8.2389258,    'b': 1.5051398,    'c': 2.8065007,    'd': 4.2904556,
    'e': 12.813865,    'f': 2.2476217,    'g': 2.0327458,    'h': 6.1476691,
    'i': 6.1476691,    'j': 0.1543474,    'k': 0.7787989,    'l': 4.0604477,
    'm': 2.4271893,    'n': 6.8084376,    'o': 7.5731132,    'p': 1.9459884,
    'q': 0.0958366,    'r': 6.0397268,    's': 6.3827211,    't': 9.1357551,
    'u': 2.7822893,    'v': 0.9866131,    'w': 2.3807842,    'x': 0.1513210,
    'y': 1.9913847,    'z': 0.0746517,    ' ': 0
}

dictlist = []
#Declaring variables for decoded String (string with the highest eng_alphabet_freq score)
maxScore = 0
max_hexval = None
max_key = None
decodedString = None

#Iterating through 256 ASCII characters
for charDec in range(256):
    #Converting charDec (decimal) to hexval (hexadecimal)
    hexval = (hex(charDec)[2:]).zfill(2)
    
    #Exception handling for UnicodeDecodeError. Sometimes appears with the .decode() operation
    #Idk why this shows up. Maybe some characters aren't being recognized as valid ASCII/UTF-8
    #characters by Python or JupyterLab
    try:
        key = bytes.fromhex(hexval).decode('UTF-8')
    except UnicodeDecodeError:
        key = hexval
    
    #print(charDec, hexval)
    
    #reverse XOR, decoding message with key?
    b = hexval*fillFactor
    _str = hex(int(a,16)^int(b,16))[2:].zfill(len(a))
    
    
    #Scoring string by eng_alphabet_freq: 
    #Score is calculated by taking the sum total of each english character's frequency value
    ##for loop iterates through each character in the decoded string, and checks if it exists in 
    ##eng_alphabet_freq (checking to see if it's a valid english alphabet character). If the character is 
    ##in the alphabet, then it's value from eng_alphabet_freq is added to the score for the string.



    try:
    #Exception handling for UnicodeDecodeError.

        #Converting reverse XOR string to ASCII/UTF-8
        ascii_str = bytes.fromhex(_str).decode('UTF-8')
        
        
        #Initializing score, alphaChars variables
        score = 0
        alphaChars = 0
        
        
        #Iterating through each character in ascii_str, calculating total score 
        for char in ascii_str:
            lowerChar = char.lower()
            if lowerChar in eng_alphabet_freq:
                score = score + eng_alphabet_freq[lowerChar]
                alphaChars = alphaChars+1
            else:
                pass
            
        if (alphaChars/len(ascii_str) < 0.8):
            score = 0
        else:
            score = score/alphaChars        
            dictlist.append((score,key,ascii_str))
       

        #Recording variables associated with the string with the max Score:
        if score > maxScore:
            maxScore = score
            max_key = key
            max_hexval = hexval
            decodedString = ascii_str
    
           

    except UnicodeDecodeError: 
        #print(charDec, hexval, " UnicodeDecodeError")
        #print(_str, " : 'ascii' codec can't decode byte 0x9c in position 0: ordinal not in range(128)")
        pass
    #if any(c not in arr for c in _str):  # Don't use str as a name.
        
    
    #print(charDec , " " ,hexval, " ", b , " " , _str)

#print(sorted(dictlist,reverse = True)[:10])
print(decodedString, " ", str(maxScore), " ", 'key = ' + str(max_key))
print(dictlist)

#Set 1 Challenge 4: Detect single-character XOR


def isvalidEnglishstring(string):
    a = string
    fillFactor = int(len(a)/2)

    eng_alphabet_freq = {
        'a': 8.2389258,    'b': 1.5051398,    'c': 2.8065007,    'd': 4.2904556,
        'e': 12.813865,    'f': 2.2476217,    'g': 2.0327458,    'h': 6.1476691,
        'i': 6.1476691,    'j': 0.1543474,    'k': 0.7787989,    'l': 4.0604477,
        'm': 2.4271893,    'n': 6.8084376,    'o': 7.5731132,    'p': 1.9459884,
        'q': 0.0958366,    'r': 6.0397268,    's': 6.3827211,    't': 9.1357551,
        'u': 2.7822893,    'v': 0.9866131,    'w': 2.3807842,    'x': 0.1513210,
        'y': 1.9913847,    'z': 0.0746517,    ' ': 0
    }
    dictlist = []

    #Declaring variables for decoded String (string with the highest eng_alphabet_freq score)
    maxScore = 0
    max_hexval = None
    max_key = None
    decodedString = None

    #Iterating through 256 ASCII characters
    for charDec in range(256):
        #Converting charDec (decimal) to hexval (hexadecimal)
        hexval = (hex(charDec)[2:]).zfill(2)

        #Exception handling for UnicodeDecodeError. Sometimes appears with the .decode() operation
        #Idk why this shows up. Maybe some characters aren't being recognized as valid ASCII/UTF-8
        #characters by Python or JupyterLab
        try:
            key = bytes.fromhex(hexval).decode('ASCII')
        except UnicodeDecodeError:
            key = hexval

        #print(charDec, hexval)

        #reverse XOR, decoding message with key?
        b = hexval*fillFactor
        _str = hex(int(a,16)^int(b,16))[2:].zfill(len(a))


        #Scoring string by eng_alphabet_freq: 
        #Score is calculated by taking the sum total of each english character's frequency value
        ##for loop iterates through each character in the decoded string, and checks if it exists in 
        ##eng_alphabet_freq (checking to see if it's a valid english alphabet character). If the character is 
        ##in the alphabet, then it's value from eng_alphabet_freq is added to the score for the string.

        



        try:
        #Exception handling for UnicodeDecodeError.

            #Converting reverse XOR string to ASCII/UTF-8
            ascii_str = bytes.fromhex(_str).decode('UTF-8')


            #Initializing score, alphaChars variables
            score = 0
            alphaChars = 0

            #Iterating through each character in ascii_str, calculating total score 
            for char in ascii_str:
                lowerChar = char.lower()
                if lowerChar in eng_alphabet_freq:
                    score = score + eng_alphabet_freq[lowerChar]
                    alphaChars = alphaChars+1
                else:
                    pass

            score = score/len(ascii_str) * (alphaChars/len(ascii_str))       



            #Recording variables associated with the string with the max Score:
            if score > maxScore:
                maxScore = score
                max_key = key
                max_hexval = hexval
                decodedString = ascii_str


        except UnicodeDecodeError: 
            #print(charDec, hexval, " UnicodeDecodeError")
            #print(_str, " : 'ascii' codec can't decode byte 0x9c in position 0: ordinal not in range(128)")
            pass
        #if any(c not in arr for c in _str):  # Don't use str as a name.


        

    #print(sorted(dictlist,reverse = True)[:10])
    #print(decodedString, " ", str(maxScore), " ", 'key = ' + str(max_key))


    return(decodedString,maxScore,max_key, max_hexval)



maxList = []

#get file object
fileObject = open("cryptochallenge34.txt", "r")
num = 0
while(True):
    #read next line
    line = fileObject.readline()
    num = num + 1
    #if line is empty, you are done with all lines in the file
    if not line:
        break
    #you can access the line
    #print("String " + str(num) + "/328: ", line.strip())
    [decodedString, maxScore, max_key, max_hexval] = isvalidEnglishstring(line.strip())
    if maxScore != 0:
        maxList.append([maxScore, max_key, max_hexval, decodedString])


      #  print(decodedString, " ", str(maxScore), " ", 'key = ' + str(max_key), 'hexval = ' + str(max_hexval))
maxList.sort(key = lambda i: i[0], reverse = True)
print("decodedString: " + str(maxList[0][3]), 'key = ' + maxList[0][1], 'hexval = ' + str(maxList[0][2]))
print()

for item in maxList[0:10]:
    print(item)

#close file
fileObject.close

#Set 1, Challenge 5: Implement repeating-key XOR
vanillaIce_string = "Burning 'em, if you ain't quick and nimble I go crazy when I hear a cymbal"
vanillaXOR = []
solution_string=''

count = 3

I_binary = (bin(ord('I'))[2:].zfill(8))
C_binary = (bin(ord('C'))[2:].zfill(8))
E_binary = (bin(ord('E'))[2:].zfill(8))

for scoop_char in vanillaIce_string:
    scoop_byte = (bin(ord(scoop_char))[2:].zfill(8))
    
    ICE_counter = count%3

    if ICE_counter == 0:
        XOR_val = bin(int(scoop_byte,2)^int(I_binary,2))
        solution_string = solution_string + XOR_val[2:].zfill(8)
    if ICE_counter == 1:
        XOR_val = bin(int(scoop_byte,2)^int(C_binary,2))
        solution_string = solution_string + XOR_val[2:].zfill(8)
    if ICE_counter == 2:
        XOR_val = bin(int(scoop_byte,2)^int(E_binary,2))
        solution_string = solution_string + XOR_val[2:].zfill(8)
    
    count = count+1



solution_string = hex(int(solution_string,2))[2:]

print(solution_string)
