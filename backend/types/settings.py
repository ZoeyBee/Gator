class Settings:
    def __init__(self, *args, **kwargs):
        self.fps    = 12
        self.width  = 1920
        self.height = 1080
        self.debug  = False
        self.ffmpeg_pix_fmt = 'yuv420p'
        self.preview_render_scale = 4
        self.max_render_threads   = 4
        self.max_history_entries  = 10

        self.font = 'Roboto Mono'

        self.colors = {
            'background_light':   '#31363b',
            'background_dark':    '#232629',
            'background_hover':   '#26292b',
            'background_outline': '#1d1f21',

            'foreground_light': '#eff0f1',
            'foreground_dark':  '#76797C',

            'accent': '#137089',
        }
