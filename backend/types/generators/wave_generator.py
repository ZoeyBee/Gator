from math import sin, pi, modf
from utils.interpolate import interpolate
from utils.sign import sign
from backend.types.generators.base_generator import BaseGenerator

PI2 = pi * 2


class WaveGenerator(BaseGenerator):
    type = 'Wave'
    evaluations = [
        lambda a, t: # Sine
        (a['Amplitude'] * sin(PI2 * a['Frequency'] * t + a['Phase'])) + a['Offset'],
        lambda a, t: # Triangle
        ((((abs(modf(a['Frequency'] * t + a['Phase'] / PI2)[0] - 0.5)) / 0.5) * a['Amplitude'] * 2) - a['Amplitude']) + a['Offset'],
        lambda a, t: # Saw
        (((modf(a['Frequency'] * t + a['Phase'] / PI2)[0]) * (a['Amplitude'] * 2)) - a['Amplitude']) + a['Offset'],
        lambda a, t: # Square
        (a['Amplitude'] * sign(((modf(a['Frequency'] * t + a['Phase'] / PI2)[0]) * (a['Amplitude'] * 2)) - a['Amplitude'])) + a['Offset']]

    def __init__(self, data, uid, index, *args, **kwargs):
        self.attributes.update({'Frequency': {'type': 'float', 'value': 1, 'min': 0.0001, 'max': 24000},
                                'Phase':     {'type': 'float', 'value': 5, 'min': 0,      'max': 10},
                                'Offset':    {'type': 'float', 'value': 0, 'min': -1,     'max': 1},
                                'Wave Type': {'type': 'float', 'value': 0, 'min': 0,      'max': 3}})
        super(WaveGenerator, self).__init__(data, uid, index, *args, **kwargs)

    def evaluate(self, frame=None, attributes=None, t=None):
        if not attributes: attributes = self.get_attribute_values(frame)
        if t is None:      t = frame / self.data.settings.fps
        wave_type = list(map(int, str(attributes['Wave Type']).split('.')))
        wave_1 = self.evaluations[wave_type[0]](attributes, t)
        if len(wave_type) > 1:
            wave_2 = self.evaluations[wave_type[0] + 1](attributes, t)
            blending = attributes['Wave Type'] - wave_type[0]
            return interpolate(wave_1, wave_2, blending)
        else: return wave_1
