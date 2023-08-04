from backend.types.base_type import BaseType
from utils.dict_place_or_create import dict_place_or_create

from pathlib import Path

from definitions import PREVIEW_DIR


class Preview(BaseType):
    def __init__(self, data, frame, layer_uid):
        super(Preview, self).__init__(data, None)
        self.image = None
        self.frame = frame
        self.rendering = True
        self.renderer = None
        self.layer_uid = layer_uid
        self.path = Path(PREVIEW_DIR, f'{self.frame}{layer_uid}.png')
        dict_place_or_create(self.data.previews, self.frame, self.layer_uid, self)
        self.data.signals.call_signal('preview_added', self)
        if self.layer_uid != 'all': self.data.rendering_previews.append(self)
        if layer_uid == 'all':
            self.layer = 'all'
            images = []
            for layer_uid, preview in self.data.previews[frame].items():
                if layer_uid == 'all': continue
                image = preview.get_image()
                if image: images.append([image,
                                         self.data.render_states[frame].layers[layer_uid]['blend_mode'],
                                         self.data.render_states[frame].layers[layer_uid]['attributes']['blend_amount']])
                else: return
            self.renderer = self.data.merge_layers(images, self.set_image)
        else:
            self.layer = self.data.layers[layer_uid]
            if not self.layer.media: return
            self.renderer = self.data.render(self.frame, self.layer.uid, self.data.settings.preview_render_scale, self.set_image)

    def set_image(self, image, *args, **kwargs):
        self.rendering = False
        self.renderer = None
        self.image = image
        if self in self.data.rendering_previews: self.data.rendering_previews.remove(self)
        self.image.save(self.path)
        self.data.signals.call_signal('preview_rendered', self)

    def get_image(self):
        if self.image: return self.image

    def delete(self):
        self.data.previews[self.frame].pop(self.layer_uid)
        if not self.data.previews[self.frame]: self.data.previews.pop(self.frame)
        self.data.signals.call_signal('preview_deleted', self)
        if self.renderer:
            exit()
            self.renderer.stop()

    def as_string(self):
        return f'{self.frame} {self.layer_uid}'

    def __str__(self): return self.as_string()
    def __repr__(self): return self.as_string()
