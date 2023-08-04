import gi; gi.require_version('Gtk', '3.0'); from gi.repository import Gtk, Gdk

from frontend.widgets.editors.base_attribute_editor import BaseAttributeEditor
from frontend.widgets.tree_combo_box import TreeComboBox


class ComboAttributeEditor(BaseAttributeEditor):
    def __init__(self, attribute):
        super(ComboAttributeEditor, self).__init__(attribute)
        self.set_value(self.attribute.default, emit=False)

    def setup_value_editor(self):
        self.value_editor = TreeComboBox(self.attribute.options, self.set_value, scrolling=False)
        self.value_editor.set_size_request(0, 35)
        self.value_editor.button.set_name('comboAttributeEditor')

    def set_value(self, value, *args, **kwargs):
        if isinstance(value, str): value = self.value_editor.entries.index(value)
        super(ComboAttributeEditor, self).set_value(value, *args, **kwargs)
        self.value_editor.set_value(self.value_editor.entries[value], False)
