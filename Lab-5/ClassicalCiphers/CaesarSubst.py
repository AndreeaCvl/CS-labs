class CaesarSubst:
    # a Caesar class which will contain the encryption function for Caesar cipher with one key used for substitution

    def __init__(self):
        """
            The constructor of the class
        """

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
                result += chr((ord(c) + s - ord('A')) % 26 + ord('A'))

            # Encryption of lowercase characters
            elif c.islower():
                result += chr((ord(c) + s - ord('a')) % 26 + ord('a'))

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
                result += chr((ord(c) - ord("A") - s) % 26 + ord('A'))

            # Decryption of lower characters
            elif c.islower():
                result += chr((ord(c) - ord("a") - s) % 26 + ord('a'))

            # Other characters which are not letters remain the same
            else:
                result += c

        return result
