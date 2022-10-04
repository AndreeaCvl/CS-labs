from Vigenere import Vigenere

# string which will be encoded
t11 = 'THISISATEST'
t12 = 'ANOTHERSTRINGFORTESTINGTHEALGORITHMS'

# the key used for encoding / decoding
key = "TRAP"

# initializing the class
v = Vigenere()

if __name__ == "__main__":

    # encryption
    print("Encrypted text:")
    e1 = v.encrypt(t11, key)
    print(e1)
    e2 = v.encrypt(t12, key)
    print(e2)

    # decryption
    print("\nDecrypted text:")
    d1 = v.decrypt(e1, key)
    print(d1)
    d2 = v.decrypt(e2, key)
    print(d2)
