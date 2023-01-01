import base64


def encrypt(data):
    return base64.b85encode(data.encode('UTF-16')).decode()


def decrypt(data):
    return base64.b85decode(data).decode('UTF-16')
