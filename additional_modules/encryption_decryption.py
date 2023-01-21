import base64

def encrypt(data) -> str:
    if data is not None:
        encode = base64.b85encode(data.encode('UTF-16'))
        sub_start_symbols = (encode.decode()).split('|N', 1)[1] # -> into database
        return sub_start_symbols

def decrypt(data) -> str:
    add_start_symbols = '|N' + data
    decode = base64.b85decode(add_start_symbols).decode('UTF-16') # -> from database
    return decode

# def encrypt(data):
#     if data is not None:
#         return base64.b85encode(data.encode('UTF-16')).decode()
#
#
# def decrypt(data):
#     return base64.b85decode(data).decode('UTF-16')
