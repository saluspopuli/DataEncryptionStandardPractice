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
    key = BitArray(hex="ACD13BC7D842FC89")  # key in hex
    input_string = "Andre Cortez Gwapo"  # test string to be encrypted

    # Generated Tables for permutations
    PC1 = random.sample(range(1,65),64)  # generates PC1 table
    PC2 = random.sample(range(1,57),56)[0:48]  # generates PC2 table

    IP = random.sample(range(1,65),64)

    PC_KEY = random.sample(range(1,65),64)

    SBOX = []

    for index in range(8):
        tmp = [random.randint(0, 15) for _ in range(64)]
        SBOX.append(tmp)

    for i in range(8):
        print(SBOX[i])  #todo: remove

    S_PERM = random.sample(range(1, 33), 32)
    F_PERM = random.sample(range(1,65), 64)

    # PC1 = [57,49,41,33,25,17, 9, 1,
    #        58,50,42,34,26,18,10, 2,
    #        59,51,43,35,27,19,11, 3,
    #        60,52,44,36,63,55,47,39,
    #        31,23,15, 7,62,54,46,38,
    #        30,22,14, 6,61,53,45,37,
    #        29,21,13, 5,28,20,13, 4]
    #
    # PC2 = [14,17,11,24, 1, 5,
    #         3,28,15, 6,21,10,
    #        23,19,12, 4,26, 8,
    #        16, 7,27,20,13, 2,
    #        41,52,31,37,47,55,
    #        30,40,51,45,33,48,
    #        44,49,39,56,34,53,
    #        46,42,50,36,29,32]

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

    key = permutate_bitarray(key, PC_KEY, 64)
    print(key)  #todo: remove


    # Removing every 8th bit =====================================================================
    # Removes every 8th bit from the 64-bit key

    key2 = BitArray(length=56)
    j = 0

    # Removes every 8th bit from the key to produce a 56 bit key
    for i in range(0,64):
        if (i+1) % 8 != 0:
            key2[j] = key[i]
            j += 1

    print(key)  # todo: remove these
    print(key2)

    # Key permutation and slicing from 56 bits to 48 bits =========================================
    keys = []
    tmp = key2

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
