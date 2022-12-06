#  Intro to Cryptography. Classical ciphers. Caesar cipher.

### Course: Cryptography & Security
### Author: Andreea Covalevschi

----

## Theory
 Cryptography consists a part of the science known as Cryptology. The other part is Cryptanalysis. There are a lot of different algorithms/mechanisms used in Cryptography.
 Some of them, which are implemented in this laboratory work are:
- Caesar cipher with one key used for substitution (as explained above);
- Caesar cipher with one key used for substitution, and a permutation of the alphabet;
- Vigenere cipher;
- Playfair cipher.
These are classical ciphers. In contrast to modern cryptographic algorithms, most classical ciphers can be practically computed and solved by hand. However, they are also usually very simple to break with modern technology.


## Objectives:

* Get familiar with the basics of cryptography and classical ciphers.
* Implement 4 types of the classical ciphers:

- Caesar cipher with one key used for substitution (as explained above),
- Caesar cipher with one key used for substitution, and a permutation of the alphabet,
- Vigenere cipher,
- Playfair cipher.


## Implementation description
This laboratory contains the implementation of 4 different algorithms, separated in different folders:
- [Caesar cipher with one key used for substitution (as explained above)](https://github.com/AndreeaCvl/CS-labs/tree/main/Lab%201/Caesar)
- [Caesar cipher with one key used for substitution, and a permutation of the alphabet](https://github.com/AndreeaCvl/CS-labs/tree/main/Lab%201/Caesar%20with%20Permutation)
- [Vigenere cipher](https://github.com/AndreeaCvl/CS-labs/tree/main/Lab%201/Vigenere)
- [Playfair cipher](https://github.com/AndreeaCvl/CS-labs/tree/main/Lab%201/Playfair)

Each folders contains 2 .py files - the class which contains the logic of the algorithm, and ```main.py``` used for testing the algorithm.

#### 1. Caesar cipher with one key used for substitution
The function **encrypt** is used for encrypting the message. Takes the message and the shift as arguments and replaces the characters in the original message with characters located at distance s (to the right) from them.
```
 def encrypt(self, message, s):
        result = ""
 
        # traverse text
        for i in range(len(message)):
            c = message[i]

            # Encryption of uppercase characters
            if (c.isupper()):
                result += chr((ord(c) + s - ord('A')) % 26 + ord('A'))

            # Encryption of lowercase characters
            elif (c.islower()):
                result += chr((ord(c) + s - ord('a')) % 26 + ord('a'))
            
            # Other characters which are not letters remain the same 
            else:
                result += c
                
        return result
```
The function **decrypt** is used for decrypting the message. Takes the encoded message and the shift as arguments and replaces the characters in the encoded message with characters located at distance s (to the left) from them.

#### 2. Caesar cipher with one key used for substitution
It has an additional function which is not in simple Caesar - **alpha_permutation** which shuffles the alphabet. The encrypt and decrypt functions work in the same way as specified above for the simple Caesar.

```
  def alpha_permutation(self):
        # creates a permutation of the alphabet
        
        # initial alphaet order
        alphabet = 'abcdefghijklmnopqrstuvwxyz'
        
        self.new_alphabet = ''
        
        # shuffles the initial alphabet
        self.new_alphabet = ''.join(random.sample(alphabet,len(alphabet)))
        
        # creates an alphabet with uppercase letters only
        self.upper_alphabet = self.new_alphabet.upper()
```

#### 3. Vigenere cipher
Has an **encrypt** function used for encrypting messages. It has a call to **new_key** function, which creates a key of the same length as the message to be encoded by repeating (or omiting) characters from the original key. Then the encrypt function encrypts the message using the Vigenere matrix which is built when initializing the class. **decrypt** does the opposite. Also has a call to **new_key**, and then it looks for the encoded character in the matrix and then finds its original value.

```
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
            return "" . join(key)  
```

#### 4. Playfair cipher
**encrypt** and **decrypt** functions work in very similar ways. First, there is a call to **build_matrix** function, which creates the playfair matrix according to the given key. Then, digraphs is called for creating pairs of characters. It adds a 'X' in pairs where the characters are the same, and if the last character doesn't have a pair, it adds 'Z' in the end of the string.
**row_rule**, **row_rule** and **rectangle_rule** encode the message according to the rules of Playfair cipher. **row_rule_dec** and **col_rule_dec** decode the message by doing the opposite action of the original functions. (if in the row_rule and col_rule we look for characters in the last row/column as an edge case, in **row_rule_dec** and **col_rule_dec** we look at the characters located in the first row/col). **rectangle_rule** function can be used both for encryption and decryption, as it works in the same way.

```
def encrypt(self, message, key):
        # buiding the playfair matrix
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
```

## Conclusions / Screenshots / Results
During this laboratory work I learned some new encryption algorithms and refreshed my knowledge of some I already know about. These algorithms of encryption belong to classical ciphers. Although it was fun to implement them, it can be concluded that these algorithms are not reliable and can be broken by whoever manages to find the key or even simplier in case of Caesar - the shift.
