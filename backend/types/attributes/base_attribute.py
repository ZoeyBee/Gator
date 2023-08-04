from utils.interpolate import interpolate


class BaseAttribute:
    def __init__(self, parent, name, attribute):
        super(BaseAttribute, self).__init__()
        self.parent = parent
        self.name = name
        self.default = attribute['value']
        if not hasattr(self, 'maximum'):
            self.minimum = attribute['min']
            self.maximum = attribute['max']
        self.keyframes = {}
        self.connections = {}
        self.animated = False
        self.interpolation = 'Linear'
        self.attr_type = attribute['type']

    def get_id(self):
        return str(self.parent.uid) + self.name

    def get_value(self, frame, connections=False):
        if not self.animated:         value = self.keyframes[1].value
        elif frame in self.keyframes: value = self.keyframes[frame].value
        elif len(self.keyframes) < 2: value = self.keyframes[1].value
        else:                         value = self.calculate_value(frame)

        if not connections: return self.clean_value(value)
        else:
            generatored_value = value
            for generator_uid, generator in self.connections.items():
                amount = generator.attributes[f'{self.get_id()} Amount'].get_value(frame)
                generatored_value *= generator.get_value(frame) * amount + 1
            return [self.clean_value(value), self.clean_value(generatored_value)]

    def calculate_value(self, frame):
        next_keyframe = max(list(self.keyframes)); last_keyframe = 1
        if frame > next_keyframe: return self.keyframes[next_keyframe].value
        for keyframe in self.keyframes:
            if   keyframe < frame: last_keyframe = keyframe
            elif keyframe > frame: next_keyframe = keyframe; break
        last_value = self.keyframes[last_keyframe].value; next_value = self.keyframes[next_keyframe].value
        if last_value == next_value: return last_value
        frame_distance = frame - last_keyframe
        if self.interpolation == 'Linear':
            if last_value < next_value:
                value_per_frame = (next_value - last_value) / (next_keyframe - last_keyframe)
            elif last_value > next_value:
                value_per_frame = (last_value - next_value) / (next_keyframe - last_keyframe)
                value_per_frame *= -1
            return last_value + (value_per_frame * frame_distance)

    def delete(self):
        for listener in self.parent.attribute_change_listeners: listener(self, 'del')
        if self.name in self.parent.attributes: self.parent.attributes.pop(self.name)
        del self

    def clean_value(self, value):
        if value > self.maximum: return self.maximum
        if value < self.minimum: return self.minimum
        return value
