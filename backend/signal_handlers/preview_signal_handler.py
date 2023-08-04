from backend.signal_handlers.base_signal_handler import BaseSignalHandler
from utils.delay import delay


class PreviewSignalHandler(BaseSignalHandler):
    def __init__(self, data, *args):
        super(PreviewSignalHandler, self).__init__(data)

    def on_render_state_added(self, render_state, *args, **kwargs):
        for layer_uid in list(self.data.layers):
            self.data.add_preview(render_state.frame, layer_uid)

    def on_render_state_deleted(self, render_state, *args, **kwargs):
        if render_state.frame in self.data.previews:
            for __, preview in list(self.data.previews[render_state.frame].items()):
                preview.delete()

    def on_preview_rendered(self, preview):
        if not preview.frame in self.data.previews: return
        for layer_uid, _preview in self.data.previews[preview.frame].items():
            if layer_uid != 'all' and _preview.rendering: return
        if preview.layer_uid == 'all':
            if len(self.data.rendering_previews) == 0: self.data.start_preview_video_render()
            return
        self.data.add_preview(preview.frame, 'all')
