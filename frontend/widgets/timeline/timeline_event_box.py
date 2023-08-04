import gi; gi.require_version('Gtk', '3.0'); from gi.repository import Gtk, Gdk

from math import ceil


class TimelineEventBox(Gtk.EventBox):
    def __init__(self, parent):
        super(TimelineEventBox, self).__init__()
        self.parent = parent
        self.set_can_focus(True)
        self.add_events(Gdk.EventMask.SCROLL_MASK)
        self.add_events(Gdk.EventMask.KEY_PRESS_MASK)
        self.connect('button-press-event', self.on_button_press)
        self.connect('button-release-event', self.on_button_release)
        self.connect('motion-notify-event', self.on_motion)
        self.connect('scroll-event', self.on_scroll)

    def on_button_release(self, button, event):
        if event.x < self.parent.attribute_name_offset:
            attribute_index = int((event.y + self.parent.y_offset) / self.parent.attribute_height)
            i = 0
            for animator_name, animator in self.parent.visible_attributes.items():
                if i == attribute_index:
                    animator['collapsed'] = not animator['collapsed']
                    self.parent.background.queue_draw()
                    break
                i += 1
                if not animator['collapsed']:
                    for attribute_name, attribute in animator['attributes'].items():
                        i += 1
        else:
            frame = (ceil((event.x + self.parent.x_offset - self.parent.attribute_name_offset) /
                        self.parent.frame_distance) +
                    self.parent.frame_offset)
            self.parent.manager.select_frame(frame)

    def on_button_press(self, button, event):
        pass

    def on_motion(self, box, event):
        pass

    def on_scroll(self, box, event):
        direction = int(event.direction)
        if direction == 0: direction = -1
        delta = 10
        if event.x > self.parent.attribute_name_offset:
            if self.parent.manager.pressing_shift: self.parent.scale(delta * direction)
            else:                                  self.parent.scroll(delta * direction)
