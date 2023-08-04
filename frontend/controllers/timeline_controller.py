import gi; gi.require_version('Gtk', '3.0'); from gi.repository import Gtk

from frontend.widgets.timeline.timeline_background import TimelineBackground
from frontend.widgets.timeline.timeline_event_box import TimelineEventBox
from frontend.widgets.timeline.timeline_button_box import TimelineButtonBox

from frontend.controllers.base_controller import BaseController
from frontend.widgets.base_module import BaseModule

from utils.interpolate import interpolate
from utils.min_max import min_max
from utils.delay import delay

from definitions import shared_objects

class TimelineController(BaseModule,
                         BaseController):
    module_name = 'Timeline'
    collapsed = False

    def setup_ui(self):
        super(TimelineController, self).setup_ui()
        BaseModule.total_modules -= 1
        self.box.remove(self.add_button)
        self.add_button.destroy()
        self.remove(self.scroll_area)
        self.scroll_area.destroy()
        self.height = 200
        self.frame_distance = 75
        self.x_offset = 0
        self.y_offset = 0
        self.frame_offset = 0
        self.attribute_name_offset = 150
        self.attribute_height = 30
        self.attributes = {}
        self.visible_attributes = {}
        self.target_attribute_name_offset = self.attribute_name_offset

        self.box.set_orientation(Gtk.Orientation(1))
        self.background = TimelineBackground(self)
        self.scroll_area.show_all()
        self.event_box = TimelineEventBox(self)
        self.event_box.add(self.background)
        self.pack_start(self.event_box, True, True, 0)

        self.playback_button_box = self.pack_start(TimelineButtonBox(self), False, False, False)

    def on_toggle_collapse_button_pressed(self, *args):
        if self.collapsed:
            self.collapsed = False
            self.collapse_button.set_image(self.icons['iconArrowDown'])
            self.header_box.remove(self.event_box)
            self.name_label.show()
            self.pack_start(self.event_box, False, False, 0)
            self.reorder_child(self.event_box, 1)
            self.background.size[1] = self.background.height
            self.background.setup_drawd()
            self.background.set_size_request(self.background.size[0],
                                             self.background.height)
            self.attribute_name_offset = self.target_attribute_name_offset
        else:
            self.collapsed = True
            self.collapse_button.set_image(self.icons['iconArrowUp'])
            self.remove(self.event_box)
            self.name_label.hide()
            self.header_box.pack_end(self.event_box, False, False, 0)
            self.background.size[1] = 30
            self.background.setup_drawd()
            self.background.set_size_request(self.background.size[0] - 50, 30)
            self.attribute_name_offset = 0

    def on_frame_selected(self, frame):
        self.background.queue_draw()

    def on_keyframe_added(self, keyframe):
        parent = keyframe.attribute.parent.uid
        name = keyframe.attribute.name
        if parent not in self.attributes:
            self.attributes[parent] = {'collapsed': True, 'attributes': {}}
        if name not in self.attributes[parent]['attributes']:
            self.attributes[parent]['attributes'][name] = []
        self.attributes[parent]['attributes'][name].append(keyframe.frame)
        self.background.queue_draw()

    def show_attribute(self, attribute):
        parent = attribute.parent.uid
        name = attribute.name
        if parent not in self.visible_attributes:
            self.visible_attributes[parent] = {'collapsed': False, 'attributes': {}}
        if name not in self.visible_attributes[parent]['attributes']:
            self.visible_attributes[parent]['attributes'][name] = self.attributes[parent]['attributes'][name]
        self.background.queue_draw()

    def hide_attribute(self, attribute):
        parent = attribute.parent.uid
        name = attribute.name
        if parent in self.visible_attributes:
            if name in self.visible_attributes[parent]['attributes']:
                self.visible_attributes[parent]['attributes'].pop(name)
            if not self.visible_attributes[parent]['attributes']:
                self.visible_attributes.pop(parent)
        self.background.queue_draw()

    def on_attribute_animated_changed(self, attribute):
        if attribute.animated: self.show_attribute(attribute)
        else:                  self.hide_attribute(attribute)

    def on_keyframe_deleted(self, keyframe):
        parent = keyframe.attribute.parent.uid
        name = keyframe.attribute.name
        self.attributes[parent]['attributes'][name].remove(keyframe.frame)
        if not self.attributes[parent]['attributes'][name]:
            self.attributes[parent]['attributes'].pop(name)
            if parent in self.visible_attributes and name in self.visible_attributes[parent]['attributes']:
                self.visible_attributes[parent]['attributes'].pop(name)
        if not self.attributes[parent]['attributes']:
            self.attributes.pop(parent)
            if parent in self.visible_attributes:
                self.visible_attributes.pop(parent)
        self.background.queue_draw()

    def scale(self, delta):
        self.x_offset = 0
        self.frame_distance = min_max(self.frame_distance - delta, 16, 160)
        self.background.queue_draw()

    def scroll(self, delta):
        self.x_offset += delta
        if self.x_offset > self.frame_distance:
            self.frame_offset += 1
            self.x_offset -= self.frame_distance
        elif self.x_offset < -self.frame_distance:
            self.frame_offset -= 1
            self.x_offset += self.frame_distance
        if self.frame_offset <= 0:
            self.frame_offset = 0
            if self.x_offset < 0: self.x_offset = 0
        self.background.queue_draw()
