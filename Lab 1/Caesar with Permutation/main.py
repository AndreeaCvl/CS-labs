from CaesarWihPermutation import CaesarWithPermutation

# string which will be encoded
t1 = "This is a test!"
t2 = "Another String for Testing the Algorithms..."

# initializing the class
test_2 = CaesarWithPermutation()

# creating a permutation of the alphabet
test_2.alpha_permutation()

# printing the obtained permutation of the alphabet
print(test_2.new_alphabet)


if __name__ == "__main__":

    # encryption
    print("\nEncrypted text:")
    e1 = test_2.encrypt(t1, 5)
    print(e1)
    e2 = test_2.encrypt(t2, 25)
    print(e2)

    # decryption
    print("\nDecrypted text:")
    d1 = test_2.decrypt(e1, 5)
    print(d1)
    d2 = test_2.decrypt(e2, 25)
    print(d2)
