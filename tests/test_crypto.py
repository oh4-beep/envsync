from envsync.crypto import *



key = generate_key()

r = encrypt_file("tests/.env", key)

x = decrypt_data(r, key)
print(x)