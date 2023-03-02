from create_app.gui_app_config import app


def main():
    app.title('Password Generator')
    app.geometry('900x550')
    app.resizable(False, False)
    app.mainloop()


if __name__ == '__main__':
    main()
