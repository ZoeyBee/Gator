from utils.dict_instert_at_index import dict_insert_at_index
from utils.min_max import min_max
from backend.types.base_type import BaseType


class BaseGenerator(BaseType):
    attributes = {}

    def __init__(self, data, uid, index, *args, **kwargs):
        super(BaseGenerator, self).__init__(data, uid, *args, **kwargs)
        self.index = index
        self.attributes.update({'Amplitude': {'type': 'float', 'value': 1, 'min': -1, 'max': 1}})
        dict_insert_at_index(self.data.generators, self.uid, self, index)
        self.data.signals.call_signal('generator_added', self)
        self.setup_attributes(self.attributes)
        self.connections = {}

    def evaluate(self, frame, *args, **kwargs): pass

    def get_value(self, frame):
        return min_max(self.evaluate(frame), -1, 1)

    def get_wave(self, frame, samples=16, cycles=1):
        attributes = self.get_attribute_values(frame)
        wave = []; t = 0; cycle = 1 / attributes['Frequency']
        for s in range(samples*cycles):
            wave.append(self.evaluate(None, attributes, t))
            t += cycle / (samples - 1)
        return wave

    def connect(self, attribute):
        attribute.connections[self.uid] = self
        self.connections[attribute.name] = attribute
        self.setup_attribute(f'{attribute.get_id()} Amount', {'type': 'float', 'value': 1, 'min': 0, 'max': 1})
        self.data.signals.call_signal('generator_connection_added', self, attribute)

    def disconnect(self, attribute):
        attribute.connections.pop(self.uid)
        self.connections.pop(attribute.name)
        self.attributes[f'{attribute.get_id()} Amount'].delete()
        self.data.signals.call_signal('generator_connection_deleted', self, attribute)

    def delete(self):
        self.data.generators.pop(self.uid)
        self.data.signals.call_signal('generator_deleted', self)
        super(BaseGenerator, self).delete()
