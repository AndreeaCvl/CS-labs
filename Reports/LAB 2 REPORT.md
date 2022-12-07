#  Symmetric Ciphers. Stream Ciphers. Block Ciphers.

### Course: Cryptography & Security
### Author: Andreea Covalevschi

----

## Theory
Symmetric Cryptography deals with the encryption of plain text when 
having only one encryption key which needs to remain private. 
Based on the way the plain text is processed/encrypted there 
are 2 types of ciphers:

Stream ciphers: <br>
- The encryption is done one byte at a time.
- Stream ciphers use confusion to hide the plain text.
- Make use of substitution techniques to modify the plain text.
- The implementation is fairly complex.
- The execution is fast.

Block ciphers:
- The encryption is done one block of plain text at a time.
- Block ciphers use confusion and diffusion to hide the plain text.
- Make use of transposition techniques to modify the plain text.
- The implementation is simpler relative to the stream ciphers.
- The execution is slow compared to the stream ciphers.

Some examples of stream ciphers are the following:
- Grain
- HC-256
- PANAMA
- Rabbit
- Rivest Cipher (RC4): It uses 64 or 128-bit long keys. It is used in TLS/SSL and IEEE 802.11 WLAN.
- Salsa20 
- Software-optimized Encryption Algorithm (SEAL)
- Scream 

The block ciphers may differ in the block size which is a 
parameter that might be implementation specific. Here are some 
examples of such ciphers:

- 3DES
- Advanced Encryption Standard (AES): A cipher with 128-bit block 
length which uses 128, 192 or 256-bit symmetric key.
- Blowfish
- Data Encryption Standard (DES): A 56-bit symmetric key cipher.
- Serpent
- Twofish: A standard that uses Feistel networks. It uses blocks 
of 128 bits with key sizes from 128-bit to 256-bit.

## Objectives:
- Get familiar with the symmetric cryptography, stream and block ciphers.
- Implement an example of a stream cipher.
- Implement an example of a block cipher.
- The implementation should, ideally follow the abstraction/contract/interface used in the previous laboratory work.
- Please use packages/directories to logically split the files that you will have.
- As in the previous task, please use a client class or test classes to showcase the execution of your programs


## Implementation description

## 1. Stream Cipher: [RC4 ](https://github.com/AndreeaCvl/CS-labs/blob/main/Lab-2/RC4.py)
### Encryption
RC4 is a stream cipher and variable-length key algorithm. This algorithm 
encrypts one byte at a time (or larger units at a time). A key input is 
pseudorandom bit generator that produces a stream 8-bit number that is 
unpredictable without knowledge of input key, The output of the generator 
is called key-stream, is combined one byte at a time with the plaintext 
stream cipher using X-OR operation.

To encrypt a message, the function ```encrypt``` receives the plain text and 
the key as input from the user and converts them to ascii. Then the key scheduling
algorithm is called which initializes a permutation in array```S``, which has
length = 256 and initially contains integers from 0 to 255 in ascending order.

```
    def key_scheduling(self, key):
        j = 0

        for i in range(256):
            j = (j + self.S[i] + key[i % len(key)]) % 256

            temp = self.S[j]
            self.S[j] = self.S[i]
            self.S[i] = temp
```

After performing the first step, vector S is initialized so there is no need to
use the initial key anymore. The second step is to generate a key stream (also 
called Stream Generation). Each S[i] is swapped with another byte in S according 
to a scheme dictated by the current configuration of S.

```
  def key_stream(self):
        i = 0
        j = 0
        while True:
            i = (1 + i) % 256
            j = (self.S[i] + j) % 256
            temp = self.S[j]
            self.S[j] = self.S[i]
            self.S[i] = temp

            # After reaching S[255] the process continues, starting from S[0] again
            yield self.S[(self.S[i] + self.S[j]) % 256]
```

To encrypt a message, each ascii value from the plain text array must be xored
with each next value produced by the function ```key_stream``` and the hex
value of the result is added to a string named result, which contains the 
encrypted result.

### Decryption
The function ```decrypt``` receives the encoded message and key from the user.
After it converts the encoded message from hex to decimal and the key to ascii,
the same algorithms for key scheduling and stream generation as for encryption are 
called. Then the message is decrypted using xor, just as in the previous example,
but this time using the encoded message.


## 1. Block Cipher: [DES ](https://github.com/AndreeaCvl/CS-labs/blob/main/Lab-2/DES.py)
### Encryption
The Data Encryption Standard (DES) is a symmetric-key block cipher published by 
the National Institute of Standards and Technology (NIST). It is based on the two fundamental attributes of cryptography: substitution 
and transposition. DES consists of 16 steps, each of which is called a round. 

The function ```encrypt``` receives the plain text (```PT```) and key from the user.
It then converts the PT to hex and splits it into chunks of 16 characters. Using the
binary representation of the key, the function ```key_processing``` is called
which makes permutation of the key according to the PC1 table and splits it in 
left and right parts C0 and D0. A left shift algorithm is performed on C0 and 0D and
this way we obtain arrays C and D each with 17 variants of the left and right key.
17 keys K are obtained by adding the halves together, then permutations are performed
on K according to the PC2 table. After all these steps, a new key ```KEY_PC2``` was obtained.

```
def key_processing(self, key_bin):

        # permutation of the key according to the PC1 table
        key_pc1 = self.permutations(key_bin, self.PC1)

        # init empty lists for storing the half-keys 1..16
        C = [None] * 17
        D = [None] * 17

        # splitting the key in left and right parts
        s = self.splitting(key_pc1, int(len(key_pc1) / 2))

        # stiring C0 and D0 inside lists
        C[0] = s[0]
        D[0] = s[1]

        # left shift
        C, D = self.left_shift(C, D)

        # 8. form the keys Kn (16 rounds)
        K_shift = [None] * 17
        for i in range(17):
            K_shift[i] = C[i] + D[i]

        # creating permutations of the key according to the PC2 table
        KEY_PC2 = [''] * 16
        for j in range(1, 17):
            KEY_PC2[j - 1] += self.permutations(K_shift[j], self.PC2)

        return KEY_PC2
```

Having the key, the program iterates trough every part of 16 characters in the 
PT and converts it to binary, performs an initial permutation on it, and splits 
it into L0 and R0 parts of equal size. Using KEY_PC2, L0 and R0 the function ```half_keys```
performs some permutations, xor and applies the S-boxes algorithm on given data.
This function generates values to store in the arrays L and R. 

```
def half_keys(self, KEY_PC2, L, R):
        for i in range(1, 17):
            L[i] = R[i - 1]

            # e-bit table permutations
            er = self.do_er(R[i - 1])

            # xor the er result with KEY_PC2
            XOR_1 = self.xor(er, KEY_PC2[i - 1], len(er))

            # splittion the above obtained result in 6 equal parts
            bbb = self.splitting(XOR_1, 6)

            # applying the s boxes
            n = 0
            new_seq = ''
            for seq in bbb:
                new_seq += self.s_box(seq, self.S[n])
                n += 1

            # permutations of the result obtained after S-bixes algorithm
            new_seq = self.permutations(new_seq, self.SBP)

            # Xor the values from L with new_seq
            XOR_2 = self.xor(L[i - 1], new_seq, len(L[i - 1]))

            # assigning a new value to R[i]
            R[i] = XOR_2

        return L, R
```
By adding the last values in L16 and R16 - K16 is created and a final 
permutation is performed it. K16 is converted to hex and appended to the string
ciphertext which in the end will contain the encoded message.

### Decryption
The proces of Decryption is the same as the process for Encryption, but instead of
using the normal key KEY_PC2 obtained after the key_processing function is called,
the algorithm uses it in reverse order. 
```KEY_PC2 = KEY_PC2[::-1]```

## Conclusions / Screenshots / Results
RC4 is a simple and fast cypher but at the same time not secure. The keystream 
generated by the RC4 is biased to varying degrees towards certain sequences which
makes it even more vulnerable. DES is more secure than RC4 and the most practical 
attack which can be used in order to break it is a brute-force attack. The biggest
downside of it is the relatively short 56-bit key size.
The objectives of this laboratory work were accomplished. Everything works as 
intended.