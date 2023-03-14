from passwords_generator_app.application_graphical_interface.gui_app_config import app
from passwords_generator_app.application_graphical_interface.toplevel_windows import (
    password_strength_screen,
    generator_history_screen
)


def shortcut_strength(event):
    current_lang = app.current_language
    password_strength_screen(current_lang)


def shortcut_history(event):
    current_lang = app.current_language
    generator_history_screen(current_lang)


def main():
    app.title('Password Generator')
    app.geometry('900x550')
    app.resizable(False, False)
    app.bind('<Control-s>', shortcut_strength)
    app.bind('<Control-S>', shortcut_strength)
    app.bind('<Control-h>', shortcut_history)
    app.bind('<Control-H>', shortcut_history)
    app.mainloop()


if __name__ == '__main__':
    main()
