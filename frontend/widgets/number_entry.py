import gi; gi.require_version('Gtk', '3.0'); from gi.repository import Gtk

from utils.min_max import min_max


class NumberEntry(Gtk.Entry):
    def __init__(self, container=None, default=100, minimum=0, maximum=100, on_change=None):
        super(NumberEntry, self).__init__()
        if container is not None: container.pack_start(self, True, True, 0)
        self.real_value = ''
        self.minimum = minimum
        self.maximum = maximum
        self.default = default
        self.on_change = on_change
        self.set_text(str(default))
        self.ignore_signals = False
        self.connect('changed', self.on_insert)

    def on_insert(self, event):
        if self.ignore_signals: return
        if not self.get_text():
            self.real_value = ''; return
        elif self.get_text().isdigit():
            value = min_max(int(self.get_text()), self.minimum, self.maximum)
            self.on_change(value)
            self.real_value = str(value)
        self.set_text(self.real_value)

    def set_value(self, value):
        self.real_value = str(value)
        self.ignore_signals = True
        self.set_text(str(value))
        self.ignore_signals = False
