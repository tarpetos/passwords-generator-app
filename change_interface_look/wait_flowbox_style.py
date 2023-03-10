def round_rectangle(x1, y1, x2, y2, canvas, radius=25, **kwargs):
    points = [
        x1 + radius, y1,
        x1 + radius, y1,
        x2 - radius, y1,
        x2 - radius, y1,
        x2, y1,
        x2, y1 + radius,
        x2, y1 + radius,
        x2, y2 - radius,
        x2, y2 - radius,
        x2, y2,
        x2 - radius, y2,
        x2 - radius, y2,
        x1 + radius, y2,
        x1 + radius, y2,
        x1, y2,
        x1, y2 - radius,
        x1, y2 - radius,
        x1, y1 + radius,
        x1, y1 + radius,
        x1, y1
    ]

    return canvas.create_polygon(points, **kwargs, smooth=True, fill='black')


def load_screen_position_size(main_window, loading_screen):
    main_window_width = main_window.winfo_screenwidth()
    main_window_height = main_window.winfo_screenheight()
    x = main_window_width // 2 - 185
    y = main_window_height // 2 - 50
    loading_screen.geometry('+{}+{}'.format(x, y))
