from backend.managers.layer_manager        import LayerManagerMixin
from backend.managers.generator_manager    import GeneratorManagerMixin
from backend.managers.effect_manager       import EffectManagerMixin
from backend.managers.history_manager      import HistoryManagerMixin
from backend.managers.keyframe_manager     import KeyframeManagerMixin
from backend.managers.render_state_manager import RenderStateManagerMixin
from backend.managers.signal_manager       import SignalManagerMixin
from backend.managers.preview_manager      import PreviewManagerMixin
from backend.managers.render_manager       import RenderManagerMixin
from backend.managers.settings_manager     import SettingsManagerMixin
from backend.managers.state_manager        import StateManagerMixin
from backend.managers.playback_manager     import PlaybackManagerMixin
from backend.managers.attribute_manager    import AttributeManagerMixin

from backend.signals import Signals

from utils.rm import rm

from definitions import shared_objects, TMP_DIR


class DataManager(LayerManagerMixin,       EffectManagerMixin,
                  HistoryManagerMixin,     KeyframeManagerMixin,
                  RenderStateManagerMixin, SignalManagerMixin,
                  PreviewManagerMixin,     GeneratorManagerMixin,
                  SettingsManagerMixin,    StateManagerMixin,
                  PlaybackManagerMixin,    RenderManagerMixin,
                  AttributeManagerMixin):
    def __init__(self, *args, **kwargs):
        shared_objects['data_manager'] = self
        self.signals = Signals(self)
        self.objects = {}

        super(DataManager, self).__init__(*args, **kwargs)

    def shutdown(self, *args, **kwargs):
        for preview in self.rendering_previews:
            if preview.renderer: preview.renderer.stop()
        rm(TMP_DIR.as_posix())
