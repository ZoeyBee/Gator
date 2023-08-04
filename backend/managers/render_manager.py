from backend.renderer import Renderer, Merger, MakeVideo

from definitions import EFFECTS, EFFECT_COMMANDS


class RenderManagerMixin:
    def __init__(self, *args, **kwargs):
        super(RenderManagerMixin, self).__init__(*args, **kwargs)

    def render(self, frame, layer_uid, scale, callback, *args, **kwargs):
        layer = self.render_states[frame].layers[layer_uid]
        commands = []
        if not 'effects' in layer: callback(layer['input_image']); return
        for effect_uid, effect in layer['effects'].items():
            command = EFFECTS[effect['effect_id']]['command'].format(**effect['attributes']['fake'])
            command = EFFECT_COMMANDS[effect['effect_id'].split('.')[0]]['base'].format(
                width = self.settings.width / scale, height = self.settings.height / scale, command = command)
            commands.append(command.split(' '))
        return Renderer(commands, layer['input_image'], callback, args, kwargs)

    def merge_layers(self, images, callback, *args, **kwargs):
        if len(images) == 1:
            callback(images[0][0], args, kwargs)
            return
        return Merger(images, callback, args, kwargs)

    def make_video(self, images_path, output_path, callback, *args, **kwargs):
        return MakeVideo(self, images_path, output_path, callback, args, kwargs)
