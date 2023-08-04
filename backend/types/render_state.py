from utils.dict_place_or_create import dict_place_or_create
from backend.types.base_type import BaseType


class RenderState(BaseType):
    def __init__(self, data, frame, *args, **kwargs):
        super(RenderState, self).__init__(data, None, *args, **kwargs)
        self.frame = frame
        self.create_unique_token()
        if frame in self.data.render_states:
            if self.token == self.data.render_states[frame].token: return
            else: self.data.render_states[frame].delete()

        self.layers = {}
        for layer_uid, layer in self.data.layers.items():
            dict_place_or_create(self.layers, layer_uid, 'blend_mode', layer.blend_mode)
            if layer.media: dict_place_or_create(self.layers, layer_uid, 'input_image', layer.media.get_image(frame))
            else:           dict_place_or_create(self.layers, layer_uid, 'input_image', None)
            for attribute_name, attribute in layer.attributes.items():
                dict_place_or_create(self.layers, layer_uid, 'attributes', attribute_name, attribute.get_value(self.frame))
            for effect_uid, effect in layer.effects.items():
                dict_place_or_create(self.layers, layer_uid, 'effects', effect_uid, 'effect_id', effect.effect_id)
                for attribute_name in effect.attributes:
                    value = effect.attributes[attribute_name].get_value(self.frame, connections=True)
                    dict_place_or_create(self.layers, layer_uid, 'effects', effect_uid, 'attributes', 'real', attribute_name, value[0])
                    dict_place_or_create(self.layers, layer_uid, 'effects', effect_uid, 'attributes', 'fake', attribute_name, value[1])

        self.data.render_states[frame] = self
        self.data.signals.call_signal('render_state_added', self)

    def create_unique_token(self):
        self.token = ''
        for __,         layer    in self.data.layers.items():  self.token += f'{layer.media}{layer.blend_mode}'
        for __,         effect   in self.data.effects.items(): self.token += f'{effect.effect_id}'
        for __, __, __, keyframe in self.data.get_keyframes(): self.token += f'{keyframe.value}'

    def delete(self):
        self.data.render_states.pop(self.frame)
        self.data.signals.call_signal('render_state_deleted', self)
