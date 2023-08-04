from subprocess import run, PIPE, Popen
from pathlib import Path
from io import BytesIO
from PIL import Image

from utils.queue import queue
from utils.rm import rm

import os

from definitions import MAX_RENDER_THREADS


class BaseRenderer:
    def __init__(self, *args, **kwargs):
        self.stopped = False
        self.process = None
        self.start(*args, **kwargs)

    def stop(self):
        #todo cancel the thread
        self.stopped = True


class Renderer(BaseRenderer):
    @queue(MAX_RENDER_THREADS)
    def start(self, commands, input_image, callback, callback_args, callback_kwargs):
        if self.stopped: return
        image = input_image
        for command in commands:
            image_bytes = BytesIO(); image.save(image_bytes, format='png')
            self.process = run(command, input=image_bytes.getvalue(), stdout=PIPE, stderr=PIPE)
            image = Image.open(BytesIO(self.process.stdout)).convert('RGBA')
            if self.stopped: return
        callback(image, *callback_args, **callback_kwargs)


class Merger(BaseRenderer):
    @queue(MAX_RENDER_THREADS)
    def start(self, images, callback, callback_args, callback_kwargs):
        if self.stopped: return
        image = BytesIO(); images[0][0].save(image, format='png')
        for _image, blend_mode, opacity in images[1:]:
            if blend_mode == 'Normal': blend_mode = 'alpha'
            layer_image = BytesIO(); _image.save(layer_image, format='png')
            self.process = Popen(['gmic', '-.png', '-.png', '-blend', f'{blend_mode.lower()},{opacity}', 'output', '-.png'],
                                stdout=PIPE, stderr=PIPE, stdin=PIPE)
            if self.stopped: return
            self.process.stdin.write(image.getvalue())
            self.process.stdin.write(layer_image.getvalue())
            image = BytesIO(self.process.communicate()[0])
        image = Image.open(image).convert('RGBA')
        if self.stopped: return
        callback(image, callback_args, callback_kwargs)


class MakeVideo(BaseRenderer):
    @queue(1)
    def start(self, data, images_path, output_path, callback, callback_args, callback_kwargs):
        rm(output_path)
        self.process = run(['ffmpeg', '-framerate', str(data.settings.fps), '-pattern_type', 'glob',
                            '-i', f'{images_path}/*.png', '-pix_fmt', data.settings.ffmpeg_pix_fmt, output_path],
                           stdout=PIPE, stderr=PIPE)
        rm(images_path)
        os.mkdir(images_path)
        callback(output_path, callback_args, callback_kwargs)
