from RSA import RSA


PT = "Encoding this text with RSA algorithm"
key = {"q": 239, "p": 151}
e = 277


if __name__ == '__main__':
    c = RSA(PT, key, e=e)
    enc = c.encrypt()
    print("The encoded message:", enc)

    print()

    c = RSA(enc, key, d=c.d)
    dec = c.decrypt()
    print("The decoded message:", dec)