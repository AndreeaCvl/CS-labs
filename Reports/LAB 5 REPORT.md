#  Web Authentication & Authorisation.

### Course: Cryptography & Security
### Author: Andreea Covalevschi

----

## Theory
Authentication & authorization are 2 of the main security goals of IT systems and should not be used interchangibly. Simply put, during authentication the system verifies the identity of a user or service, and during authorization the system checks the access rights, optionally based on a given user role.

There are multiple types of authentication based on the implementation mechanism or the data provided by the user. Some usual ones would be the following:

- Based on credentials (Username/Password);
- Multi-Factor Authentication (2FA, MFA);
- Based on digital certificates;
- Based on biometrics;
- Based on tokens.

Regarding authorization, the most popular mechanisms are the following:

- Role Based Access Control (RBAC): Base on the role of a user;
- Attribute Based Access Control (ABAC): Based on a characteristic/attribute of a user.


## Objectives:
1. Take what you have at the moment from previous laboratory works and put it in a web service / serveral web services.
2. Your services should have implemented basic authentication and MFA (the authentication factors of your choice).
3. Your web app needs to simulate user authorization and the way you authorise user is also a choice that needs to be done by you.
4. As services that your application could provide, you could use the classical ciphers. Basically the user would like to get access and use the classical ciphers, but they need to authenticate and be authorized.

## Implementation description
In order to use the app, the user must be authenticated either as an admin or as a simple
user. To create an account as a simple user, a POST request should be sent 
at the server (endpoint api/register) containing an username and a password. The hash
of the password is stored inside the database, along with the user role which is "simple".
To create an admin account, a request containing the same data should be sent to the
endpoint /api/register/admin, but if the password won't match the already defined
password for admins, the account won't be created. After the registration process, a
qr code will be generated. After scanning it, the user will see his token (used
for 2 factor authentication), and a new code will be generated evry 30 seconds.
```
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
```

When logging in, the user should provide his username, password and his token.
If everything is right, then a unique session ID is generated and returned. The
user will use this session ID along with his identifier (username) to make further
requests.

For encoding or decoding messages using the app, the user should be logged in either
as a simple user or as an admin. Data for encryption/decryption should be provided
in orger to receive a coherent response. The result will be returned only if the
session ID is correct and the user is authorized. You cand see below the function for
encoding a message with playfair cipher.

```
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
```

And an example of the body for encrypting a message:
```
{
    "username": "Andrex3a",
    "session_id": "85c374b1-7ccb-11ed-bd09-58fb845c3b49",
    "message": "THISISATEST",
    "key": "TRAP",
    "action": "encrypt"
}
```

## Conclusions
For making a secure app many details should be taken into account, such as: hashing
the password, not allowing unauthorized or unauthenticated users, making sure no one
as access to personal information of another user. 2-Factor-Authentication is
an additional layer of security and neutralizes the risks associated with 
compromised passwords. Authorization grants access to specific resources based on 
an authenticated user's entitlements. In this laboratory work I got to know the basics
of these concepts and everything works as intended.
