# CipherMethods class for storing the methods used in RC4 and DES
class CipherMethods:
    def __init__(self, algorithm):
        self.algorithm = algorithm

    def encrypt(self, cipher):
        print("Encrypting the message with {} algorithm:".format(self.algorithm))
        return

    def decrypt(self, cipher):
        print("Decrypting the message with {} algorithm:".format(self.algorithm))
        return
