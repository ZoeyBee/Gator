import gi; gi.require_version('Gtk', '3.0'); from gi.repository import Gtk

from frontend.widgets.tree_combo_box import TreeComboBox
from frontend.widgets.button import Button
from frontend.widgets.editors.float_attribute_editor import FloatAttributeEditor
from frontend.widgets.editors.combo_attribute_editor import ComboAttributeEditor
from frontend.widgets.editors.position_attribute_editor import PositionAttributeEditor

from frontend.widgets.editors.base_editor import BaseEditor

from definitions import EFFECTS, EFFECT_CATEGORIES, shared_objects


class EffectEditor(BaseEditor):
    def __init__(self, controller, effect):
        super(EffectEditor, self).__init__(controller)
        self.set_name('EffectEditor')
        self.effect = effect
        self.effect_id_combo_box = TreeComboBox(None, self.on_effect_id_changed,
                                                lambda e: f'{e[0]}.{e[-1]}',
                                                lambda e: e.split('.')[1])
        self.effect_id_combo_box.set_name('effectEditorIdComboBox')
        self.attach(self.effect_id_combo_box, 0, 0, 1, 1)
        for category, effects in EFFECT_CATEGORIES.items():
            category = category.split('.')
            for effect in effects:
                self.effect_id_combo_box.add_option([category[0], category[1], effect])
        self.effect_id_combo_box.set_value(self.effect.effect_id, emit=False)

        self.effect.add_attribute_change_listener(self.on_attribute_changed)

    def on_delete_button_pressed(self, *args):
        self.controller.data.delete_effect(self.effect.uid)

    def on_effect_id_changed(self, effect_id):
        shared_objects['data_manager'].set_effect_id(self.effect.uid, effect_id)
