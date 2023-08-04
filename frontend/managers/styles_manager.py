import gi; gi.require_version('Gtk', '3.0'); from gi.repository import Gtk, Gio

import os
from pathlib import Path
from utils.rm import rm

from definitions import STYLES_DIR


class StylesManager:
    def __init__(self):
        super(StylesManager, self).__init__()
        self.styles = []
        self.load_styles()

    def load_styles(self):
        self.styles = []
        for style in os.listdir(STYLES_DIR.as_posix()):
            if 'generated' in style: rm(Path(STYLES_DIR, style).as_posix()); continue
            provider = Gtk.CssProvider(); self.styles.append(provider)
            tmp_style = Path(STYLES_DIR, style + '_generated')
            with Path(STYLES_DIR, style).open('r') as f:
                result = f.read()
                for color, value in self.data.settings.colors.items(): result = result.replace(color, value)
                with tmp_style.open('w') as f: f.write(result)
            provider.load_from_path(tmp_style.as_posix()); rm(tmp_style)
