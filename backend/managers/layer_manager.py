from backend.types.image_input import ImageInput
from backend.types.layer import Layer
from backend.types.uid import UID


class LayerManagerMixin:
    def __init__(self, *args, **kwargs):
        super(LayerManagerMixin, self).__init__(*args, **kwargs)
        self.layers = {}
        self.blending_modes = ['Normal', 'Add', 'Alpha', 'And', 'Average',
                               'Blue', 'Burn', 'Darken', 'Difference',
                               'Divide', 'Dodge', 'Exclusion', 'Freeze',
                               'Grain extract', 'Grain merge', 'Green',
                               'Hard light', 'Hard mix', 'Hue',
                               'Interpolation', 'Lighten', 'Lightness',
                               'Linear burn', 'Linear light', 'Luminance',
                               'Multiply', 'Negation', 'Or', 'Overlay',
                               'Pin light', 'Red', 'Reflect', 'Saturation',
                               'Shape average', 'Soft burn', 'Soft dodge',
                               'Soft light', 'Screen', 'Stamp', 'Subtract',
                               'Value', 'Vivid light', 'xor']

    def add_layer(self, name=None, media=None, index=None, uid=None):
        if not index: index = len(self.layers)
        if not uid:   uid   = UID()
        if not name:  name  = f'Layer {uid}'

        Layer(self, uid, name, media, index=index)

    def set_layer_media(self, uid, media_type, media_path):
        self.layers[uid].set_media(media_type, media_path)

    def set_layer_blend_mode(self, uid, blend_mode):
        self.layers[uid].set_blend_mode(blend_mode)

    def set_layer_name(self, uid, name):
        self.layers[uid].set_name(name)

    def get_layer_by_name(self, name):
        for layer_uid, layer in self.layers.items():
            if layer.name == name: return layer_uid
        return None

    def delete_layer(self, uid): self.layers[uid].delete()
    def change_layer_name(self, uid, name): self.layers[uid].set_name(name)

