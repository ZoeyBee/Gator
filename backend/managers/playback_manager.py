from utils.delay import delay
#todo add a signal handler that reacts to fps and keyframe changes

class PlaybackManagerMixin:
    def __init__(self, *args, **kwargs):
        super(PlaybackManagerMixin, self).__init__(*args, **kwargs)
        self.playing = False
        self.timer = None
        self.playback_current_frame = 1
        self.playback_max_frames    = 1
        self.playback_start_frame   = 1
        self.framerate_in_seconds   = 1

    def set_playback_start_frame(self, frame):
        self.playback_start_frame = frame
        self.signals.call_signal('playback_start_frame_changed', self.playback_start_frame)

    def start_playing(self):
        self.playing = True
        self.signals.call_signal('playback_playing_changed', self.playing)
        self.playback_max_frames = self.get_max_frame()
        self.framerate_in_seconds = 1 / self.settings.fps
        self.start_timer()

    def stop_playing(self):
        if self.timer is not None:
            self.timer.cancel()
            self.timer = None
        self.playing = False
        self.signals.call_signal('playback_playing_changed', self.playing)

    def start_timer(self):
        self.timer = delay(self.goto_next_frame, self.framerate_in_seconds)

    def goto_next_frame(self):
        self.playback_current_frame += 1
        if self.playback_current_frame > self.playback_max_frames:
            self.playback_current_frame = self.playback_start_frame
        self.signals.call_signal('playback_frame_changed', self.playback_current_frame)
        self.start_timer()
