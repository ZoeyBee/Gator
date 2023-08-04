import gi; gi.require_version('Gtk', '3.0'); from gi.repository import Gtk, Gio


class KeyboardManager:
    def __init__(self):
        super(KeyboardManager, self).__init__()
        self.pressing_shift = False
        self.pressing_ctrl = False

    def setup_window_connections(self):
        self.window.connect('key-press-event', self.on_key_press)
        self.window.connect('key-release-event', self.on_key_release)

    def on_key_press(self, window, event):
        # print(event.keyval)
        if event.keyval == 65505:
            self.pressing_shift = True

    def on_key_release(self, window, event):
        if event.keyval == 65505:
            self.pressing_shift = False
