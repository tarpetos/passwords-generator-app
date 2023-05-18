from passwords_generator_app.application_graphical_interface.main_app_gui import PasswordGeneratorApp
from passwords_generator_app.application_graphical_interface.toplevel_windows_gui import (
    password_strength_screen,
    generator_history_screen
)

app = PasswordGeneratorApp()


def shortcut_strength(event):
    current_lang = app.current_language
    password_strength_screen(current_lang)


def shortcut_history(event):
    current_lang = app.current_language
    generator_history_screen(current_lang)


def main():
    app.title('Password Generator')
    app.geometry('900x550')
    app.minsize(900, 550)
    app.bind('<Control-s>', shortcut_strength)
    app.bind('<Control-S>', shortcut_strength)
    app.bind('<Control-h>', shortcut_history)
    app.bind('<Control-H>', shortcut_history)
    app.mainloop()


if __name__ == '__main__':
    main()
