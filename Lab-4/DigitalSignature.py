import hashlib


class DigitalSignature:
    def __init__(self):
        self.message = None
        self.digest = None

    def digest_message(self):
        # self.message = input('What is your message?\n')
        self.message = 'mai am de facut inca un laborator'

        self.digest = hashlib.sha256(self.message.encode('UTF-8')).hexdigest()
        return self.digest

    def verify_signature(self, dec):
        if self.digest == dec:
            print("Digital signature success!")
            return True
        return False