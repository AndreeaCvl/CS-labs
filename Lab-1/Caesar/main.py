from CaesarSubst import CaesarSubst

# string which will be encoded
t1 = "This is a test!"
t2 = "Another String for Testing the Algorithms..."

# initializing the class
test_1 = CaesarSubst()

if __name__ == "__main__":

    # encryption
    print("Encrypted text:")
    e1 = test_1.encrypt(t1, 5)
    print(e1)
    e2 = test_1.encrypt(t2, 25)
    print(e2)

    # decryption
    print("\nDecrypted text:")
    d1 = test_1.decrypt(e1, 5)
    print(d1)
    d2 = test_1.decrypt(e2, 25)
    print(d2)
