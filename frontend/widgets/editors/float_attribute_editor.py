import gi; gi.require_version('Gtk', '3.0'); from gi.repository import Gtk, Gdk

from frontend.widgets.editors.base_attribute_editor import BaseAttributeEditor
from frontend.widgets.number_entry import NumberEntry

from math import pi
from utils.hex_to_rgb import hex_to_rgb
from utils.min_max import min_max
from utils.delay import delay
from utils.interpolate import interpolate

from definitions import shared_objects


class FloatAttributeEditor(BaseAttributeEditor):
    def __init__(self, attribute):
        super(FloatAttributeEditor, self).__init__(attribute)
        self.drawd = {
            'x': 19, 'y': 14, 'width': 397, 'height': 69, # nice
            'entry_width': 0,
            'handle_size': 14, 'handle_x': 19,
            'col_handle':  hex_to_rgb(shared_objects['data_manager'].settings.colors['foreground_dark']),
            'col_scale':   hex_to_rgb(shared_objects['data_manager'].settings.colors['background_hover']),
        }
        self.drawd['real_width'] = self.drawd['width'] - self.drawd['handle_size'] - 5 - self.drawd['entry_width']
        self.motion_timer = None
        self.motion_block_time = 0.5
        self.edit_mode_active = False

        self.set_value(self.attribute.default, emit=False)

    def setup_value_editor(self):
        self.value_editor_box = Gtk.Box(spacing=0)
        self.value_editor = Gtk.DrawingArea()
        self.value_editor.connect('draw', self.draw)
        self.value_editor.set_size_request(0, 35)
        self.event_box = Gtk.EventBox()
        self.value_editor_box.pack_start(self.event_box, True, True, 0)
        self.event_box.add(self.value_editor)
        self.event_box.set_can_focus(True)
        self.event_box.add_events(2); self.event_box.add_events(8)
        self.event_box.connect('motion-notify-event', self.on_motion)
        self.event_box.connect('button-press-event',  self.on_click)

    def on_motion(self, event_box, event):
        x = min_max(event.x, self.drawd['x'], self.drawd['real_width'])
        self.drawd['handle_x'] = x
        self.value_editor.queue_draw()
        value = interpolate(self.attribute.minimum, self.attribute.maximum,
                            (x - self.drawd['x']) / (self.drawd['real_width'] - self.drawd['x']))
        if self.motion_timer is not None: self.motion_timer.cancel()
        self.motion_timer = delay(self.set_value_from_pos, self.motion_block_time, [event.x])

    def on_click(self, event_box, event):
        if event.button == 1:
            self.set_value_from_pos(event.x)
        elif event.button == 3:
            pass
            # self.edit_mode_active = True
            # self.value_entry = NumberEntry(None, self.attribute.default, self.attribute.minimum, self.attribute.maximum)
            # self.value_editor_box.remove(self.event_box)
            # self.value_editor_box.pack_start(self.value_entry, True, True, 0)

    def set_value_from_pos(self, x, update_handle=True):
        width = self.drawd['real_width']
        x = min_max(x, self.drawd['x'], width)
        value = interpolate(self.attribute.minimum, self.attribute.maximum, (x - self.drawd['x']) / (width - self.drawd['x']))
        self.set_value(value, update_handle)

    def set_value(self, value, *args, **kwargs):
        super(FloatAttributeEditor, self).set_value(value, *args, **kwargs)
        weight = (value - self.attribute.minimum) / (self.attribute.maximum - self.attribute.minimum)
        width = self.drawd['real_width']
        self.drawd['handle_x'] = interpolate(self.drawd['x'], width, weight)
        self.value_editor.queue_draw()

    def draw(self, da, ctx):
        ctx.set_antialias(3)
        ctx.set_line_width(2)
        ctx.set_tolerance(1)

        ctx.new_path()
        x = self.drawd['x']
        y = self.drawd['y']-4
        width = self.drawd['real_width']
        height = 8
        ctx.move_to(x, y)
        ctx.line_to(width, y)
        ctx.line_to(width, y+height)
        ctx.line_to(x, y+height)
        ctx.line_to(x, y)
        ctx.close_path()
        ctx.set_source_rgb(*self.drawd['col_scale'])
        ctx.fill()

        ctx.new_path()
        ctx.arc(self.drawd['handle_x'], self.drawd['y'], self.drawd['handle_size'], 0, pi*2)
        ctx.close_path()
        ctx.set_source_rgb(*self.drawd['col_handle'])
        ctx.fill()

        ctx.restore()
        ctx.save()
