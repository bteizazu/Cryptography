import base64

def str_2_bin(string):
    #converts a string from text to binary
    stringBinary = ''    
    for char in string:
        stringBinary = stringBinary + (bin(ord(char))[2:].zfill(8))
    return stringBinary

def str_2_bin_array(string):
    #converts a string from text to an array of binary bytes
    stringBinary = []    
    for char in string:
        stringBinary.append(bin(ord(char))[2:].zfill(8))
    return stringBinary

def hex_2_b64(hex_str):
    # hex -> base64
    b64 = b64encode(bytes.fromhex(hex_str)).decode()
    return b64
def hex_2_bin(hex_str):
    bin_string = bin(int(hex_str, 16))[2:].zfill(4*len(hex_str))
    return bin_string
def b64_2_hex(b64_str):
    # base64 -> hex
    h = b64decode(b64_str.encode()).hex()
    return h

def bin_array_2_str(bin_array):
    #converts an array of binary bytes to a string
    str_decoded = ''
    for byte in test_str_bin:
        str_decoded += chr(int(byte,2))
    return str_decoded

def base64_2_bin(string):
    #https://stackoverflow.com/questions/43207978/python-converting-from-base64-to-binary
    decoded = base64.b64decode(string)
    stringBinary = ("".join(["{:08b}".format(x) for x in decoded]))
    
    return stringBinary

def bitwiseHammingDist(string1,string2):
    #string1, binary
    #string2, binary
    if len(string1) != len(string2):
        raise ValueError("Bröther, String sizes don't match")
    else:
        string3 ='{0:b}'.format(int(string1,2)^int(string2,2))
            #XOR function will give a 1 if the bits are different and a 0 if they are the same
            #Summing the number of 1 bits of the XOR function yields the Hamming distance
        count = 0
        for num in string3:
            if num == '1':
                count = count+1

    return count



def keyGuesser(a:str):
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

            if (alphaChars/len(ascii_str) < 0.85):
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
    #print(decodedString, " ", str(maxScore), " ", 'key = ' + str(max_key))
    #print(dictlist)
    
    return (decodedString, str(max_key))

