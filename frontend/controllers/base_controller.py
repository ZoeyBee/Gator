import gi; gi.require_version('Gtk', '3.0'); from gi.repository import Gtk


class BaseController(Gtk.Box):
    def __init__(self, parent, manager):
        super(BaseController, self).__init__(orientation='vertical', spacing=0)
        self.manager = manager
        self.data = manager.data
        self.parent = parent
        self.setup_ui()
        for signal in self.data.signals.list_of_signals:
            if hasattr(self, f'on_{signal}'): self.data.signals.add_listener(signal, eval(f'self.on_{signal}'))
        self.connect_signals()

    def setup_ui(self): pass

    def connect_signals(self): pass
