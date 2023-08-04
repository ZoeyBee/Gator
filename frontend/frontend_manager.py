import gi; gi.require_version('Gtk', '3.0'); from gi.repository import Gtk, Gdk

from frontend.managers.graphics_manager import GraphicsManager
from frontend.managers.selection_manager import SelectionManager
from frontend.managers.styles_manager import StylesManager
from frontend.managers.keyboard_manager import KeyboardManager
from frontend.main_window import MainWindow

from backend.signal_handlers.frontend_signal_handler import FrontendSignalHandler

from definitions import shared_objects


class FrontendManager(GraphicsManager, SelectionManager, StylesManager, KeyboardManager):
    def __init__(self, setup_window=True):
        shared_objects['frontend_manager'] = self
        self.data = shared_objects['data_manager']
        self.data.add_signal_handler(FrontendSignalHandler, 'frontend', self)
        super(FrontendManager, self).__init__()
        if setup_window:
            self.setup_window()
            self.setup_data()
            self.setup_window_connections()
            Gtk.main()

    def setup_data(self):
        self.data.add_layer()
        self.data.set_layer_media(list(self.data.layers)[0], 'Image', 'tmp_input_image.jpg')
        # self.data.add_effect(self.selected_layer, 'gmic.Stereographic Projection')
        self.data.add_effect(self.selected_layer)

    def setup_window_connections(self):
        super(FrontendManager, self).setup_window_connections()

    def setup_window(self):
        self.window = MainWindow(self)
        self.window.show_all()
        self.window.connect('destroy', Gtk.main_quit)
        self.window.connect('destroy', self.data.shutdown)
