from DB import DB
from Auth import Auth
from DigitalSignature import DigitalSignature
from RSA import RSA

if __name__ == '__main__':
    # connecting to database
    db = DB()
    db.connect()

    # initializing the authentication process
    auth = Auth(db)
    auth.start_auth()

    # fetching the database to make sure a new record was added
    db.fetch_database()

    # verifying a digital signature
    ds = DigitalSignature()
    ds.digest_message()

    # encoding the message
    key = {"q": 239, "p": 151}
    e = 277

    c = RSA(ds.digest, key, e=e)
    enc = c.encrypt()

    c2 = RSA(enc, key, d=c.d)
    dec = c2.decrypt()

    # verifying the signature
    ds.verify_signature(dec)





