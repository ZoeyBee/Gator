import gi; gi.require_version('Gtk', '3.0'); from gi.repository import Gtk

from utils.hex_to_rgb import hex_to_rgb
from utils.min_max import min_max

from math import ceil
from utils.delay import delay

from definitions import shared_objects


class TimelineBackground(Gtk.DrawingArea):
    def __init__(self, parent):
        super(TimelineBackground, self).__init__()
        self.parent = parent
        self.height = parent.height
        self.size = [100, self.height]
        self.setup_drawd()
        self.connect('draw', self.draw)
        self.connect('size-allocate', self.on_resize)
        self.set_size_request(100, self.size[1])

    def on_resize(self, *args):
        size = self.get_allocated_size()[0]
        self.size = [size.width, size.height]
        self.set_size_request(size.width, size.height)
        self.setup_drawd()

    def setup_drawd(self):
        self.drawd = {
            'x': 0, 'y': 0, 'width': self.size[0], 'height': self.size[1],
            'col_bg': hex_to_rgb(shared_objects['data_manager'].settings.colors['background_outline']),
            'col_line': hex_to_rgb(shared_objects['data_manager'].settings.colors['background_hover']),
            'col_line_selected': hex_to_rgb(shared_objects['data_manager'].settings.colors['accent']),
            'col_keyframe': hex_to_rgb(shared_objects['data_manager'].settings.colors['foreground_dark']),
            'col_text': hex_to_rgb(shared_objects['data_manager'].settings.colors['foreground_dark']),
        }
        self.drawd['col_line_highlight'] = [c + 0.05 for c in self.drawd['col_line']]
        self.queue_draw()

    def set_font_size_for_text(self, ctx, text, limit, start_size=20):
        font_size = start_size
        ctx.set_font_size(font_size)
        while ctx.text_extents(text).width > limit - 7:
            font_size -= 1; ctx.set_font_size(font_size)  # not ideal, replace with cool maths

    def draw(self, da, ctx):
        ctx.set_antialias(3)
        ctx.set_tolerance(1)

        ctx.new_path()
        ctx.move_to(self.drawd['x'], self.drawd['y'])
        ctx.line_to(self.drawd['width'], self.drawd['y'])
        ctx.line_to(self.drawd['width'], self.drawd['y']+self.drawd['height'])
        ctx.line_to(self.drawd['x'], self.drawd['y']+self.drawd['height'])
        ctx.line_to(self.drawd['x'], self.drawd['y'])
        ctx.close_path()
        ctx.set_source_rgb(*self.drawd['col_bg'])
        ctx.fill()

        visible_frames = ceil((self.drawd['width'] -
                               self.parent.attribute_name_offset) / self.parent.frame_distance) + 1
        for i in range(visible_frames):
            x = (self.parent.frame_distance * i) - self.parent.x_offset + self.parent.attribute_name_offset
            if x < self.parent.attribute_name_offset: continue
            frame = i + 1 + self.parent.frame_offset
            ctx.new_path()
            ctx.move_to(x, self.drawd['y'])
            ctx.line_to(x, self.drawd['y'] + self.drawd['height'])
            ctx.close_path()
            ctx.set_source_rgb(*self.drawd['col_line'])
            ctx.set_line_width(1)
            if frame == self.parent.manager.selected_frame:
                ctx.set_source_rgb(*self.drawd['col_line_selected'])
                ctx.set_line_width(2)
            elif frame % (self.parent.data.settings.fps / 2) == 0:
                ctx.set_source_rgb(*self.drawd['col_line_highlight'])
            ctx.stroke()

        width = self.parent.frame_distance * 0.4
        height = self.parent.attribute_height
        mheight = height - 5
        x_offset = (self.parent.attribute_name_offset - self.parent.x_offset +
                    (self.parent.frame_distance / 2) - (width / 2))
        ctx.select_font_face(self.parent.data.settings.font)
        ctx.set_font_size(20)
        text_height = ctx.text_extents('H').height
        y = 5
        if not self.parent.collapsed:
            y += self.parent.y_offset
            for animator_uid, animator in self.parent.visible_attributes.items():
                animator_name = shared_objects['data_manager'].objects[animator_uid].name
                self.set_font_size_for_text(ctx, animator_name, self.parent.attribute_name_offset)
                text_width = ctx.text_extents(animator_name).width + 10
                ctx.set_source_rgb(*self.drawd['col_text'])
                if animator['collapsed']:
                    ctx.move_to(self.parent.attribute_name_offset - text_width, y+text_height)
                    ctx.show_text(animator_name)
                    for attribute_name, keyframes in animator['attributes'].items():
                        drawn_frames = []
                        for frame in keyframes:
                            frame -= self.parent.frame_offset + 1
                            if frame > visible_frames or frame < -1: continue
                            if frame in drawn_frames: continue
                            drawn_frames.append(self)
                            x = (self.parent.frame_distance * frame) + x_offset
                            if x < self.parent.attribute_name_offset: continue
                            my = y - 5
                            ctx.new_path()
                            ctx.move_to(x, my+(mheight/2))
                            ctx.line_to(x+(width/2), my)
                            ctx.line_to(x+width, my+(mheight/2))
                            ctx.line_to(x+(width/2), my+mheight)
                            ctx.close_path()
                            ctx.set_source_rgb(*self.drawd['col_keyframe'])
                            ctx.fill()
                    y += self.parent.attribute_height
                else:
                    ctx.move_to(0, y+text_height)
                    ctx.show_text(animator_name)
                    y += self.parent.attribute_height
                    for attribute_name, keyframes in animator['attributes'].items():
                        self.set_font_size_for_text(ctx, attribute_name,
                                                    self.parent.attribute_name_offset)
                        text_width = ctx.text_extents(attribute_name).width + 5
                        ctx.set_source_rgb(*self.drawd['col_text'])
                        ctx.move_to(self.parent.attribute_name_offset - text_width, y+text_height)
                        ctx.show_text(attribute_name)
                        ctx.set_source_rgb(*self.drawd['col_keyframe'])
                        for frame in keyframes:
                            frame -= self.parent.frame_offset + 1
                            if frame > visible_frames or frame < -1: continue
                            x = (self.parent.frame_distance * frame) + x_offset
                            if x < self.parent.attribute_name_offset: continue
                            my = y - 5
                            ctx.new_path()
                            ctx.move_to(x, my+(mheight/2))
                            ctx.line_to(x+(width/2), my)
                            ctx.line_to(x+width, my+(mheight/2))
                            ctx.line_to(x+(width/2), my+mheight)
                            ctx.close_path()
                            ctx.set_source_rgb(*self.drawd['col_keyframe'])
                            ctx.fill()
                        y += self.parent.attribute_height

        ctx.save()
        ctx.restore()
