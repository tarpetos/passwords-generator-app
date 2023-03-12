from passwords_generator_app.create_app.gui_app_config import app
from passwords_generator_app.create_app.inputs_and_buttons_processing import password_strength_checker


def shortcut_strength(event):
    current_lang = app.current_language
    password_strength_checker(event, current_lang)


def main():
    app.title('Password Generator')
    app.geometry('900x550')
    app.resizable(False, False)
    app.bind('<Control-s>', shortcut_strength)
    app.bind('<Control-S>', shortcut_strength)
    app.mainloop()


if __name__ == '__main__':
    main()
