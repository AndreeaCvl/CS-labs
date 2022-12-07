#  Asymmetric Ciphers.

### Course: Cryptography & Security
### Author: Andreea Covalevschi

----

## Theory
Asymmetric Cryptography (a.k.a. Public-Key Cryptography)deals with the encryption of plain text when having 2 keys, one being public and the other one private. The keys form a pair and despite being different they are related.

As the name implies, the public key is available to the public but the private one is available only to the authenticated recipients.

A popular use case of the asymmetric encryption is in SSL/TLS certificates along side symmetric encryption mechanisms. It is necessary to use both types of encryption because asymmetric ciphers are computationally expensive, so these are usually used for the communication initiation and key exchange, or sometimes called handshake. The messages after that are encrypted with symmetric ciphers.



Examples: <br>
- RSA
- Diffie-Helman
- ECC
- El Gamal
- DSA

## Objectives:
- Get familiar with the asymmetric cryptography mechanisms.
- Implement an example of an asymmetric cipher.

## Implementation description

## RSA  
### Encryption
Fot starting the algorithm, the user must first choose the 
public key (consists of p, q and e). ```p``` and ```q``` 
must be primes, so the first thing which happens inside the encrypt
function s calling another function ```check_if_prime``` which
checks if the condition is met.
The function ```key_generation``` creates the private key d, and if
the operation was successful it returns the value True or False 
otherwise. This function first find the value of A, A = (q-1)*(p-1), 
then checks if e is in range (0, A) and if e and A are coprimes.
Only when both conditions are true, the algorithm proceeds to 
compute d as a multiplicative inverse of E mod A.

```
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
```
To encrypt a message, the plain test must be converted to ASCII.
Each of its elements is taken and raised at the power e. 
``pw = i ** self.e``. Then the result of ``pw % self.n`` is found 
and appended to the encoded string result.

### Decryption
To decrypt a message the same keys must be used, with the only difference
that instead of receiving the public key e as input from the user,
it must receive the private key d. Then the algorithm for obtaining
the decrypted message is the same as for encryption.

## Conclusions / Screenshots / Results
RSA is an algorithm which is used until today. One of its downsides
may be the fact that it is relatively slow, but at the same time it
is hard to break, especially when a large enough key is used.
Its security relies on the computational difficulty of 
factoring large integers.
The implementation of the algorithm works as intended and the
message can be both encrypted and decrypted (if the key is 
already known) correctly.