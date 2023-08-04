import gi; gi.require_version('Gtk', '3.0'); from gi.repository import Gtk
import cairo; gi.require_foreign('cairo')

from frontend.widgets.button import Button

from definitions import shared_objects


class BaseAttributeEditor(Gtk.Grid):
    def __init__(self, attribute=None):
        super(BaseAttributeEditor, self).__init__()
        self.attribute = attribute
        self.icons = {
            'keyframe_disabled': shared_objects['frontend_manager'].icon('keyframeMarkerEmpty', 25, 25),
            'keyframe_enabled':  shared_objects['frontend_manager'].icon('keyframeMarker', 25, 25),
            'settings': shared_objects['frontend_manager'].icon('iconSine', 25, 25),
        }
        self.value = None

        self.keyframe_button = Button(None, self.on_keyframe_button_pressed, image=self.icons['keyframe_disabled'])
        self.keyframe_button.set_name('hideBackground')

        self.name_label = Gtk.Label(); self.name_label.set_text(attribute.name)
        self.name_label.set_name('attributeNameLabel')

        self.settings_button = Button(None, self.on_settings_button_pressed, image=self.icons['settings'])
        self.settings_button.set_sensitive(False)
        self.settings_button.set_opacity(0.15)
        self.settings_button.set_name('hideBackground')

        self.setup_value_editor()
        self.value_editor.set_name('attributeValueEditor')

        self.attach(self.keyframe_button, 0, 0, 1, 1)
        self.attach(self.name_label,      1, 0, 1, 1)
        self.attach(self.settings_button, 2, 0, 1, 1)
        if hasattr(self, 'value_editor_box'): self.attach(self.value_editor_box, 0, 1, 3, 1)
        elif hasattr(self, 'event_box'):      self.attach(self.event_box,        0, 1, 3, 1)
        else:                                 self.attach(self.value_editor,     0, 1, 3, 1)

    def on_keyframe_button_pressed(self, *args):
        animated = not self.attribute.animated
        shared_objects['data_manager'].set_attribute_animated(self.attribute, animated)
        if hasattr(self, 'link_attribute'):
            shared_objects['data_manager'].set_attribute_animated(self.link_attribute, animated)

    def on_animated_changed(self, *args):
        if self.attribute.animated:
            self.keyframe_button.set_image(self.icons['keyframe_enabled'])
            self.settings_button.set_opacity(100)
            self.settings_button.set_sensitive(True)
        else:
            self.keyframe_button.set_image(self.icons['keyframe_disabled'])
            self.settings_button.set_opacity(0.15)
            self.settings_button.set_sensitive(False)

    def on_settings_button_pressed(self, *args):
        pass

    def set_value(self, value, emit=True, *args, **kwargs):
        if value != self.value:
            self.value = self.attribute.clean_value(value)
            if emit:
                shared_objects['data_manager'].add_keyframe(shared_objects['frontend_manager'].selected_frame,
                                                            self.attribute.parent.uid, self.attribute.name, self.value)
