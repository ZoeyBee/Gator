from backend.types.effect import Effect
from backend.types.uid import UID


class EffectManagerMixin:
    def __init__(self, *args, **kwargs):
        super(EffectManagerMixin, self).__init__(*args, **kwargs)
        self.effects = {}

    def add_effect(self, layer=None, effect_id=None, index=None, uid=None):
        if effect_id is None: effect_id = 'gmic.Cartoon'
        if index     is None: index     = len(self.layers[layer].effects)
        if uid       is None: uid       = UID()
        Effect(self, uid, effect_id, layer, index)

    def set_effect_id(self, uid, effect_id): self.effects[uid].set_effect_id(effect_id)
    def delete_effect(self, uid): self.effects[uid].delete()
