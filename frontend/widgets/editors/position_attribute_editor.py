import gi; gi.require_version('Gtk', '3.0'); from gi.repository import Gtk, Gdk
from frontend.widgets.editors.base_attribute_editor import BaseAttributeEditor

from math import pi
from utils.hex_to_rgb import hex_to_rgb
from utils.min_max import min_max
from utils.delay import delay
from utils.interpolate import interpolate

from definitions import shared_objects


class PositionAttributeEditor(BaseAttributeEditor):
    def __init__(self, attribute):
        super(PositionAttributeEditor, self).__init__(attribute)
        self.drawd = {
            'x': 19, 'y': 0, 'width': 398, 'height': 179,
            'real_x': 33, 'real_y': 14,
            'handle_x': 33, 'handle_y': 14, 'handle_size': 14,
            'col_handle':  hex_to_rgb(shared_objects['data_manager'].settings.colors['foreground_dark']),
            'col_scale':   hex_to_rgb(shared_objects['data_manager'].settings.colors['background_hover']),
        }
        self.drawd['real_width'] = self.drawd['width'] - self.drawd['handle_size'] - 5
        self.drawd['handle_max_x'] = self.drawd['real_width'] - self.drawd['handle_size']
        self.drawd['handle_max_y'] = self.drawd['height'] - self.drawd['handle_size']
        self.motion_block_time = 0.5
        self.x_motion_timer = None
        self.y_motion_timer = None
        self.value = {'x': None, 'y': None}

    def add_link(self, link_attribute):
        self.link_attribute = link_attribute
        self.set_value(self.attribute.default, 'x', emit=False)
        self.set_value(self.attribute.default, 'y', emit=False)

    def setup_value_editor(self):
        self.value_editor = Gtk.DrawingArea()
        self.value_editor.connect('draw', self.draw)
        self.value_editor.set_size_request(0, 180)
        self.event_box = Gtk.EventBox()
        self.event_box.add(self.value_editor)
        self.event_box.set_can_focus(True)
        self.event_box.add_events(2); self.event_box.add_events(8)
        self.event_box.connect('motion-notify-event', self.on_motion)
        self.event_box.connect('button-press-event',  self.on_click)
        self.name_label.set_text(self.attribute.name[:-1])

    def on_motion(self, event_box, event):
        x = min_max(event.x, self.drawd['real_x'], self.drawd['handle_max_x'])
        y = min_max(event.y, self.drawd['real_y'], self.drawd['handle_max_y'])
        self.drawd['handle_x'] = x; self.drawd['handle_y'] = y
        self.value_editor.queue_draw()
        value_x = interpolate(self.attribute.minimum, self.attribute.maximum,
                              (x - self.drawd['x']) / (self.drawd['handle_max_x'] - self.drawd['x']))
        value_y = interpolate(self.attribute.minimum, self.attribute.maximum,
                              (y - self.drawd['y']) / (self.drawd['handle_max_y'] - self.drawd['y']))
        if self.x_motion_timer is not None: self.x_motion_timer.cancel()
        if self.y_motion_timer is not None: self.y_motion_timer.cancel()
        self.x_motion_timer = delay(self.set_value_from_pos, self.motion_block_time, [event.x, 'x'])
        self.y_motion_timer = delay(self.set_value_from_pos, self.motion_block_time, [event.y, 'y'])

    def on_click(self, event_box, event):
        self.set_value_from_pos(event.x, 'x')
        self.set_value_from_pos(event.y, 'y')

    def set_value_from_pos(self, pos, dimension, update_handle=True):
        if dimension == 'x':
            x = min_max(pos, self.drawd['real_x'], self.drawd['handle_max_x'])
            value = interpolate(self.attribute.minimum, self.attribute.maximum,
                                (x - self.drawd['real_x']) / (self.drawd['handle_max_x']- self.drawd['real_x']))
        elif dimension == 'y':
            y = min_max(pos, self.drawd['real_y'], self.drawd['handle_max_y'])
            value = interpolate(self.attribute.minimum, self.attribute.maximum,
                                (y - self.drawd['real_y']) / (self.drawd['handle_max_y']- self.drawd['real_y']))
        self.set_value(value, dimension, update_handle)

    def set_value(self, value, dimension='x', emit=True, *args, **kwargs):
        if value != self.value[dimension]:
            if (dimension == 'x' and self.attribute.dimension == 'x' or
                dimension == 'y' and self.attribute.dimension == 'y'):
                attribute = self.attribute
            else:
                attribute = self.link_attribute

            self.value[dimension] = attribute.clean_value(value)
            if emit:
                shared_objects['data_manager'].add_keyframe(shared_objects['frontend_manager'].selected_frame,
                                                            attribute.parent.uid, attribute.name, self.value[dimension])

            weight = (value - attribute.minimum) / (attribute.maximum - attribute.minimum)
            if dimension == 'x': self.drawd['handle_x'] = interpolate(self.drawd['real_x'], self.drawd['handle_max_x'], weight)
            if dimension == 'y': self.drawd['handle_y'] = interpolate(self.drawd['real_y'], self.drawd['handle_max_y'], weight)
            self.value_editor.queue_draw()

    def draw(self, da, ctx):
        ctx.set_antialias(3)
        ctx.set_line_width(2)
        ctx.set_tolerance(1)

        ctx.new_path()
        ctx.move_to(self.drawd['x'], self.drawd['y'])
        ctx.line_to(self.drawd['real_width'], self.drawd['y'])
        ctx.line_to(self.drawd['real_width'], self.drawd['y']+self.drawd['height'])
        ctx.line_to(self.drawd['x'], self.drawd['y']+self.drawd['height'])
        ctx.line_to(self.drawd['x'], self.drawd['y'])
        ctx.close_path()
        ctx.set_source_rgb(*self.drawd['col_scale'])
        ctx.fill()

        ctx.new_path()
        ctx.arc(self.drawd['handle_x'],
                self.drawd['handle_y'],
                self.drawd['handle_size'], 0, pi*2)
        ctx.close_path()
        ctx.set_source_rgb(*self.drawd['col_handle'])
        ctx.fill()

        ctx.restore()
        ctx.save()
