from create_app.gui_app_config import app


def run_app():
    app.title('Password Generator')
    app.geometry('700x550')
    app.resizable(False, False)
    app.mainloop()
