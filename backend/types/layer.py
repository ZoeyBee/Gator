from utils.dict_instert_at_index import dict_insert_at_index

from backend.types.base_type import BaseType
from backend.types.image_input import ImageInput


class Layer(BaseType):
    attributes = {'blend_amount': {'type': 'int', 'value': 100, 'min': 0, 'max': 100}}

    def __init__(self, data, uid, name, media=None, blend_mode='Normal', index=None, *args, **kwargs):
        super(Layer, self).__init__(data, uid, *args, **kwargs)

        self.name = name
        self.effects = {}
        self.media = media
        self.blend_mode = blend_mode
        self.index = index
        dict_insert_at_index(self.data.layers, uid, self, index)
        self.data.signals.call_signal('layer_added', self)
        self.setup_attributes(self.attributes)

    def set_media(self, media_type, media_path):
        if media_type == 'Image': self.media = ImageInput(media_path)
        else:                     self.media = None
        self.data.signals.call_signal('layer_media_changed', self)

    def set_blend_mode(self, blend_mode):
        self.blend_mode = blend_mode
        self.data.signals.call_signal('layer_blend_mode_changed', self)

    def set_name(self, name):
        old_name = self.name; self.name = name
        self.data.signals.call_signal('layer_name_changed', self, old_name)

    def delete(self):
        super(Layer, self).delete()
        self.data.layers.pop(self.uid)
        self.data.signals.call_signal('layer_deleted', self)
        for __, effect in self.effects.items(): effect.delete()

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name
