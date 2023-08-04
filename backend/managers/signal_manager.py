class SignalManagerMixin:
    def __init__(self):
        self.signal_handlers = {}
        super(SignalManagerMixin, self).__init__()

    def add_signal_handler(self, handler, name, manager=None):
        self.signal_handlers[name] = handler(self, manager)
