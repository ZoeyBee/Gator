from time import sleep
from backend.data_manager import DataManager
from definitions import shared_objects
import os

DataManager()
data = shared_objects['data_manager']

data.settings.debug = True
data.add_layer('test')
data.add_layer('oi')
data.add_effect(data.get_layer_by_name('test'))
data.add_effect(data.get_layer_by_name('oi'))
data.set_layer_media(data.get_layer_by_name('oi'), 'Image', 'tmp_input_image.jpg')
data.set_layer_media(data.get_layer_by_name('test'), 'Image', 'tmp_input_image.jpg')
data.add_generator()
data.add_generator_connection(5, 4, 'Smoothness')
data.generators[5].attributes['Wave Type'].animated = True
data.effects[4].attributes['Smoothness'].animated = True
data.add_keyframe(12, 4, 'Smoothness', 5)
data.add_layer('hey')
data.delete_layer(2)
data.undo()
data.save('test.gator')
data.load('test.gator')
data.start_playing()
sleep((1 / data.settings.fps) * 2)
data.stop_playing()
import pprint; pprint.PrettyPrinter(indent=2).pprint(data.__dict__)
