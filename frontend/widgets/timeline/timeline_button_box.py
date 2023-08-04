import gi; gi.require_version('Gtk', '3.0'); from gi.repository import Gtk
from frontend.widgets.button import Button

from definitions import shared_objects

class TimelineButtonBox(Gtk.Box):
    def __init__(self, parent):
        super(TimelineButtonBox, self).__init__()
        self.parent = parent
        add_button = lambda button: (self.pack_start(button, False, False, True),
                                     button.set_name('playbackButton'))

        self.back_back_button = Button(None, None, image=self.parent.manager.icon('iconBackwards', 25, 25))
        add_button(self.back_back_button)
        self.back_button = Button(None, None, image=self.parent.manager.icon('iconStepBackwards', 25, 25))
        add_button(self.back_button)
        self.play_button = Button(None, self.on_play_button_pressed, image=self.parent.manager.icon('iconPlay', 25, 25))
        add_button(self.play_button)
        self.pause_button = Button(None, None, image=self.parent.manager.icon('iconPause', 25, 25))
        add_button(self.pause_button)
        self.pause_button.hide()
        self.stop_button = Button(None, None, image=self.parent.manager.icon('iconStop', 25, 25))
        add_button(self.stop_button)
        self.forward_button = Button(None, None, image=self.parent.manager.icon('iconStepForwards', 25, 25))
        add_button(self.forward_button)
        self.forward_forward_button = Button(None, None, image=self.parent.manager.icon('iconForwards', 25, 25))
        add_button(self.forward_forward_button)

    def on_play_button_pressed(self, *args, **kwargs):
        shared_objects['data_manager'].start_playing
        self.pause_button.show()

