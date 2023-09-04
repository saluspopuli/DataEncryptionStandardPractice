from bitstring import Bits, BitArray, BitStream, pack
import random

if __name__ == '__main__':
    random.seed("andre")  # Sets random seed for reproducibility of tables

    key = BitArray(hex="ACD13BC7D842FC89")  # key in hex
    input_string = "Andre Cortez Gwapo"  # test string to be encrypted

    bitstream = BitArray(bytes=input_string.encode())  # converts string into ASCII binary

    # Slicing of bitstream into list =============================================================

    chunks = []

    for i in range(0, len(bitstream), 64):  # Slices the string into 64 bit chunks and puts it
        chunks.append(bitstream[i:i + 64])  # into a list

    if chunks[len(chunks)-1] != 64:
        for i in range(len(chunks[len(chunks)-1]),64):  # Pads final chunk with zeroes
            chunks[len(chunks)-1].append(BitArray(uint=0, length=1))

    for i in range(len(chunks)):  # todo: remove
        print(chunks[i].bin)
        print(chunks[i].tobytes().decode("utf-8"))


    # Initial Permutation =======================================================================

    PC1 = random.sample(range(1,65),64)  # generates PC1 table
    print(PC1)  # todo: remove

    tmp = BitArray(length=64)
    for i in range(len(key)):
        tmp[i] = key[PC1[i] - 1]

    key2 = tmp

    print(key.bin)
    print(key2.bin)

    # Removing every 8th bit =====================================================================
    # todo: REDO THIS ENTIRE THING
    print("Supposed to be bit skipping here")

    chunks3 = []

    for chunk in chunks2:
        tmp = BitArray(length=56)
        j = -1

        for i in range(0,64):
            if (i+1) % 8 != 0:  # Skip every 8th bit
                j += 1
                tmp[j] = chunk[i]

        chunks3.append(tmp)

    for i in range(len(chunks3)):
        print(chunks3[i].bin)
