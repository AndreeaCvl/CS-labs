from CipherMethods import CipherMethods


class DES(CipherMethods):
    def __init__(self, PC1, PC2, IP, ST, S, SBP, FP):
        super().__init__('DES')

        # hyperparameters - the permutation tables
        self.PC1 = PC1  # PC-1 - length 56 - applied to key
        self.PC2 = PC2  # PC-2 - length 48 - applied to key
        self.IP = IP  # Initial Permutation - length 64 - applied to message
        self.ST = ST  # E Bit-selection table - length 48
        self.S = S  # S boxes list, array of 8 matrices with dimensions 16x4
        self.SBP = SBP  # P - length 32 - permutation of S-box output
        self.FP = FP  # the final permutation - length 64

    # function for splitting any string in substrings of length = size
    def splitting(self, string, size):
        splitted = [string[i:i + size] for i in range(0, len(string), size)]
        return splitted

    # function for conversion from hex to binary
    def hex_to_binary(self, t):
        res = "{:064b}".format(int(t, 16))
        return res

    def bin_to_hex(self, n):
        # convert binary to int
        num = int(n, 2)

        # convert int to hexadecimal
        hex_num = hex(num)
        return (hex_num)[2:]

    # making permutations of any target array, using a table with the new indices
    def permutations(self, target, table):
        p = ''
        for i in range(len(table)):
            p += target[table[i] - 1]
        return p

    def left_shift(self, C, D):
        # 7. Left shift each each round (16 times) create Cn Dn
        for i in range(1, 17):

            if i in [1, 2, 9, 16]:
                num = 1
            else:
                num = 2

            c = C[i - 1][num::] + C[i - 1][:num:]
            C[i] = c

            d = D[i - 1][num::] + D[i - 1][:num:]
            D[i] = d

        return C, D

    # generating a new binary sequence of 48 bits using the E-bits selection table
    def do_er(self, r):
        er = ''
        table = self.ST
        for i in range(len(self.ST)):
            er += r[table[i] - 1]
        return er

    # function for xoring 2 binary values
    def xor(self, a, b, l):

        xor = ''

        for j in range(l):
            if a[j] == b[j]:
                xor += '0'
            else:
                xor += '1'

        return xor

    def s_box(self, seq, table):
        new_seq = ''

        row = int(seq[0] + seq[-1], 2)
        col = int(seq[1:5], 2)

        new_seq_dec = table[row][col]
        new_seq = '{:04b}'.format(new_seq_dec)

        return new_seq

    # generating "half-keys"
    def half_keys(self, KEY_PC2, L, R):
        for i in range(1, 17):
            L[i] = R[i - 1]

            # e-bit table permutations
            er = self.do_er(R[i - 1])

            # xor the er result with KEY_PC2
            XOR_1 = self.xor(er, KEY_PC2[i - 1], len(er))

            # splittion the above obtained result in 6 equal parts
            bbb = self.splitting(XOR_1, 6)

            # applying the s boxes
            n = 0
            new_seq = ''
            for seq in bbb:
                new_seq += self.s_box(seq, self.S[n])
                n += 1

            # permutations of the result obtained after S-bixes algorithm
            new_seq = self.permutations(new_seq, self.SBP)

            # Xor the values from L with new_seq
            XOR_2 = self.xor(L[i - 1], new_seq, len(L[i - 1]))

            # assigning a new value to R[i]
            R[i] = XOR_2

        return L, R

    # creating the key PC-2
    def key_processing(self, key_bin):

        # permutation of the key according to the PC1 table
        key_pc1 = self.permutations(key_bin, self.PC1)

        # init empty lists for storing the half-keys 1..16
        C = [None] * 17
        D = [None] * 17

        # splitting the key in left and right parts
        s = self.splitting(key_pc1, int(len(key_pc1) / 2))

        # stiring C0 and D0 inside lists
        C[0] = s[0]
        D[0] = s[1]

        # left shift
        C, D = self.left_shift(C, D)

        # 8. form the keys Kn (16 rounds)
        K_shift = [None] * 17
        for i in range(17):
            K_shift[i] = C[i] + D[i]

        # creating permutations of the key according to the PC2 table
        KEY_PC2 = [''] * 16
        for j in range(1, 17):
            KEY_PC2[j - 1] += self.permutations(K_shift[j], self.PC2)

        return KEY_PC2

    # function for encrypting the message
    def encrypt(self, cipher):
        super().encrypt(cipher)

        PT = cipher.message
        key = cipher.key

        # 1. Convert text to hex
        PT_hex = PT.encode().hex()

        # splitting the hex text into chunks of 16 characters (hex format)
        splitted = self.splitting(PT_hex, 16)

        # Key to binary (init length 64 bits)
        key_bin = self.hex_to_binary(key)

        # obtaining a new key using the key processing function
        KEY_PC2 = self.key_processing(key_bin)

        # init a string for storing the encoded message
        ciphertext = ''

        # itterating trough 64-bit blocks of the input message
        for i in splitted:
            PT_hex = i

            # 2. Hex message to binary
            PT_bin = self.hex_to_binary(PT_hex)

            # initial permutation
            text_ip = self.permutations(PT_bin, self.IP)

            # init tables for storing L and R for each iteration
            L = [None] * 17
            R = [None] * 17

            # splitting the message afer applying the IP in Left and Right sides
            s = self.splitting(text_ip, int(len(text_ip) / 2))
            L[0] = s[0]
            R[0] = s[1]

            # Generating new half keys L and R
            L, R = self.half_keys(KEY_PC2, L, R)

            # creating a new key
            K16 = R[16] + L[16]

            # applying the final permutation
            fp_text = self.permutations(K16, self.FP)

            # append new encoded sequence to ciphertext
            ciphertext += self.bin_to_hex(fp_text)

        return ciphertext

    # function for decripting the encoded message
    def decrypt(self, cipher):
        super().decrypt(cipher)

        enc = cipher.message
        key = cipher.key

        PT_hex = enc

        # splitting the hex text into chunks of 16 characters (hex format)
        splitted = self.splitting(PT_hex, 16)

        # Key to binary (init length 64 bits)
        key_bin = self.hex_to_binary(key)

        # generating the new key
        KEY_PC2 = self.key_processing(key_bin)

        # reversing the key
        KEY_PC2 = KEY_PC2[::-1]

        decoded = ''

        for i in splitted:
            PT_hex = i

            # 2. Hex message to binary
            PT_bin = self.hex_to_binary(PT_hex)

            # initial permutation
            text_ip = self.permutations(PT_bin, self.IP)

            # init tables for storing L and R for each iteration
            L = [None] * 17
            R = [None] * 17

            # splitting the message afer applying the IP in Left and Right sides
            s = self.splitting(text_ip, int(len(text_ip) / 2))
            L[0] = s[0]
            R[0] = s[1]

            # creating half-keys
            L, R = self.half_keys(KEY_PC2, L, R)

            # creating a new key
            K16 = R[16] + L[16]

            # applying the final permutation
            fp_text = self.permutations(K16, self.FP)

            # append new decoded sequence to the decoded string
            decoded += self.bin_to_hex(fp_text)

        # decoding te result from hex to utf-8
        decoded = bytes.fromhex(decoded).decode('utf-8')

        return decoded
