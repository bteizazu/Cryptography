# Set 1, Challenge 6: Break repeating-key XOR


from itertools import combinations
from base64 import b64encode, b64decode

encodedString = ''
key_length_dict={}
min_keylength_arr = []
#finding the key_size that yields the minimum hamming distance for each string in the txt file
#logging this key size value for each line

fileObject = open("/Users/bteizazu/cryptochallenge36.txt", "r")
data = fileObject.read().replace('\n', '')
filedata_hex = b64_2_hex(data)
string_bin = base64_2_bin(data)


#filedata_hex = '0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f'
#string_bin = hex_2_bin(filedata_hex)


char_length = len(string_bin)/8
key_length_dict = {}
for key_length in range(2,min(41,int(len(string_bin)/16))):
        
    hamming_dist = 0
 
    key_bitsize = key_length*8
    hamming_pair = 2*key_bitsize
    pairings = int(len(string_bin)/hamming_pair)
    
    for i in range(pairings):
        c1_start = i*hamming_pair
        c1_end = c1_start + key_bitsize
        c2_start = c1_end
        c2_end = c1_end + key_bitsize
        chunk1 = string_bin[c1_start:c1_end] #key_length*8 -> Each character in key is 8 bits long
        chunk2 = string_bin[c2_start:c2_end]

        hamming_dist += bitwiseHammingDist(chunk1,chunk2)
    
    print (hamming_dist , key_bitsize , pairings)
    hamming_dist_norm = (hamming_dist / key_bitsize) / pairings
    key_length_dict[key_length]=hamming_dist_norm




suggested_key_lengths = dict(sorted(key_length_dict.items(), key=lambda x: x[1])[0:10])

print('Suggested key lengths : corresponding hamming distances')
for i in suggested_key_lengths:
    print (i, ':', suggested_key_lengths[i])
    #https://towardsdatascience.com/sorting-a-dictionary-in-python-4280451e1637
    #https://careerkarma.com/blog/python-sort-a-dictionary-by-value/
key_length_min_hamming = min(key_length_dict, key=key_length_dict.get)

def break_it_up(a_string:str,groups:int,data_type = "ASCII"):
    
    #break a string up into groups, alternating from the start to the end of the string:
    #           String = 'This is an example string', Groups = 4
    #                     |||||||||||||||||||||||||
    #  Group Assignment=  1234123412341234123412341 , Output = ['T axltg', 'hinaer', 'is m i', 's epsn']
    ##e.g.: String = 'ABCDEFG', groups = 3, Output = ['ADG','BE','CF']
    string_segmented = ['']*groups
    group_count = 0
    
    if data_type == "ASCII":
        byte_size = 1
    if data_type == "hex":
        byte_size = 2
    if data_type == "binary":
        byte_size = 8
        
    assert (len(a_string) % byte_size == 0)
    
    char_count = 0
    char_limit = byte_size - 1
    
    
    for char in a_string:
        
        segmenter = group_count % (groups)
        string_segmented[segmenter] += char
        
        if (char_count == char_limit):
            char_count = 0
            group_count+=1
        else:
            char_count += 1
    
    return string_segmented


def bring_it_together(string_list:list, data_type = "ASCII"):
    #inverse function of 'break_it_up'
    count = 0
    assembled_string = ''
    if data_type == "ASCII":
        byte_size = 1
    if data_type == "hex":
        byte_size = 2
    if data_type == "binary":
        byte_size = 8
    limit = len(string_list[0])/byte_size
    while (count < limit):
        for string in string_list:
            try:
                if count<len(string)/byte_size:
                    assembled_string += string[byte_size*count:byte_size*(count+1)]
            except TypeError:
                pass
        count += 1
    return assembled_string

thex_string = '1d363c37'
thex_break = break_it_up(thex_string, groups = 3, data_type = 'hex')
thex_bring = bring_it_together(thex_break, data_type = 'hex')

tascii_string = 'This string is to test that bring_it_together inverts break_it_upp'
tascii_break = break_it_up(tascii_string, groups = 3,data_type = 'ASCII')
tascii_bring = bring_it_together(tascii_break, data_type = 'ASCII')


tbinary_string = '10111011010101011011011010110101'
tbinary_break = break_it_up(tbinary_string, groups = 2, data_type = 'binary')
tbinary_bring = bring_it_together(tbinary_break, data_type = 'binary')


assert thex_bring == thex_string
assert tbinary_bring == tbinary_string
assert tascii_bring == tascii_string



#parsing and segmenting text file into bins by key length number
segmented_file_list = []
Guesses = []

#segmented_file_list -> A list of lists containing the file segmented into groups for each suggested key length
for i in suggested_key_lengths:
    segmented_file_list.append(break_it_up(filedata_hex,groups = i, data_type = 'hex'))

for segmented_file in segmented_file_list:
    
    #segmented_file -> A list containing the file segmented into groups based on a given suggested key length
    
    decoded_file_segments = []*len(segmented_file)
    possible_key = ''
    
    for file_segment in segmented_file:
        
        #file_segment -> A string containing part of the file
        
        [decoded_string, key] = keyGuesser(file_segment)
        possible_key += key
        decoded_file_segments.append(decoded_string)

    possible_decoded_text = bring_it_together(decoded_file_segments, data_type = 'ASCII')

    possible_decoded_text.replace('\n', '\n ')
                
            
    print([possible_key,possible_decoded_text])
    Guesses.append([possible_key,possible_decoded_text[0:50]])
for item in Guesses:
    print(item)
