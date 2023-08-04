from backend.signal_handlers.preview_signal_handler import PreviewSignalHandler
from backend.types.preview import Preview

from shutil import copyfile
from pathlib import Path

from definitions import PREVIEW_DIR, PREVIEW_VIDEO_DIR


class PreviewManagerMixin():
    def __init__(self, *args, **kwargs):
        super(PreviewManagerMixin, self).__init__(*args, **kwargs)
        self.add_signal_handler(PreviewSignalHandler, 'preview')
        self.previews = {}
        self.preview_video_path = None
        self.rendering_previews = []

    def add_preview(self, frame, layer_uid):
        Preview(self, frame, layer_uid)

    def start_preview_video_render(self):
        video_path = Path(PREVIEW_DIR, 'video.mp4').as_posix()
        for frame, layers in self.previews.items():
            if 'all' not in layers: return
            preview = layers['all']
            copyfile(preview.path.as_posix(), Path(PREVIEW_VIDEO_DIR, f'{preview.frame}.png').as_posix())
        self.make_video(PREVIEW_VIDEO_DIR, video_path, self.end_preview_video_render)

    def end_preview_video_render(self, video_path, *args, **kwargs):
        self.preview_video_path = video_path
        self.signals.call_signal('preview_video_rendered', video_path)

    def get_preview_at_frame(self, frame, layer):
        max_frame = self.get_max_frame()
        if frame > max_frame: frame = max_frame
        try:
            preview = self.previews[frame][layer]
            if preview.rendering: return False
            return preview
        except KeyError:
            return False
