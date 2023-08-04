import gi; gi.require_version('Gtk', '3.0'); from gi.repository import Gtk

from frontend.widgets.tree_combo_box import TreeComboBox
from frontend.widgets.button import Button
from frontend.widgets.editors.float_attribute_editor import FloatAttributeEditor
from frontend.widgets.editors.combo_attribute_editor import ComboAttributeEditor
from frontend.widgets.editors.position_attribute_editor import PositionAttributeEditor

from frontend.widgets.editors.base_editor import BaseEditor
from definitions import shared_objects


class GeneratorEditor(BaseEditor):
    def __init__(self, controller, generator):
        super(GeneratorEditor, self).__init__(controller)
        self.set_name('GeneratorEditor')
        self.generator = generator
        self.generator_type_combo_box = TreeComboBox(None, self.on_generator_type_changed)
        self.generator_type_combo_box.set_name('effectEditorIdComboBox')
        self.attach(self.generator_type_combo_box, 0, 0, 1, 1)
        self.generator_type_combo_box.add_option(['Wave'])
        self.generator_type_combo_box.set_value('Wave')

        self.generator.add_attribute_change_listener(self.on_attribute_changed)

    def on_delete_button_pressed(self, *args):
        self.controller.data.delete_generator(self.generator.uid)

    def on_generator_type_changed(self, generator_type):
        pass
        # shared_objects['data_manager'].set_generator_type(self.generator.uid, generator_type)
