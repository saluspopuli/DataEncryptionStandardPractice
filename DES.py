from bitstring import Bits, BitArray, BitStream, pack
import random


def shift_key(input_bit_array, round_number):

    left_key = input_bit_array[:28]
    right_key = input_bit_array[28:]

    shift_number = 2

    if round_number in {1, 2, 9, 16}:
        shift_number = 1

    tmp_left_key = left_key[:shift_number]
    tmp_right_key = right_key[:shift_number]

    left_key <<= shift_number
    right_key <<= shift_number

    left_key = left_key[:-shift_number] + tmp_left_key
    right_key = right_key[:-shift_number] + tmp_right_key

    final_key = left_key + right_key

    return final_key



def permutate_bitarray(input_bit_array, table, length):

    permuted_array = BitArray(length=length)

    for index in range(length):
        permuted_array[index] = input_bit_array[table[index]-1]

    return permuted_array


def DES_round(message, key, IP, SBOX, S_PERM):
    selection_table = [31, 1,  2,  3,  4,  5,
                       4,  5,  6,  7,  8,  9,
                       8,  9,  10, 11, 12, 13,
                       12, 13, 14, 15, 16, 17,
                       16, 17, 18, 19, 20, 21,
                       20, 21, 22, 23, 24, 25,
                       24, 25, 26, 27, 28, 29,
                       28, 29, 30, 31, 32, 1]

    permuted_text = permutate_bitarray(message, IP, 64)
    print(permuted_text.bin)    # todo: remove

    left_text = permuted_text[:32]
    right_text = permuted_text[32:]

    print(right_text.bin)       # todo: remove
    right_text = permutate_bitarray(right_text, selection_table, 48)
    print(right_text.bin)       # todo: remove
    print(key.bin)              # todo: remove
    right_text = right_text ^ key
    print("Right Text: ")       # todo: remove
    print(right_text.bin)       # todo: remove

    sliced_bits = []

    for i in range(8):
        tmp = right_text [:6]
        right_text = right_text[6:]

        sliced_bits.append(tmp)

    print("not shifted")
    for i in range(8):
        print(sliced_bits[i].bin)   # todo: remove

    sliced_bits = [(bit[0:1] + bit[5:] + bit[1:5]) for bit in sliced_bits]

    print("shifted")
    for i in range(8):
        print(sliced_bits[i])   # todo: remove

    sliced_bits = [int(bit.bin, 2) for bit in sliced_bits]

    print("number")
    for i in range(8):
        print(sliced_bits[i])  # todo: remove

    tmp2 = []
    for i in range(8):
        tmp = SBOX[i]
        tmp2.append(tmp[sliced_bits[i]])

    sliced_bits = tmp2

    print("shortened")
    for i in range(8):
        print(sliced_bits[i])  #todo: remove

    tmp2 = ""
    for i in range(8):
        tmp = bin(sliced_bits[i])[2:].zfill(4)
        tmp2 = tmp2 + tmp

    sliced_bits = BitArray('0b' + tmp2)
    print(sliced_bits.bin)  #todo: remove

    sliced_bits = permutate_bitarray(sliced_bits,S_PERM,32)

    print(sliced_bits.bin)  #todo: remove

    final_message = sliced_bits ^ left_text
    final_message = sliced_bits + left_text

    return final_message



# =================================== MAIN CODE ==============================================


if __name__ == '__main__':

    # Input values and parameters
    random.seed("andre")  # Sets random seed for reproducibility of tables/arrays
    key = BitArray(hex="ACD13BC7D842FC8F")  # key in hex
    input_string = "Andre Cortez Gwapo"  # test string to be encrypted

    # Generated Tables for permutations
    # PC1 = random.sample(range(1,65),64)  # generates PC1 table
    # PC2 = random.sample(range(1,57),56)[0:48]  # generates PC2 table
    #
    # IP = random.sample(range(1,65),64)
    #
    # PC_KEY = random.sample(range(1,65),64)
    #
    # SBOX = []
    #
    # for index in range(8):
    #     tmp = [random.randint(0, 15) for _ in range(64)]
    #     SBOX.append(tmp)
    #
    # for i in range(8):
    #     print(SBOX[i])  #todo: remove
    #
    # S_PERM = random.sample(range(1, 33), 32)
    # F_PERM = random.sample(range(1,65), 64)


    PC1 = [57,49,41,33,25,17, 9, 1,
           58,50,42,34,26,18,10, 2,
           59,51,43,35,27,19,11, 3,
           60,52,44,36,63,55,47,39,
           31,23,15, 7,62,54,46,38,
           30,22,14, 6,61,53,45,37,
           29,21,13, 5,28,20,12, 4]

    PC2 = [14,17,11,24, 1, 5,
            3,28,15, 6,21,10,
           23,19,12, 4,26, 8,
           16, 7,27,20,13, 2,
           41,52,31,37,47,55,
           30,40,51,45,33,48,
           44,49,39,56,34,53,
           46,42,50,36,29,32]

    IP = [58, 50, 42, 34, 26, 18, 10, 2,
          60, 52, 44, 36, 28, 20, 12, 4,
          62, 54, 46, 38, 30, 22, 14, 6,
          64, 56, 48, 40, 32, 24, 16, 8,
          57, 49, 41, 33, 25, 17,  9, 1,
          59, 51, 43, 35, 27, 19, 11, 3,
          61, 53, 45, 37, 29, 21, 13, 5,
          63, 55, 47, 39, 31, 23, 15, 7]

    SBOX =[
        [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7,
         0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8,
         4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0,
         15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13],

        [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5 ,10,
         3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5,
         0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15,
         13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9],

        [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8,
         13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1,
         13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7,
         1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12],

        [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15,
         13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9,
         10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4,
         3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14],

        [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9,
         14, 11, 2, 12, 4, 7, 13, 1, 5 ,0, 15, 10, 3, 9, 8, 6,
         4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14,
         11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3],

        [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11,
         10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8,
         9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6,
         4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13],

        [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1,
         13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6,
         1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2,
         6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12],

        [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7,
         1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2,
         7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8,
         2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]
    ]

    S_PERM = [16,  7, 20, 21,
              29, 12, 28, 17,
               1, 15, 23, 26,
               5, 18, 31, 10,
               2,  8, 24, 14,
              32, 27,  3,  9,
              19, 13, 30,  6,
              22, 11,  4, 25]

    F_PERM = [40, 8, 48, 16, 56, 24, 64, 32,
              39, 7, 47, 15, 55, 23, 63, 31,
              38, 6, 46, 14, 54, 22, 62, 30,
              37, 5, 45, 13, 53, 21, 61, 29,
              36, 4, 44, 12, 52, 20, 60, 28,
              35, 3, 43, 11, 51, 19, 59, 27,
              34, 2, 42, 10, 50, 18, 58, 26,
              33, 1, 41,  9, 49, 17, 57, 25]

    #todo: finish up putting the actual tables

    # Slicing of message bitstream into list =============================================================

    bitstream = BitArray(bytes=input_string.encode())  # converts string into ASCII binary
    chunks = []

    for i in range(0, len(bitstream), 64):  # Slices the string into 64 bit chunks and puts it
        chunks.append(bitstream[i:i + 64])  # into a list

    # Pads final chunk with zeroes
    if chunks[len(chunks)-1] != 64:
        for i in range(len(chunks[len(chunks)-1]),64):
            chunks[len(chunks)-1].append(BitArray(uint=0, length=1))
            # this constructor is needed for some insane reason

    for i in range(len(chunks)):  # todo: remove
        print(chunks[i].bin)
        print(chunks[i].tobytes().decode("utf-8"))

    # Initial Permutation =======================================================================
    # Permutates the key

    print(key)
    print(key.bin)  # todo: remove these 3
    print(len(PC1))
    key = permutate_bitarray(key, PC1, 56)
    print(key)  #todo: remove


    # Key permutation and slicing from 56 bits to 48 bits =========================================
    keys = []
    tmp = key

    for i in range(0,16):  # Gets all 56 bit keys for all 16 rounds by shifting
        tmp = shift_key(tmp,i+1)
        keys.append(tmp)

    print("Printing new keys")  # todo: remove these
    for i in range(0,16):
        print(keys[i].bin)

    tmp = []
    for index in range(len(keys)):  # Permutes shifted 56 bit keys into 48 bits
        tmp.append(permutate_bitarray(keys[index], PC2, 48))

    keys = tmp

    print("Printing permuted keys")  # todo: remove these
    for i in range(0,16):
        print(keys[i].bin)

    tmp2 = []
    for i in range(len(chunks)):
        tmp = chunks[i]
        for j in range(16):
            tmp = DES_round(tmp, keys[j], IP, SBOX, S_PERM)
        tmp2.append(tmp)

    chunks = tmp2

    for i in range(len(chunks)):  #todo: remove
        print(chunks[i].bin)

    tmp = []
    for chunk in chunks:
        left = chunk[:32]
        right = chunk[32:]

        tmp.append(right+left)

    chunks = tmp

    for i in range(len(chunks)):  #todo: remove
        print(chunks[i].bin)

    tmp = []
    for chunk in chunks:
        tmp.append(permutate_bitarray(chunk, F_PERM, 64))

    chunks = tmp

    print("Final Answer")
    for i in range(len(chunks)):  #todo: remove
        print(chunks[i].bin)
        print(chunks[i].hex)
