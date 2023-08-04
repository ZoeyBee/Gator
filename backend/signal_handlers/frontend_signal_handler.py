from backend.signal_handlers.base_signal_handler import BaseSignalHandler


class FrontendSignalHandler(BaseSignalHandler):
    def __init__(self, *args, **kwargs):
        super(FrontendSignalHandler, self).__init__(*args, **kwargs)
        self.selected_frame_above_max = True

    def on_layer_blend_mode_changed(self, layer):
        if self.manager.selected_layer == layer.uid:
            self.data.signals.call_signal('selected_layer_blend_mode_changed', layer)

    def on_layer_media_changed(self, layer):
        if self.manager.selected_layer == layer.uid:
            self.data.signals.call_signal('selected_layer_media_changed', layer)

    def on_frame_selected(self, frame):
        if frame >= self.data.max_frame: self.selected_frame_above_max = True
        else:                            self.selected_frame_above_max = False

    def frame_counts_as_selected(self, frame, maximum=None):
        if maximum is None: maximum = self.data.max_frame
        if frame == self.manager.selected_frame:
            return True
        else:
            if self.selected_frame_above_max and frame == maximum:
                return True
        return False

    def on_keyframe_added(self, keyframe):
        if not keyframe.attribute.animated or self.frame_counts_as_selected(keyframe.frame, max(list(keyframe.attribute.keyframes.keys()))):
            self.data.signals.call_signal('selected_keyframe_added', keyframe)

    def on_keyframe_deleted(self, keyframe):
        if not keyframe.attribute.animated or len(keyframe.attribute.keyframes) > 0 and self.frame_counts_as_selected(keyframe.frame, max(list(keyframe.attribute.keyframes.keys()))):
            self.data.signals.call_signal('selected_keyframe_deleted', keyframe)

    def on_preview_rendered(self, preview):
        if preview.layer_uid == self.manager.selected_layer or preview.layer_uid == 'all':
            if self.frame_counts_as_selected(preview.frame):
                self.data.signals.call_signal('selected_preview_rendered', preview)
