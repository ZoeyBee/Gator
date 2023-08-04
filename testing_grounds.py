import gi; gi.require_version('Gtk', '3.0'); from gi.repository import Gtk

from backend.data_manager import DataManager
from frontend.frontend_manager import FrontendManager

from frontend.widgets.editors.float_attribute_editor import FloatAttributeEditor

def press(*args):
    print('hey', args)

data = DataManager()
manager = FrontendManager(False)

data.add_layer()
data.set_layer_media(list(data.layers)[0], 'Image', 'tmp_input_image.jpg')

window = Gtk.Window()
window.set_title('forcefloat')
box = Gtk.Box()
window.add(box)
editor = FloatAttributeEditor()
box.pack_start(editor, True, True, 0)
# window.connect('button-press-event', press)
# window.connect('motion-notify-event', press)

window.show_all()
window.connect('destroy', Gtk.main_quit)
Gtk.main()

