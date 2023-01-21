from change_interface_look.center_app import center_window
from create_app.gui_app_config import app

def run_app():
    app.title('Password Generator')
    app.geometry('700x550')
    app.resizable(False, False)
    center_window(app)
    app.mainloop()
