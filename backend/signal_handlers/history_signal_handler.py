from utils.dict_place_or_create import dict_place_or_create

from backend.signal_handlers.base_signal_handler import BaseSignalHandler


class HistorySignalHandler(BaseSignalHandler):
    def __init__(self, data, *args):
        super(HistorySignalHandler, self).__init__(data)
        self.ignores = {}

    def catch_ignores(signal_function, *args, **kwargs):
        def aux(self, obj, *xs, **kws):
            signal_name = signal_function.__name__
            if signal_name in self.ignores:
                if obj.uid in self.ignores[signal_name]:
                    ignore = self.ignores[signal_name][obj.uid]; ignore['count'] -= 1
                    if ignore['count'] < 1:
                        self.ignores[signal_name].pop(obj.uid)
                        if not self.ignores[signal_name]: self.ignores.pop(signal_name)
                    if ignore['type'] == 'block': return
                    return signal_function(self, obj, *args, parent=ignore['parent'], **kwargs)
            return signal_function(self, obj, *args, **kwargs)
        return aux

    def add_ignore(self, signal, obj, ignore):
        if signal in self.ignores and obj in self.ignores[signal]:
            self.ignores[signal][obj]['count'] += 1
        else:
            dict_place_or_create(self.ignores, signal, obj, ignore)

    @catch_ignores
    def on_layer_added(self, layer, *args, parent=None, **kwargs):
        entry = self.data.add_history_entry(parent,
                                            {'function': self.data.delete_layer,
                                             'args': [layer.uid],
                                             'ignore': ['on_layer_deleted', layer.uid]},
                                            {'function': self.data.add_layer,
                                             'args': [layer.name, layer.media, layer.index, layer.uid],
                                             'ignore': ['on_layer_added', layer.uid]})
        for attribute_name in layer.attributes:
            self.add_ignore('on_keyframe_added', layer.uid, {'count': 1, 'type': 'merge', 'parent': entry})

    @catch_ignores
    def on_layer_deleted(self, layer, *args, parent=None, **kwargs):
        entry = self.data.add_history_entry(parent,
                                            {'function': self.data.add_layer,
                                             'args': [layer.name, layer.media, layer.index, layer.uid],
                                             'ignore': ['on_layer_added', layer.uid]},
                                            {'function': self.data.delete_layer,
                                             'args': [layer.uid],
                                             'ignore': ['on_layer_deleted', layer.uid]})
        for effect_uid in layer.effects:
            self.add_ignore('on_effect_deleted', effect_uid, {'count': 1, 'type': 'merge', 'parent': entry})
        for frame, attribute_name, keyframe in layer.get_keyframes():
            self.add_ignore('on_keyframe_deleted', keyframe.uid, {'count': 1, 'type': 'merge', 'parent': entry})

    @catch_ignores
    def on_effect_added(self, effect, *args, parent=None, **kwargs):
        entry = self.data.add_history_entry(parent,
                                            {'function': self.data.delete_effect,
                                             'args': [effect.uid],
                                             'ignore': ['on_effect_deleted', effect.uid]},
                                            {'function': self.data.add_effect,
                                             'args': [effect.layer, effect.effect_id, effect.index, effect.uid],
                                             'ignore': ['on_effect_added', effect.uid]})
        for attribute_name in effect.attributes:
            self.add_ignore('on_keyframe_added', effect.uid, {'count': 1, 'type': 'merge', 'parent': entry})

    @catch_ignores
    def on_effect_deleted(self, effect, *args, parent=None, **kwargs):
        entry = self.data.add_history_entry(parent,
                                            {'function': self.data.add_effect,
                                             'args': [effect.layer, effect.effect_id, effect.index, effect.uid],
                                             'ignore': ['on_effect_added', effect.uid]},
                                            {'function': self.data.delete_effect,
                                             'args': [effect.uid],
                                             'ignore': ['on_effect_deleted', effect.uid]})
        for frame, attribute_name, keyframe in effect.get_keyframes():
            self.add_ignore('on_keyframe_deleted', keyframe.uid, {'count': 1, 'type': 'merge', 'parent': entry})

    @catch_ignores
    def on_generator_added(self, generator, *args, parent=None, **kwargs):
        entry = self.data.add_history_entry(parent,
                                            {'function': self.data.delete_generator,
                                             'args': [generator.uid],
                                             'ignore': ['on_generator_deleted', generator.uid]},
                                            {'function': self.data.add_generator,
                                             'args': [generator.type, generator.uid, generator.index],
                                             'ignore': ['on_generator_added', generator.uid]})
        for attribute_name in generator.attributes:
            self.add_ignore('on_keyframe_added', generator.uid, {'count': 1, 'type': 'merge', 'parent': entry})

    @catch_ignores
    def on_generator_deleted(self, generator, *args, parent=None, **kwargs):
        entry = self.data.add_history_entry(parent,
                                            {'function': self.data.add_generator,
                                             'args': [generator.type, generator.uid, generator.index],
                                             'ignore': ['on_generator_added', generator.uid]},
                                            {'function': self.data.delete_generator,
                                             'args': [generator.uid],
                                             'ignore': ['on_generator_deleted', generator.uid]})
        for frame, attribute_name, keyframe in generator.get_keyframes():
            self.add_ignore('on_keyframe_deleted', keyframe.uid, {'count': 1, 'type': 'merge', 'parent': entry})

    @catch_ignores
    def on_keyframe_added(self, keyframe, *args, parent=None, **kwargs):
        entry = self.data.add_history_entry(parent,
                                            {'function': self.data.delete_keyframe,
                                             'args': [keyframe.frame, keyframe.uid, keyframe.attribute.name],
                                             'ignore': ['on_keyframe_deleted', keyframe.uid]},
                                            {'function': self.data.add_keyframe,
                                             'args': [keyframe.frame, keyframe.uid, keyframe.attribute.name, keyframe.value],
                                             'ignore': ['on_keyframe_added', keyframe.uid]})

    @catch_ignores
    def on_keyframe_deleted(self, keyframe, *args, parent=None, **kwargs):
        entry = self.data.add_history_entry(parent,
                                            {'function': self.data.add_keyframe,
                                             'args': [keyframe.frame, keyframe.uid, keyframe.attribute.name, keyframe.value],
                                             'ignore': ['on_keyframe_added', keyframe.uid]},
                                            {'function': self.data.delete_keyframe,
                                             'args': [keyframe.frame, keyframe.uid, keyframe.attribute.name],
                                             'ignore': ['on_keyframe_deleted', keyframe.uid]})
