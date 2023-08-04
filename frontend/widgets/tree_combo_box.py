import gi; gi.require_version('Gtk', '3.0'); from gi.repository import Gtk

from utils.delay import delay

from frontend.widgets.button import Button
from frontend.widgets.tree import Tree

from definitions import shared_objects


class TreeComboBox(Gtk.Box):
    def __init__(self, entries, on_change, value_format=None, label_format=None, scrolling=False):
        super(TreeComboBox, self).__init__()
        self.entries = []
        self.value = None
        self.dialog = TreeDialog(self)
        self.button = Button(self, self.on_button_pressed,
                             shared_objects['frontend_manager'].icon('iconArrowDown'),
                             '')
        self.on_change = on_change
        self.value_format = value_format
        self.label_format = label_format
        if entries is not None:
            for entry in entries: self.add_option(entry)

    def add_option(self, option):
        self.dialog.tree_view.add_entry(option)
        self.entries.append(option)

    def on_button_pressed(self, button):
        self.dialog.start()

    def set_value(self, value, emit=True):
        if self.label_format: self.button.label.set_text(self.label_format(value))
        else:                 self.button.label.set_text(value)
        self.value = value
        if self.on_change is not None and emit:
            self.on_change(value)
        if self.dialog.value != value:
            self.dialog.set_value(value, emit=False)


class TreeDialog(Gtk.Dialog):
    def __init__(self, parent):
        super(TreeDialog, self).__init__(self)
        self.parent = parent
        for style in shared_objects['frontend_manager'].styles:
            Gtk.StyleContext.add_provider_for_screen(self.get_style_context().get_screen(), style, 800)
        self.set_modal(True)
        self.set_decorated(False)
        self.attached = False
        if hasattr(shared_objects['frontend_manager'], 'window'):
            self.set_attached_to(shared_objects['frontend_manager'].window)
            self.attached = True
        self.connect('button_press_event', self.on_click)
        self.box = self.get_content_area()
        self.tree_view = TreeTree(self)
        self.scroll_window = Gtk.ScrolledWindow()
        self.box.pack_start(self.scroll_window, True, True, 0)
        self.scroll_window.add(self.tree_view)
        self.scroll_window.set_propagate_natural_width(True)
        self.scroll_window.set_propagate_natural_height(True)
        self.box.show_all()
        self.set_keep_above(True)
        self.tree_view.connect('changed', self.set_value)
        self.value = None

    def start(self):
        self.set_position(Gtk.WindowPosition(2))
        self.scroll_window.remove(self.tree_view)
        self.tree_view.expand_to_path(Gtk.TreePath(self.tree_view.entries_by_content[self.value]))
        self.tree_view.get_selection().select_path(Gtk.TreePath(self.tree_view.entries_by_content[self.value]))
        self.scroll_window.add(self.tree_view)
        if not self.attached: self.set_attached_to(shared_objects['frontend_manager'].window)
        self.scroll_window.set_max_content_height(shared_objects['frontend_manager'].window.screen_size.height)
        self.run()
        self.hide()
        if self.value is not None and self.value != self.parent.value:
            self.parent.set_value(self.value)

    def set_value(self, value, emit=False):
        self.response(0)
        self.value = value
        if self.tree_view.value != value: self.tree_view.set_value(value, emit)

    def on_click(self, button, event):
        if self.is_active(): return
        self.response(0)


class TreeTree(Tree): # Dont judge me
    def __init__(self, parent, *args, **kwargs):
        self.store = Gtk.TreeStore(str)
        self.depth = 0
        self.entries_by_content = {}
        self.content_by_entries = {}
        self._parent = parent
        super(TreeTree, self).__init__(*args, reorderable=False, **kwargs)
        self.set_headers_clickable(True)

    def add_entry(self, entry):
        index = len(self.entries)
        self.react_to_insert = False
        entries_navigator = self.entries
        iter = None
        depth = 0
        content = ''
        if isinstance(entry, str): entry = [entry]
        for e in entry:
            if e in entries_navigator:
                place = list(entries_navigator).index(e)
                iter = self.store.iter_nth_child(iter, place)
            else:
                place = len(entries_navigator)
                iter = self.store.append(iter, ['0'])
                self.store.set(iter, {0: e})
                entries_navigator[e] = {}
            depth += 1
            content += f':{place}'
            entries_navigator = entries_navigator[e]
        if self._parent.parent.value_format:
            e = self._parent.parent.value_format(entry)
        self.entries_by_content[e] = content[1:]
        self.content_by_entries[content[1:]] = e
        if depth > self.depth: self.depth = depth
        self.react_to_insert = True

    def on_change(self, event):
        if self.ignore_signals: return
        i = self.get_cursor().path
        if i is not None:
            if len(str(i).split(':')) == self.depth:
                self.set_value(self.content_by_entries[str(i)])
            else:
                self.get_selection().select_path(Gtk.TreePath(self.entries_by_content[self.value]))

    def set_value(self, value, emit=True):
        if value != self.value:
            self.value = value
            self.ignore_signals = True
            self.expand_to_path(Gtk.TreePath(self.entries_by_content[value]))
            self.get_selection().select_path(Gtk.TreePath(self.entries_by_content[value]))
            self.ignore_signals = False
            if emit: self.emit('changed', value)
