import gi; gi.require_version('Gtk', '3.0'); from gi.repository import Gtk

from frontend.controllers.base_controller import BaseController
from frontend.widgets.number_entry import NumberEntry
from frontend.widgets.combo_box import ComboBox
from frontend.widgets.tree_combo_box import TreeComboBox
from frontend.widgets.button import Button
from frontend.widgets.tree import Tree


class LayerController(BaseController):
    def connect_signals(self):
        self.layer_list.connect('changed', self.on_layer_list_changed)
        self.layer_list.connect('name_changed', self.on_layer_list_name_changed)
        self.max_input_length = 20

    def setup_ui(self):
        input_button_box = Gtk.Box(orientation='horizontal', spacing=0); self.add(input_button_box)
        self.input_clone_button = Button(input_button_box, self.on_input_button_clicked, label='Clone')
        self.input_video_button = Button(input_button_box, self.on_input_button_clicked, label='Video')
        self.input_image_button = Button(input_button_box, self.on_input_button_clicked, label='Image')
        self.layer_input_info = Gtk.Label(); self.layer_input_info.hide()
        input_button_box.pack_start(self.layer_input_info, True, True, 0)
        self.input_change_button = Button(input_button_box, self.on_input_button_clicked, label='Change')
        self.input_change_button.hide()

        layer_button_box = Gtk.Box(orientation='horizontal', spacing=0); self.add(layer_button_box)
        self.layer_add_button = Button(layer_button_box, self.on_add_layer_button_clicked,
                                       image=self.manager.icon('iconPlus', 70, 30))
        self.layer_del_button = Button(layer_button_box, self.on_delete_layer_button_clicked,
                                       image=self.manager.icon('iconMinus', 70, 30))
        self.layer_blend_mode_box = TreeComboBox(self.data.blending_modes, self.on_blend_mode_box_changed)
        layer_button_box.pack_start(self.layer_blend_mode_box, True, False, 0)
        self.layer_blend_mode_box.set_name('layerBlendModeBox')
        self.layer_opacity_entry = NumberEntry(layer_button_box, 100, 0, 100, self.on_layer_opacity_entry_changed)

        self.layer_list_scroll = Gtk.ScrolledWindow()
        self.pack_start(self.layer_list_scroll, True, True, 0)
        self.layer_list = Tree(reorderable=False, editable=True); self.layer_list_scroll.add(self.layer_list)

    def load_layer_media(self, media):
        if media is None:
            self.input_clone_button.show()
            self.input_image_button.show()
            self.input_video_button.show()
            self.input_change_button.hide()
            self.layer_input_info.hide()
        else:
            self.layer_input_info.show()
            input_path = media.input_path
            if len(input_path) > self.max_input_length:
                input_path = f'{input_path[0:self.max_input_length-3]}...'
            elif len(input_path) < self.max_input_length:
                input_path = input_path + ' ' * (self.max_input_length - len(input_path))
            self.layer_input_info.set_text(f'{media.type}: {input_path}')
            self.input_change_button.show()
            self.input_clone_button.hide()
            self.input_image_button.hide()
            self.input_video_button.hide()

    def on_input_button_clicked(self, button, *args):
        input_type = button.get_label()
        if input_type != 'Change':
            dialog = Gtk.FileChooserDialog(action=Gtk.FileChooserAction(0), title='Open', buttons=('Cancel', 0, 'Open', 1))
            if dialog.run():
                path = dialog.get_filename(); dialog.destroy()
                if path is not None: self.data.set_layer_media(self.manager.selected_layer, input_type, path)
        else:
            self.data.set_layer_media(self.manager.selected_layer, None, None)
    def on_layer_opacity_entry_changed(self, value):
        self.data.add_keyframe(self.manager.selected_frame, self.manager.selected_layer, 'blend_amount', value)
    def on_blend_mode_box_changed(self, blend_mode): self.data.set_layer_blend_mode(self.manager.selected_layer, blend_mode)
    def on_delete_layer_button_clicked(self, *args):
        if len(self.data.layers) > 1: self.data.delete_layer(self.manager.selected_layer)
    def on_add_layer_button_clicked(self, *args): self.data.add_layer(index=self.layer_list.get_index(self.manager.selected_layer))
    def on_layer_list_changed(self, *args): self.manager.select_layer(self.layer_list.value)
    def on_layer_list_name_changed(self, uid, name): self.data.set_layer_name(uid, name)

    def on_layer_added(self, layer): self.layer_list.add_entry(layer.uid, layer.name, layer.index)
    def on_layer_deleted(self, layer): self.layer_list.del_entry(layer.uid)
    def on_selected_layer_blend_mode_changed(self, layer): self.layer_blend_mode_box.set_value(layer.blend_mode, emit=False)
    def on_selected_layer_media_changed(self, layer): self.load_layer_media(layer.media)
    def on_layer_name_changed(self, layer, old_name):
        self.layer_list.set_entry_value(self.layer_list.get_index(layer.uid), layer.name)
    def on_layer_selected(self, layer):
        self.layer_list.set_value(layer.uid)
        self.layer_blend_mode_box.set_value(layer.blend_mode)
        if isinstance(layer.attributes['blend_amount'], dict):
            self.layer_opacity_entry.set_value(layer.attributes['blend_amount']['value'])
        else:
            self.layer_opacity_entry.set_value(layer.attributes['blend_amount'].get_value(self.manager.selected_frame))
        self.load_layer_media(layer.media)
    def on_selected_keyframe_added(self, keyframe):
        if keyframe.attribute.name == 'blend_amount' and keyframe.uid == self.manager.selected_layer:
            self.layer_opacity_entry.set_value(keyframe.value)
