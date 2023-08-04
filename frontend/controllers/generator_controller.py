import gi; gi.require_version('Gtk', '3.0'); from gi.repository import Gtk

from frontend.widgets.editors.generator_editor import GeneratorEditor
from frontend.controllers.base_controller import BaseController
from frontend.widgets.base_module import BaseModule
from frontend.widgets.button import Button

from utils.delay import delay


class GeneratorController(BaseModule,
                          BaseController):
    module_name = 'CV Generators'
    collapsed = False

    def setup_ui(self):
        super(GeneratorController, self).setup_ui()
        self.generators = {}

    def on_add_button_pressed(self, button):
        self.data.add_generator()

    def on_generator_added(self, generator):
        editor = GeneratorEditor(self, generator); self.box.add(editor)
        self.generators[generator.uid] = editor
        self.box.reorder_child(editor, generator.index+1)
        self.box.reorder_child(self.add_button, len(self.generators))
        editor.show_all()

    def on_generator_deleted(self, generator):
        self.box.remove(self.generators[generator.uid])
        self.generators[generator.uid].destroy()
