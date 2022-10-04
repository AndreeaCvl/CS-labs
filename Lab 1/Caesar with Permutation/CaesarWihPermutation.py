import random


class CaesarWithPermutation:
    #  a class which will contain the encryption function for Caesar cipher with one key used for substitution

    def __init__(self):
        """
            The constructor of the class
        """
        self.upper_alphabet = None
        self.new_alphabet = None

    def alpha_permutation(self):
        # creates a permutation of the alphabet

        # initial alphabet order
        alphabet = 'abcdefghijklmnopqrstuvwxyz'

        self.new_alphabet = ''

        # shuffles the initial alphabet
        self.new_alphabet = ''.join(random.sample(alphabet, len(alphabet)))

        # creates an alphabet with uppercase letters only
        self.upper_alphabet = self.new_alphabet.upper()

    def encrypt(self, message, s):
        """
            The function for encoding
                :param message: string
                    The message to be encoded
                :param s: integer
                    The shift
                :return: string
                    The encoded message
        """

        result = ""

        # traverse text
        for i in range(len(message)):
            c = message[i]

            # Encryption of uppercase characters
            if c.isupper():
                idx = self.upper_alphabet.index(c)
                result += self.upper_alphabet[(idx + s) % 26]

            # Encryption of lowercase characters
            elif c.islower():
                idx = self.new_alphabet.index(c)
                result += self.new_alphabet[(idx + s) % 26]

            # Other characters which are not letters remain the same
            else:
                result += c

        return result

    def decrypt(self, message, s):
        """
            The function for decoding
                :param message: string
                    The message to be decoded
                :param s: integer
                    The shift
                :return: string
                    The decoded message
        """

        result = ""

        # traverse text
        for i in range(len(message)):
            c = message[i]

            # Decryption of upper characters
            if c.isupper():
                idx = self.upper_alphabet.index(c)
                result += self.upper_alphabet[(idx - s) % 26]

            # Decryption of lower characters
            elif c.islower():
                idx = self.new_alphabet.index(c)
                result += self.new_alphabet[(idx - s) % 26]

            # Other characters which are not letters remain the same
            else:
                result += c

        return result
