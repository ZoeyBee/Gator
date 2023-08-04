import gi; gi.require_version('Gtk', '3.0'); from gi.repository import Gtk

from frontend.widgets.tree_combo_box import TreeComboBox
from frontend.widgets.button import Button
from frontend.widgets.editors.float_attribute_editor import FloatAttributeEditor
from frontend.widgets.editors.combo_attribute_editor import ComboAttributeEditor
from frontend.widgets.editors.position_attribute_editor import PositionAttributeEditor

from definitions import EFFECTS, EFFECT_CATEGORIES, shared_objects


class BaseEditor(Gtk.Grid):
    def __init__(self, controller):
        super(BaseEditor, self).__init__()
        self.controller = controller
        self.attributes = {}

        self.delete_button = Button(None, self.on_delete_button_pressed,
                                    image=self.controller.manager.icon('iconDelete', 30, 30))
        self.delete_button.set_name('EffectDeleteButton')
        self.attach(self.delete_button, 1, 0, 1, 1)

        self.attribute_scroll_area = Gtk.ScrolledWindow()
        self.attribute_scroll_area.set_vexpand(True)
        self.attribute_scroll_area.set_name('AttributeScrollArea')
        self.attribute_scroll_area_box = Gtk.Box(orientation='vertical', spacing=0)
        self.attribute_scroll_area.add(self.attribute_scroll_area_box)
        self.attach(self.attribute_scroll_area, 0, 1, 2, 1)

    def on_attribute_changed(self, attribute, add_or_del):
        if attribute.attr_type == 'invisible': return
        name = attribute.name
        if add_or_del == 'add':
            if attribute.attr_type == 'combo': Editor = ComboAttributeEditor
            elif 'position' in attribute.attr_type:
                name = attribute.name[:-1]
                if name in self.attributes:
                    self.attributes[name].add_link(attribute)
                    return
                Editor = PositionAttributeEditor
            else: Editor = FloatAttributeEditor
            editor = Editor(attribute); self.attribute_scroll_area_box.pack_start(editor, False, False, 0)
            editor.show_all()
            self.attributes[name] = editor
        else:
            if 'position' in attribute.attr_type: name = name[:-1]
            if name in self.attributes:
                self.attribute_scroll_area_box.remove(self.attributes[name])
                self.attributes[name].destroy()
                self.attributes.pop(name)
