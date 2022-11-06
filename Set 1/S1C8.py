#Set 1, Challenge 8: Detect AES
fileObject = open('/Users/bteizazu/Downloads/cryptopals38.txt','r')
data = fileObject.readlines()

for line in data:
    line_corrected = line[:-1]
    line_bin = hex_2_bin(line_corrected)
    byte_len = len(line_bin)//(8)
    num_blocks = byte_len//16
    block_array = []
    for i in range(num_blocks):
        block_array.append(line_bin[int(i*(8*16)):int((i+1)*(8*16))])
    
    if len(block_array) != len(set(block_array)):
        print(line_corrected)
        for block in block_array:
#            print(bin_2_str(block))
        
    
  
