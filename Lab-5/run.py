from ClassicalCiphers.CaesarSubst import CaesarSubst
from ClassicalCiphers.CaesarWihPermutation import CaesarWithPermutation
from ClassicalCiphers.Playfair import Playfair
from ClassicalCiphers.Vigenere import Vigenere
from flask import Flask, make_response, jsonify, request
from DB import DB
from Auth import Auth
import pyotp
import uuid
import base64
import qrcode

app = Flask(__name__)
global db

users_dict = dict()
key = dict()
admin_password = "somehexpassword"


@app.route('/api/register', methods=['POST'])
def register():
    try:
        user_data = request.get_json()
        reg = Auth(db)
        reg.register(user_data['username'], user_data['password'], "simple")
        print(db.fetch_database())

        username = user_data['username']

        key[username] = username + "SecretKey"
        k = base64.b32encode(bytearray(key[username], 'ascii')).decode('utf-8')

        uri = pyotp.totp.TOTP(k).provisioning_uri(name=username, issuer_name="CS-lab-5")
        print(uri)

        qrcode.make(uri).save("totp.png")

        return "New record created. Please scan the QR code for 2FA"
    except:
        return "Username already taken"


@app.route('/api/register/admin', methods=['POST'])
def admin_register():
    user_data = request.get_json()
    if user_data['password'] != admin_password:
        return "Wong admin password"
    else:
        reg = Auth(db)
        reg.register(user_data['username'], user_data['password'], "admin")

        username = user_data['username']

        key[username] = username + "SecretKey"
        k = base64.b32encode(bytearray(key[username], 'ascii')).decode('utf-8')

        uri = pyotp.totp.TOTP(k).provisioning_uri(name=username, issuer_name="CS-lab-5")
        print(uri)

        qrcode.make(uri).save("totp.png")

        return "Admin created. Please scan the QR code for 2FA"


@app.route('/api/login', methods=['POST'])
def login():

    user_data = request.get_json()
    password = user_data['password']
    username = user_data['username']

    log = Auth(db)
    result = log.login(username, password)

    if result:
        k = base64.b32encode(bytearray(key[user_data['username']], 'ascii')).decode('utf-8')
        totp = pyotp.TOTP(k)
        print(totp.now())

        if totp.now() == user_data['login_token']:
            session_id = uuid.uuid1()
            users_dict[user_data['username']] = str(session_id)
            return "Your unique session ID is: " + str(session_id) + " Use it for your next requests"
        else:
            return "Incorrect token"
    else:
        return "Incorrect data! Try again."


@app.route('/api/CaesarSubstitution', methods=['POST'])
def caesarSubstitution():
    data = request.get_json()
    message = data['message']
    shift = data['shift']
    action = data['action']

    if users_dict[data['username']] == data['session_id']:
        user = db.search_by_username(data['username'])
        if user["user_type"] == "simple" or user["user_type"] == "admin":
            c = CaesarSubst()
            if action == "encrypt":
                e = c.encrypt(message, int(shift))
            elif action == "decrypt":
                e = c.decrypt(message, int(shift))
            return e
        else:
            return "Unauthorized"
    else:
        return "Expired session ID"


@app.route('/api/CaesarPermutation', methods=['POST'])
def caesarPermutation():
    data = request.get_json()
    message = data['message']
    shift = data['shift']
    action = data['action']

    if users_dict[data['username']] == data['session_id']:
        user = db.search_by_username(data['username'])
        if user["user_type"] == "simple" or user["user_type"] == "admin":
            c = CaesarWithPermutation()
            if action == "encrypt":
                c.alpha_permutation()
                e = c.encrypt(message, int(shift))
                print(c.new_alphabet)
                return e
            elif action == "decrypt":
                c.alpha_permutation()
                c.new_alphabet = data['alphabet']
                e = c.decrypt(message, int(shift))
                return e
        else:
            return "Unauthorized"
    else:
        return "Expired session ID"


@app.route('/api/playfair', methods=['POST'])
def playfair():
    data = request.get_json()
    message = data['message']
    cipher_key = data['key']
    action = data['action']

    if users_dict[data['username']] == data['session_id']:
        user = db.search_by_username(data['username'])
        if user["user_type"] == "simple" or user["user_type"] == "admin":
            c = Playfair()
            if action == "encrypt":
                e = c.encrypt(message, cipher_key)
            elif action == "decrypt":
                e = c.decrypt(message, cipher_key)
            return e
        else:
            return "Unauthorized"
    else:
        return "Expired session ID"


@app.route('/api/vigenere', methods=['POST'])
def vigenere():
    data = request.get_json()
    message = data['message']
    cipher_key = data['key']
    action = data['action']

    if users_dict[data['username']] == data['session_id']:
        user = db.search_by_username(data['username'])
        if user["user_type"] == "simple" or user["user_type"] == "admin":
            c = Vigenere()
            if action == "encrypt":
                e = c.encrypt(message, cipher_key)
            elif action == "decrypt":
                e = c.decrypt(message, cipher_key)
            return e
        else:
            return "Unauthorized"
    else:
        return "Expired session ID"


if __name__ == '__main__':
    db = DB()
    db.connect()

    app.run()