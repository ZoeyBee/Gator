import gi; gi.require_version('Gtk', '3.0'); from gi.repository import Gtk


class Button(Gtk.Button):
    def __init__(self, container=None, on_click=None, image=None, label=None):
        super(Button, self).__init__()
        if image is not None and label is not None:
            self.label = Gtk.Label(label); box = Gtk.Box(); self.add(box)
            box.pack_start(self.label, False, False, 0)
            box.pack_end(image, False, False, 0)
            self.image = image
        else:
            if image is not None: self.set_image(image)
            if label is not None: self.set_label(label)
        if on_click  is not None: self.connect('clicked', on_click)
        if container is not None: container.pack_start(self, True, True, 0)
