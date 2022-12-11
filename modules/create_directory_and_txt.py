import os


def create_directory():
    if not os.path.exists('passwords'):
        os.mkdir('passwords')


def create_txt():
    with open('readme.txt', 'w') as db_manual_txt:
        db_manual_txt.write(
            """
                Here you need to add a description of the program.
            """
        )
