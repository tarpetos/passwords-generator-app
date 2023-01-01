import json
import os

from additional_modules.encryption_decryption import decrypt


NUMBER_OF_JSON_IDENTS = 10


def create_directory():
    if not os.path.exists('passwords'):
        os.mkdir('passwords')


# def create_json(table_rows, file_name):
#     data = [
#         {
#             'id': password_data[0],
#             'password_usage': password_data[1],
#             'password': decrypt(password_data[2]),
#             'password_length': password_data[3],
#             'password_has_repeatable': password_data[4],
#         }
#         for password_data in table_rows
#     ]
#
#     directory = 'passwords'
#     file_path = os.path.join(directory, f'{file_name}.json')
#
#     create_directory()
#
#     with open(file_path, 'w+') as outfile:
#         json.dump(data, outfile, indent=NUMBER_OF_JSON_IDENTS)


def create_txt():
    with open('readme.txt', 'w') as db_manual_txt:
        db_manual_txt.write(
            '''
                Here you need to add a description of the program.
            '''
        )
