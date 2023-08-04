from backend.signal_handlers.base_signal_handler import BaseSignalHandler
from utils.delay import delay


class RenderStateSignalHandler(BaseSignalHandler):
    def __init__(self, data, *args):
        self.blacklist = ['render_state_added',
                          'render_state_deleted',
                          'selected_keyframe_added',
                          'selected_keyframe_deleted',
                          'preview_added',
                          'preview_deleted',
                          'preview_rendered',
                          'selected_preview_rendered',
                          'preview_video_rendered',
                          'playback_frame_changed',
                          'playback_start_frame_changed',
                          'playback_playing_changed',
                          'history_changed',
                          'layer_renamed',
                          'layer_selected',
                          'frame_selected',
                          'selected_layer_media_changed',
                          'selected_layer_blend_mode_changed',
                          'shutdown', 'clear',
                          'window_changed',
                          'window_size_changed',
                          'generator_added',
        ]
        self.update_block_timer = None
        super(RenderStateSignalHandler, self).__init__(data)

    def update_all_render_states(self):
        self.update_block_timer = None
        self.data.update_all_render_states()

    def on_event(self, *args, **kwargs):
        if self.update_block_timer: self.update_block_timer.cancel()
        self.update_block_timer = delay(self.update_all_render_states, 1)
