class SelectionManager:
    def __init__(self):
        super(SelectionManager, self).__init__()
        self.selected_layer = 1
        self.selected_frame = 1

    def select_layer(self, layer_uid):
        self.selected_layer = layer_uid
        self.data.signals.call_signal('layer_selected', self.data.layers[layer_uid])

    def select_frame(self, frame):
        self.selected_frame = frame
        self.data.signals.call_signal('frame_selected', frame)
