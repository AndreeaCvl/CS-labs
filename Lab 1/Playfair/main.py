from Playfair import Playfair

# string which will be encoded
t11 = 'THISISATEST'
t12 = 'ANOTHERSTRINGFORTESTINGTHEALGORITHMS'

# the key used for encoding / decoding
key = "SUNRISE"

# initializing the class
p = Playfair()

if __name__ == "__main__":

    # encryption
    print("Encrypted text:")
    e1 = p.encrypt(t11, key)
    print(e1)
    e2 = p.encrypt(t12, key)
    print(e2)

    # decryption
    print("\nDecrypted text:")
    d1 = p.decrypt(e1, key)
    print(d1)
    d2 = p.decrypt(e2, key)
    print(d2)
