class RSA:
    def __init__(self, message, key, d=None, e=None):
        self.message = message
        self.key = key
        self.d = d  # private key
        self.e = e  # public key
        self.n = None  # public key

    # function to check if a number is prime
    # used to verify if the key chosen by the user is suitable for the algorithm
    def check_if_prime(self):
        for i in self.key:
            for j in range(2, self.key[i] // 2):
                if (self.key[i] % j) == 0:
                    print(f"{i} = {self.key[i]}. It is not a prime number.")
                    return False
        return True

    # converting message to ascii
    def str_to_int(self):
        lst = list()

        for i in self.message:
            lst.append(ord(i))

        return lst

    # fing the greatest common divisor
    def gcd(self, p, q):
        while q != 0:
            p, q = q, p % q
        return p

    # detect if 2 numbers are coprime
    def is_coprime(self, x, y):
        return self.gcd(x, y) == 1

    # generating the key
    def key_generation(self):

        # find the public key n
        self.n = self.key["q"] * self.key["p"]

        # find A
        A = (self.key["q"] - 1) * (self.key["p"] - 1)

        # check if e is working with the other keys
        if self.e > A:
            print(f"Error. E = {self.e} is bigger than A = {A}.")
            return False

        if not self.is_coprime(A, self.e):
            print(f"Error. E = {self.e} and A = {A} are not coprimes")
            return False

        # multiplicative inverse of E mod A
        self.d = pow(self.e, -1, A)

        return True

    def encrypt(self):

        # check if p and q are primes
        if not self.check_if_prime():
            return

        # convert message to int
        new_message = self.str_to_int()

        # if key is not good
        if not self.key_generation():
            return "Error."

        # init a list to store encrypted symbols
        encrypted = list()

        # encrypt the message
        for i in new_message:
            pw = i ** self.e
            rem = pw % self.n
            encrypted.append(rem)

        return encrypted

    def decrypt(self):

        # create public key n
        self.n = self.key["q"] * self.key["p"]

        decoded = ''

        # decode the message
        for i in self.message:
            pw = i ** self.d
            rem = pw % self.n
            decoded += chr(rem)

        return decoded
