import numpy as np


class Playfair:

    def __init__(self):
        """
            The constructor of the class
        """
        self.matrix = None

    def build_matrix(self, key):

        """
            Constructs the Playfair matrix
                :param key: string
                    The key of the cipher
        """

        # empty list for keeping the letters in order as they are added in the matrix
        letters = []

        # adding unique letters from the key to the list of letters
        for i in range(len(key)):
            if key[i] not in letters:
                letters.append(key[i])

        # initializing i with the index of the first letter of alphabet in unicode
        i = ord('A')

        # building a list with all letters (except J), arranged in order of their appearance
        while len(letters) < 25:
            if chr(i) not in letters:
                if chr(i) != 'J':
                    letters.append(chr(i))
            i += 1

        # defining a new shape for the list
        shape = (5, 5)

        # reshaping the list of letters into a 5x5 matrix
        x = np.array(letters)
        self.matrix = x.reshape(shape)

    def digraphs(self, message):
        """
            Identifies pairs of characters
                :param message: string
                    The message to be encoded
        """

        # empty list for storing the digraphs
        digraphs = []

        # iterating through the letters of the message and creating pairs
        while len(message) > 1:

            if message[0] != message[1]:

                # pairing different letters
                s = message[0] + message[1]
                message = message[2:]
            else:

                # Adding bogus letters where needed
                s = message[0] + 'X'
                message = message[1:]

            # appending the resulted pair to the list
            digraphs.append(s)

        # in case a character remains unpaired, add Z at the end
        if len(message) == 1:
            s = message + 'Z'
            digraphs.append(s)

        return digraphs

    def row_rule(self, r0, c0, r1, c1):
        """
            Encode message according to row rule
                :param r0: int
                    row of the first character in pair
                :param  c0: int
                    column of the first character in pair
                :param r1: int
                    row of the second character in pair
                :param c1: int
                    column of the first character in pair
                :return: string
                    a pair of encoded characters
        """

        # if first character in the last column
        if c0 == 4:
            p0 = self.matrix[r0][0]
        else:
            p0 = self.matrix[r0][c0 + 1]

        # if second character in the last column
        if c1 == 4:
            p1 = self.matrix[r1][0]
        else:
            p1 = self.matrix[r1][c1 + 1]

        return p0 + p1

    def col_rule(self, r0, c0, r1, c1):
        """
            Encode message according to column rule
        """
        if r0 == 4:
            p0 = self.matrix[0][c0]
        else:
            p0 = self.matrix[r0 + 1][c0]

        if r1 == 4:
            p1 = self.matrix[0][c1]
        else:
            p1 = self.matrix[r1 + 1][c1]

        return p0 + p1

    def rectangle_rule(self, r0, c0, r1, c1):
        """
            Encode / decode message according to rectangle rule
        """
        p0 = self.matrix[r0][c1]
        p1 = self.matrix[r1][c0]

        return p0 + p1

    def row_rule_dec(self, r0, c0, r1, c1):
        """
            decode message according to row rule
        """
        if c0 == 0:
            p0 = self.matrix[r0][4]
        else:
            p0 = self.matrix[r0][c0 - 1]

        if c1 == 0:
            p1 = self.matrix[r1][4]
        else:
            p1 = self.matrix[r1][c1 - 1]

        return p0 + p1

    def col_rule_dec(self, r0, c0, r1, c1):
        """
            Decode message according to column rule
        """
        if r0 == 0:
            p0 = self.matrix[4][c0]
        else:
            p0 = self.matrix[r0 - 1][c0]

        if r1 == 0:
            p1 = self.matrix[4][c1]
        else:
            p1 = self.matrix[r1 - 1][c1]

        return p0 + p1

    def encrypt(self, message, key):
        """
            Encrypts the given message with a specified key
                :param message: string
                    the message to be encoded
                :param key: string
                    the key of the cipher
                :return: string
                    the encoded message
        """

        # building the playfair matrix
        self.build_matrix(key)

        # creating a set of digraphs
        digraphs = self.digraphs(message)

        encoded = ''

        # getting the indices of each pair and finding the rule to follow
        for element in digraphs:

            # indices of the first character in pair
            ind0 = np.where(self.matrix == element[0])
            row0 = ind0[0][0]
            col0 = ind0[1][0]

            # indices of the second character in pair
            ind1 = np.where(self.matrix == element[1])
            row1 = ind1[0][0]
            col1 = ind1[1][0]

            # calling the function with respect to the rule
            if row0 == row1:
                encoded += self.row_rule(row0, col0, row1, col1)
            elif col0 == col1:
                encoded += self.col_rule(row0, col0, row1, col1)
            else:
                encoded += self.rectangle_rule(row0, col0, row1, col1)

        return encoded

    def decrypt(self, enc_message, key):
        """
            Decrypts the given message with a specified key
                :param enc_message: string
                    the message to be decoded
                :param key: string
                    the key of the cipher
                :return: string
                    the decoded message
        """

        # building the playfair matrix
        self.build_matrix(key)

        # creating the set of digraphs
        digraphs = self.digraphs(enc_message)

        decoded = ''

        # getting the indices of each pair and finding the rule to follow
        for element in digraphs:

            # indices of the first character in pair
            ind0 = np.where(self.matrix == element[0])
            row0 = ind0[0][0]
            col0 = ind0[1][0]

            # indices of the second character in pair
            ind1 = np.where(self.matrix == element[1])
            row1 = ind1[0][0]
            col1 = ind1[1][0]

            # calling the function with respect to the rule
            if row0 == row1:
                decoded += self.row_rule_dec(row0, col0, row1, col1)
            elif col0 == col1:
                decoded += self.col_rule_dec(row0, col0, row1, col1)
            else:
                decoded += self.rectangle_rule(row0, col0, row1, col1)

        return decoded
