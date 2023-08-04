import gi; gi.require_version('Gtk', '3.0'); from gi.repository import Gtk, Gdk

from frontend.controllers.layer_controller import LayerController
from frontend.controllers.effect_controller import EffectController
from frontend.controllers.generator_controller import GeneratorController
from frontend.controllers.preview_controller import PreviewController
from frontend.controllers.timeline_controller import TimelineController
from frontend.widgets.button import Button

from pathlib import Path

from time import sleep

from definitions import GRAPHICS_DIR, shared_objects


class MainWindow(Gtk.Window):
    def __init__(self, manager):
        Gtk.Window.__init__(self, title='forcefloat')
        self.connect('realize', self.after_init)
        self.screen_size = Gdk.Monitor.get_geometry(Gdk.Display.get_monitor(Gdk.Display.get_default(), 0))
        width, height = self.screen_size.width * 0.9, self.screen_size.height * 0.8
        self.set_default_size(width, height)
        self.manager = manager
        for style in self.manager.styles:
            Gtk.StyleContext.add_provider_for_screen(self.get_style_context().get_screen(), style, 800)

        root_grid = Gtk.Grid(); self.add(root_grid)
        self.effect = EffectController(root_grid, self.manager)
        self.generator = GeneratorController(root_grid, self.manager)
        self.timeline = TimelineController(root_grid, self.manager)

        box = Gtk.Box(orientation='vertical')
        preview = PreviewController(root_grid, self.manager); box.pack_start(preview, False, False, 0)
        layer = LayerController(box, self.manager); box.pack_start(layer, True, True, 0)

        root_grid.attach(self.effect,    0, 0, 1, 1)
        root_grid.attach(self.generator, 0, 1, 1, 1)
        root_grid.attach(self.timeline,  0, 2, 1, 1)
        root_grid.attach(box,            1, 0, 1, 2)

        self.manager.data.signals.add_listener('selected_keyframe_added', self.on_selected_keyframe_added)
        self.manager.data.signals.add_listener('attribute_animated_changed', self.on_attribute_animated_changed)
        self.manager.data.signals.add_listener('frame_selected', self.on_frame_selected)

    def after_init(self, *args):
        self.generator.on_toggle_collapse_button_pressed()
        # self.timeline.on_toggle_collapse_button_pressed()

    def on_selected_keyframe_added(self, keyframe):
        args = [keyframe.value]
        if 'position' in keyframe.attribute.attr_type: args.append(keyframe.attribute.dimension)
        if keyframe.uid in self.manager.data.generators:
            d = self.generator.generators[keyframe.uid].attributes
            if keyframe.attribute.name in d: d[keyframe.attribute.name].set_value(keyframe.value, emit=False)
        elif keyframe.uid in self.manager.data.effects:
            d = self.effect.effects[keyframe.uid].attributes
            if keyframe.attribute.name in d: d[keyframe.attribute.name].set_value(keyframe.value, emit=False)

    def on_frame_selected(self, frame):
        dimension = None
        for animator_uid, attributes in self.manager.data.animated_attributes.items():
            if animator_uid in self.manager.data.generators:
                for attribute_name, attribute in attributes.items():
                    if 'position' in attribute.attr_type:
                        dimension = attribute_name[-1]
                        attribute_name = attribute_name[:-1]
                    editor = self.generator.generators[animator_uid].attributes[attribute_name]
                    editor.set_value(attribute.get_value(frame), emit=False, dimesion=dimension)
            elif animator_uid in self.manager.data.effects:
                if self.manager.data.effects[animator_uid].layer != self.manager.selected_layer: continue
                for attribute_name, attribute in attributes.items():
                    if 'position' in attribute.attr_type:
                        dimension = attribute_name[-1]
                        attribute_name = attribute_name[:-1]
                    editor = self.effect.effects[animator_uid].attributes[attribute_name]
                    editor.set_value(attribute.get_value(frame), emit=False, dimension=dimension)

    def on_attribute_animated_changed(self, attribute):
        uid = attribute.parent.uid
        name = attribute.name
        if 'position' in attribute.attr_type: name = name[:-1]
        if uid in self.manager.data.generators:
            self.generator.generators[uid].attributes[name].on_animated_changed()
        elif uid in self.manager.data.effects:
            self.effect.effects[uid].attributes[name].on_animated_changed()
