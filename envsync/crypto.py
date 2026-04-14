from cryptography.fernet import Fernet, InvalidToken

def generate_key() -> str:
    return Fernet.generate_key().decode()

def encrypt_file(file_path: str, key: str) -> str:
    f = Fernet(key.encode())
    with open(file_path, "rb") as file:
        data = file.read()
    return f.encrypt(data).decode()

def decrypt_data(encrypted_string: str, key: str) -> str:
    f = Fernet(key.encode())
    try:
        return f.decrypt(encrypted_string.encode()).decode()
    except InvalidToken:
        raise Exception("Wrong key — could not decrypt.")
    


