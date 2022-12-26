def check_if_description_existing(store_of_user_passwords, password_description):
    list_of_descriptions = store_of_user_passwords.select_descriptions()

    if password_description in list_of_descriptions:
        return True
    else:
        return False
