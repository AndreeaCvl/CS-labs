from CipherMethods import CipherMethods


class RC4(CipherMethods):
    def __init__(self):
        super().__init__('RC4')

        # initializing a state vector S
        self.S = [i for i in range(256)]

    # The key-scheduling algorithm used to initialize the permutation in the array "S"
    def key_scheduling(self, key):
        j = 0

        for i in range(256):
            j = (j + self.S[i] + key[i % len(key)]) % 256

            temp = self.S[j]
            self.S[j] = self.S[i]
            self.S[i] = temp

    # Each S[i] is swapped with another byte in S according to a scheme dictated by the current configuration of S.
    def key_stream(self):
        i = 0
        j = 0
        while True:
            i = (1 + i) % 256
            j = (self.S[i] + j) % 256
            temp = self.S[j]
            self.S[j] = self.S[i]
            self.S[i] = temp

            # After reaching S[255] the process continues, starting from S[0] again
            yield self.S[(self.S[i] + self.S[j]) % 256]

    # function for encrypting a message
    def encrypt(self, cipher):

        # giving access to methods from the class CipherMethods and parameters used when creating a Cipher class object
        super().encrypt(cipher)

        # Converting chars to ascii
        PT = [ord(char) for char in cipher.message]
        key = [ord(char) for char in cipher.key]

        # Calling the function for key scheduling
        self.key_scheduling(key)

        # Stream generation
        # ks is a generator object
        ks = self.key_stream()

        # Obtaining the result using xor with the obtained keystream
        result = ''
        for c in PT:
            xor = c ^ next(ks)
            add = str(hex(xor))
            result += add

        # returning the result
        return result

    # function for decrypting a message
    def decrypt(self, cipher):

        # giving access to methods from the class CipherMethods and parameters used when creating a Cipher class object
        super().decrypt(cipher)

        message = cipher.message

        # converting the message from hex to decimal
        encoded = message.split('0x')[1:]
        encoded = [int('0x' + c.lower(), 0) for c in encoded]

        # Converting chars to ascii
        key = [ord(char) for char in cipher.key]

        # calling the key scheduling algorithm
        self.key_scheduling(key)

        # Stream Generation
        ks = self.key_stream()

        result = ''

        # decrypting the message using xor, just as in case of encryption. This time using the encoded message
        for c in encoded:
            dec = str(chr(c ^ next(ks)))
            result += dec

        return result
