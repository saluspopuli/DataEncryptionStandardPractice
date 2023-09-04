from bitstring import Bits, BitArray, BitStream, pack
import random

def shift_key(input_bit_array, round_number, PC2):

    return_key = BitArray(length=48)
    left_key = input_bit_array[:28]
    right_key = input_bit_array[28:]

    shift_number = 2

    if round_number in {1, 2, 9, 16}:
        shift_number = 1

    left_key <<= shift_number
    right_key <<= shift_number

    final_key = left_key + right_key

    for index in range(48):
        return_key[index] = final_key[PC2[index]-1]

    return return_key

# =================================== MAIN CODE ==============================================


if __name__ == '__main__':

    # Input values and parameters
    random.seed("andre")  # Sets random seed for reproducibility of tables/arrays
    key = BitArray(hex="ACD13BC7D842FC89")  # key in hex
    input_string = "Andre Cortez Gwapo"  # test string to be encrypted

    # Generated Tables for permutations
    PC1 = random.sample(range(1,65),64)  # generates PC1 table
    PC2 = random.sample(range(1,57),56)[0:48]  # generates PC2 table

    # Slicing of bitstream into list =============================================================

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
    # Permutates the plaintext/bitstream message chunks

    print(PC1)  # todo: remove

    chunks2 = BitArray(length=64)

    # Permutates the plaintext bits by moving them around according to the order of the addresses in the PC1 array
    for chunk in chunks:
        for i in chunk:
            chunks2[i] = key[PC1[i] - 1]

    print(chunks2.bin)  # todo: remove these
    print(chunks2.bin)

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

    print(shift_key(key2,1, PC2))  # todo: remove these




