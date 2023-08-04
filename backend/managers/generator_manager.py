from backend.types.generators.wave_generator import WaveGenerator
from backend.types.uid import UID


class GeneratorManagerMixin:
    def __init__(self, *args, **kwargs):
        super(GeneratorManagerMixin, self).__init__(*args, **kwargs)
        self.generators = {}

    def add_generator(self, type='Wave', uid=False, index=None):
        if not uid: uid = UID()
        if not index: index = len(self.generators)
        if type == 'Wave': WaveGenerator(self, uid, index)

    def add_generator_connection(self, generator_uid, animator_uid, attribute_name):
        self.generators[generator_uid].connect(self.objects[animator_uid].attributes[attribute_name])

    def delete_generator_connection(self, generator_uid, animator_uid, attribute_name):
        self.generators[generator_uid].disconnect(self.objects[animator_uid].attributes[attribute_name])

    def delete_generator(self, uid):
        self.generators[uid].delete()
