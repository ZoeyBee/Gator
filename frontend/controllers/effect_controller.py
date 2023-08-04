import gi; gi.require_version('Gtk', '3.0'); from gi.repository import Gtk

from frontend.widgets.editors.effect_editor import EffectEditor
from frontend.controllers.base_controller import BaseController
from frontend.widgets.base_module import BaseModule

from utils.dict_instert_at_index import dict_insert_at_index

from frontend.widgets.button import Button


class EffectController(BaseModule,
                       BaseController):
    module_name = 'Effects'

    def setup_ui(self):
        super(EffectController, self).setup_ui()
        self.effects = {}

    def on_add_button_pressed(self, *args):
        self.data.add_effect(self.manager.selected_layer)

    def on_effect_added(self, effect):
        editor = EffectEditor(self, effect); self.box.add(editor)
        self.effects[effect.uid] = editor
        self.box.reorder_child(editor, effect.index+1)
        self.box.reorder_child(self.add_button, len(self.effects))
        editor.show_all()

    def on_layer_selected(self, layer):
        for effect_id, effect in self.effects.items(): effect.hide()
        for effect_id, effect in layer.effects.items(): self.effects[effect_id].show()

    def on_effect_deleted(self, effect):
        self.box.remove(self.effects[effect.uid])
        self.effects[effect.uid].destroy()
