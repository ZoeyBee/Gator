import gi; gi.require_version('Gtk', '3.0'); from gi.repository import Gtk
from utils.dict_instert_at_index import dict_insert_at_index


class Tree(Gtk.TreeView):
    def __init__(self, container=None, search=False, reorderable=True, editable=False):
        super(Tree, self).__init__()
        if container is not None: container.pack_start(self, True, True, 0)
        self.entries = {}
        if not hasattr(self, 'store'): self.store = Gtk.ListStore(str, int)
        self.value = None
        self.listeners = {}
        self.ignore_signals = False
        self.get_selection().connect('changed', self.on_change)
        self.set_model(self.store)
        column = Gtk.TreeViewColumn()
        self.append_column(column)
        renderer_text = Gtk.CellRendererText()
        renderer_text.set_property('editable', editable)
        renderer_text.connect('edited', self.on_text_changed)
        column.pack_start(renderer_text, True)
        column.add_attribute(renderer_text, 'text', 0)
        self.set_headers_visible(False)
        self.get_selection().select_path(Gtk.TreePath(0))
        self.set_reorderable(reorderable)
        self.store.connect('row-inserted', self.on_reorder)
        self.react_to_insert = True
        self.set_enable_search(search)

    def on_text_changed(self, cell, path, new_value):
        real_path = list(self.entries.keys())[int(path)]
        if self.entries[real_path] != new_value:
            self.emit('name_changed', real_path, new_value)

    def set_entry_value(self, path, value, column=0):
        real_path = list(self.entries.keys())[int(path)]
        self.entries[real_path] = value
        self.store.set_value(self.store.get_iter(int(path)), column, value)

    def on_reorder(self, store, index, tree_iter):
        if self.react_to_insert:
            for i in range(len(self.entries)):
                print(store.get_value(store.get_iter(i), 0), store.get_value(store.get_iter(i), 1))

    def add_entry(self, uid, text, index):
        dict_insert_at_index(self.entries, uid, text, index - len(self.entries))
        self.react_to_insert = False
        if index == len(self.entries) - 1: self.store.prepend([text, uid])
        else: self.store.insert_before(self.store.get_iter(index), [text, uid])
        self.set_value(uid)
        self.react_to_insert = True

    def del_entry(self, uid):
        if uid in self.entries:
            index = list(self.entries.keys()).index(uid)
            self.entries.pop(uid)
            self.store.remove(self.store.get_iter(index))
            if self.value == uid:
                if index > 0: index -= 1
                if len(self.entries) > 0:
                    uid = list(self.entries.keys())[index]
                    self.set_value(uid)

    def on_change(self, event):
        if self.ignore_signals: return
        i = self.get_cursor().path
        if i is not None:
            i = int(str(i))
            self.set_value(list(self.entries.keys())[i])

    def connect(self, signal, listener):
        if signal not in self.listeners: self.listeners[signal] = []
        self.listeners[signal].append(listener)

    def emit(self, signal, *args, **kwargs):
        if signal in self.listeners:
            for listener in self.listeners[signal]:
                listener(*args, **kwargs)

    def get_index(self, value):
        return list(self.entries.keys()).index(value)

    def set_value(self, value):
        if value != self.value:
            self.value = value
            index = list(self.entries.keys()).index(value)
            self.ignore_signals = True
            self.get_selection().select_path(Gtk.TreePath(index))
            self.ignore_signals = False
            self.emit('changed', value)
