def hex_to_rgb(color):
    return tuple(int(color[1:][i:i+2], 16) / 255 for i in (0, 2, 4))
