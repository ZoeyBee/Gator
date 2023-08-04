class Signals:
    signals = {}

    def __init__(self, data):
        self.data = data
        for signal in Signals.list_of_signals:
            self.signals[signal] = {'listeners': []}

    def call_signal(self, signal_name, *args, **kwargs):
        for callback in self.signals[signal_name]['listeners']: callback(*args, **kwargs)
        if self.data.settings.debug: print('|', signal_name, args, kwargs)

    def add_listener(self, signal_name, callback):
        self.signals[signal_name]['listeners'].append(callback)

    def remove_listener(self, signal_name, callback):
        self.signals[signal_name]['listeners'].remove(callback)

    list_of_signals = [
                 'layer_added',                       'layer_deleted',
                 'layer_name_changed',                'layer_media_changed',
                 'layer_blend_mode_changed', 'selected_layer_media_changed',
        'selected_layer_blend_mode_changed',

        'effect_added', 'effect_deleted', 'effect_id_changed',

                 'keyframe_added',          'keyframe_deleted',
        'selected_keyframe_added', 'selected_keyframe_deleted',

        'render_state_added',
        'render_state_deleted',

                 'preview_added',    'preview_deleted',
                 'preview_rendered', 'preview_video_rendered',
        'selected_preview_rendered',

        'generator_added',            'generator_deleted',
        'generator_connection_added', 'generator_connection_deleted',

        'attribute_animated_changed',

        'playback_playing_changed',
        'playback_frame_changed',
        'playback_start_frame_changed',

        'layer_selected', 'frame_selected',
    ]
