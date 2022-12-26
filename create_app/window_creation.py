from create_app.pass_gen_app import app


def run_app():
    app.title('Password Generator')
    app.geometry('700x550')
    app.resizable(False, False)
    app.mainloop()
