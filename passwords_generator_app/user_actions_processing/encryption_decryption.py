import os
import sys

import cryptography.fernet
from cryptography.fernet import Fernet
import base64

from ..database_connections.local_db_connector import ROOT_PATH

KEY_FILE = os.path.expanduser(f'{ROOT_PATH}.password_generator_key')


def generate_key(comment: str = None):
    key = Fernet.generate_key()
    with open(KEY_FILE, 'wb') as key_file:
        if comment is not None:
            key_file.write(f'# {comment}\n'.encode())
        key_file.write(key)


def load_key() -> bytes:
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, 'rb') as key_file:
            key_lines = [line for line in key_file.readlines() if not line.startswith(b'#')]
            key_data = b''.join(key_lines)
            return key_data
    else:
        generate_key(
            'This is your unique encryption and decryption key created by the '
            'Password Generator application. DO NOT delete or change it.\n'
            '# If you want to move data.db, then also move this file along with data.db.'
        )
        return load_key()


def revoke_key():
    if os.path.exists(KEY_FILE):
        os.remove(KEY_FILE)


def encrypt(data: str, new_key: bytes = None) -> str | None:
    try:
        if data is not None:
            encryption_object = Fernet(load_key() if new_key is None else new_key)
            encrypted = encryption_object.encrypt(data.encode())
            return base64.urlsafe_b64encode(encrypted).decode()
    except ValueError:
        sys.exit('Encryption error!!!')


def decrypt(data: str, new_key: bytes = None) -> str | None:
    try:
        decryption_object = Fernet(load_key() if new_key is None else new_key)
        decrypted = decryption_object.decrypt(base64.urlsafe_b64decode(data)).decode()
        return decrypted
    except cryptography.fernet.InvalidToken:
        sys.exit('You are using invalid token!!!')
    except ValueError:
        sys.exit('Decryption error!!!')
