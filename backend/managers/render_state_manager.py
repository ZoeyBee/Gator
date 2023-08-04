from backend.types.render_state import RenderState
from backend.signal_handlers.render_state_signal_handler import RenderStateSignalHandler


class RenderStateManagerMixin():
    def __init__(self, *args, **kwargs):
        super(RenderStateManagerMixin, self).__init__(*args, **kwargs)
        self.add_signal_handler(RenderStateSignalHandler, 'render_state')
        self.render_states = {}

    def add_render_state(self, frame):
        RenderState(self, frame)

    def delete_render_state(self, frame):
        self.render_states[frame].delete()

    def update_all_render_states(self):
        for frame in range(self.get_max_frame()):
            frame += 1
            self.add_render_state(frame)
