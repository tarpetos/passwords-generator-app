from create_app.gui_app_config import app


def run_app():
    app.title('Password Generator')
    app.geometry('900x550')
    app.resizable(False, False)
    app.bind_all('<Control-f>', app.shortcut_search)
    app.bind_all('<Control-F>', app.shortcut_search)
    app.mainloop()
