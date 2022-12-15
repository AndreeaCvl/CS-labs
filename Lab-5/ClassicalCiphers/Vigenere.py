class Vigenere:

    def __init__(self):
        """
            The constructor of the class
        """
        # initializing the Vigenere matrix
        self.matrix = [[chr(ord('A') + (i + j) % 26) for i in range(26)] for j in range(26)]

    def new_key(self, message, key):
        """
            The function for creating a key of the same length as the message
                :param message: string
                    The message to be encoded or decoded
                :param key: string
                    The used key
                :return: string
                    The key which would be used further
        """

        # converting the string key to a list for convenience
        key = list(key)

        # repeating the key if needed
        if len(message) == len(key):
            return key
        else:
            for i in range(len(message) - len(key)):
                key.append(key[i % len(key)])
            return "".join(key)

    def encrypt(self, message, key):
        """
            The function for encrypting the message
                :param message: string
                    The message to be encoded
                :param key: string
                    The used key
                :return: string
                    The encoded message
        """

        # obtaining a key of the same length as the message
        key = self.new_key(message, key)

        result = ''

        # mapping chars form the message string with chars from the key using the Vigenere matrix
        for k in range(len(message)):
            row = ord(message[k]) - ord('A')
            col = ord(key[k]) - ord('A')

            result += self.matrix[row][col]

        return result

    def decrypt(self, message, key):
        """
            The function for decrypting the message
                :param message: string
                    The message to be decoded
                :param key: string
                    The used key
                :return: string
                    The decoded message
        """

        # obtaining a key of the same length as the message
        key = self.new_key(message, key)

        result = ''

        # mapping chars form the message string with chars from the key using the Vigenere matrix
        for k in range(len(message)):

            row = ord(key[k]) - ord('A')

            # finding the column in the needed row where the k-th letter from the encoded message is located
            for i in range(len(self.matrix)):
                if self.matrix[row][i] == message[k]:
                    col = i

            result += self.matrix[col][0]

        return result
    