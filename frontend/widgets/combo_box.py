import gi; gi.require_version('Gtk', '3.0'); from gi.repository import Gtk


class ComboBox(Gtk.Box):
    def __init__(self, container, entries, on_change, scrolling=False):
        super(ComboBox, self).__init__()
        if container is not None: container.pack_start(self, True, True, 0)
        if not hasattr(self, 'entries'): self.entries = entries
        self.entries_by_content = {}
        store = Gtk.ListStore(str, int)
        if isinstance(entries, dict):
            for uid, obj in entries.items():
                store.append([obj, uid])
                self.entries_by_content[obj] = uid
        if isinstance(entries, list):
            self.entries = {}
            uid = 0
            for string in entries:
                self.entries[uid] = string
                self.entries_by_content[string] = uid
                store.append([string, uid])
                uid += 1
        self.combo_box = Gtk.ComboBox.new_with_model(store)
        self.pack_start(self.combo_box, True, True, 0)
        renderer_text = Gtk.CellRendererText()
        self.combo_box.pack_start(renderer_text, True)
        self.combo_box.add_attribute(renderer_text, 'text', 0)
        self.combo_box.set_active(0)
        self.combo_box.connect('changed', self.on_change)
        self.listeners = {}
        self.value = None
        self.set_value(list(self.entries.keys())[0])
        if on_change is not None: self.connect('changed', on_change)
        self.ignore_signals = False

    def on_change(self, *args):
        if self.ignore_signals: return
        self.set_value(list(self.entries.keys())[self.combo_box.get_active()])

    def connect(self, signal, listener):
        if signal not in self.listeners: self.listeners[signal] = []
        self.listeners[signal].append(listener)

    def emit(self, signal, *args, **kwargs):
        if signal in self.listeners:
            for listener in self.listeners[signal]:
                listener(*args, **kwargs)

    def set_value(self, value, emit=True):
        if isinstance(value, str):
            value = self.entries_by_content[value]
        if value != self.value:
            self.value = value
            self.ignore_signals = True
            self.combo_box.set_active(list(self.entries.keys()).index(value))
            self.ignore_signals = False
            if emit: self.emit('changed', value)
