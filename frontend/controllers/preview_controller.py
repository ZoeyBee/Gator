import gi; gi.require_version('Gtk', '3.0'); from gi.repository import Gtk, GdkPixbuf

from frontend.controllers.base_controller import BaseController
from frontend.widgets.base_module import BaseModule

from pathlib import Path

from definitions import GRAPHICS_DIR

EMPTY_IMAGE = Path(GRAPHICS_DIR, 'loading.png').as_posix()


class PreviewController(BaseController):
    def setup_ui(self):
        preview_box = Gtk.Box(spacing=0); self.add(preview_box)
        self.preview_image = Gtk.Image().new_from_pixbuf(GdkPixbuf.Pixbuf.new_from_file_at_scale(EMPTY_IMAGE, 200, 200, True))
        preview_box.pack_start(self.preview_image, True, True, 0)
        self.show_merged = False
        self.use_video = False

    def on_frame_selected(self, frame):
        image_path = self.data.get_preview_at_frame(frame, self.manager.selected_layer)
        if not image_path: image_path = EMPTY_IMAGE
        else:              image_path = image_path.path.as_posix()
        try: self.preview_image.set_from_pixbuf(GdkPixbuf.Pixbuf.new_from_file_at_scale(image_path, 200, 200, True))
        except gi.repository.GLib.Error: pass

    def on_selected_preview_rendered(self, preview):
        if self.show_merged and preview.layer_uid != 'all': return
        try: self.preview_image.set_from_pixbuf(GdkPixbuf.Pixbuf.new_from_file_at_scale(preview.path.as_posix(), 200, 200, True))
        except gi.repository.GLib.Error: pass

    def on_preview_video_rendered(self, video):
        pass
        # print(video)
