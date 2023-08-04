import json

from backend.types.uid import UID

from utils.dict_place_or_create import dict_place_or_create


class StateManagerMixin:
    def __init__(self, *args, **kwargs):
        super(StateManagerMixin, self).__init__(*args, **kwargs)

    def clear(self):
        for uid, layer in list(self.layers.items()): layer.delete()
        for uid, generator in list(self.generators.items()): generator.delete()

    def save(self, file_path):
        state = {}
        for uid, layer in self.layers.items():
            if layer.media is None: media = layer.media
            else: media = [layer.media.type, layer.media.input_path]
            dict_place_or_create(state, 'layers', uid, {
                'name': layer.name, 'media': media,
                'index': layer.index, 'uid': uid})
        for uid, effect in self.effects.items():
            dict_place_or_create(state, 'effects', uid, {
                'layer': effect.layer, 'effect_id': effect.effect_id,
                'index': effect.index, 'uid': uid})
        for uid, generator in self.generators.items():
            dict_place_or_create(state, 'generators', uid, {
                'type': generator.type, 'uid': uid, 'index': generator.index})
            for attribute_name, attribute in generator.connections.items():
                dict_place_or_create(state, 'generator_connections', uid, {
                    'uid': generator.uid, 'attribute': [attribute_name, attribute.parent.uid]
                })
        for frame, uid, attribute_name, keyframe in self.get_keyframes():
            dict_place_or_create(state, 'keyframes', frame, uid, attribute_name, {
                'frame': frame, 'uid': uid, 'value': keyframe.value})
        state['next_id'] = UID.next_id
        with open(file_path, 'w') as f: f.write(json.dumps(state, separators=(',', ':')))

    def load(self, file_path):
        self.clear()
        with open(file_path, 'r') as f: state = json.loads(f.read())

        for uid, layer in state['layers'].items():
            self.add_layer(layer['name'], None, layer['index'], layer['uid'])
            if layer['media'] is not None: self.set_layer_media(layer['uid'], layer['media'][0], layer['media'][1])
        for uid, effect in state['effects'].items():
            self.add_effect(effect['layer'], effect['effect_id'], effect['index'], effect['uid'])
        for uid, generator in state['generators'].items():
            self.add_generator(generator['type'], generator['uid'], generator['index'])
        for uid, connection in state['generator_connections'].items():
            self.add_generator_connection(connection['uid'], connection['attribute'][1], connection['attribute'][0])
        for frame, animators in state['keyframes'].items():
            for uid, keyframes in animators.items():
                for attribute_name, keyframe in keyframes.items():
                    self.add_keyframe(keyframe['frame'], keyframe['uid'], attribute_name, keyframe['value'])

        UID.next_id = state['next_id']

        self.history_entries = []; self.current_history_entry = 0
