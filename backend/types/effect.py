from utils.dict_instert_at_index import dict_insert_at_index

from backend.types.base_type import BaseType

from definitions import EFFECTS


class Effect(BaseType):
    def __init__(self, data, uid, effect_id, layer, index=None, *args, **kwargs):
        super(Effect, self).__init__(data, uid, *args, **kwargs)
        self.effect_id = effect_id
        self.layer = layer
        self.index = index
        self.name = effect_id.split('.')[1]
        self.data.effects[uid] = self
        self.attributes = EFFECTS[self.effect_id]['attributes']
        self.keyframes = {}
        self.data.signals.call_signal('effect_added', self)
        self.setup_attributes(self.attributes)
        dict_insert_at_index(self.data.layers[self.layer].effects, self.uid, self, self.index)

    def set_effect_id(self, effect_id):
        old_effect_id = self.effect_id
        self.effect_id = effect_id
        self.name = effect_id.split('.')[1]
        for frame, attribute_name, keyframe in self.get_keyframes(): keyframe.delete()
        for attribute_name, attribute in list(self.attributes.items()): attribute.delete()
        self.attributes = EFFECTS[self.effect_id]['attributes']
        self.setup_attributes(self.attributes)
        self.data.signals.call_signal('effect_id_changed', self)

    def delete(self):
        self.data.effects.pop(self.uid)
        self.data.signals.call_signal('effect_deleted', self)
        if self.layer in self.data.layers: self.data.layers[self.layer].effects.pop(self.uid)
        for frame, attribute_name, keyframe in self.get_keyframes(): keyframe.delete()
        super(Effect, self).delete()

    def __str__(self):
        return self.effect_id
