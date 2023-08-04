import gi; gi.require_version('Gtk', '3.0'); from gi.repository import Gtk, GdkPixbuf

import os
from pathlib import Path

from definitions import GRAPHICS_DIR


class GraphicsManager:
    def __init__(self):
        self.icon_paths = {}
        self.icons = {}
        self.load_icons()
        super(GraphicsManager, self).__init__()

    def load_icons(self):
        for icon_path in os.listdir(GRAPHICS_DIR.as_posix()):
            icon_path = Path(GRAPHICS_DIR, icon_path)
            self.icon_paths[icon_path.name.split('.')[0]] = icon_path

    def icon(self, icon, width=10, height=10):
        path = self.icon_paths[icon]
        if path.suffix == '.svg':
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(path.as_posix(), width, height, False)
            return Gtk.Image.new_from_pixbuf(pixbuf)
        return Gtk.Image.new_from_file(path.as_posix())
