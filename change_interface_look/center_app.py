def center_window(window):
    window.update_idletasks()

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width - window.winfo_width()) // 2
    y = (screen_height - window.winfo_height()) // 2

    window.wm_geometry(f'+{x}+{y}')
