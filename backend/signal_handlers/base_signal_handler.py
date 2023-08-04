class BaseSignalHandler:
    whitelist = None
    blacklist = None

    def __init__(self, data, manager=None):
        super(BaseSignalHandler, self).__init__()
        self.data = data
        self.manager = manager
        for signal in self.data.signals.list_of_signals:
            if self.blacklist and signal     in self.blacklist: continue
            if self.whitelist and signal not in self.whitelist: continue
            if hasattr(self, f'on_{signal}'): self.data.signals.add_listener(signal, eval(f'self.on_{signal}'))
            if hasattr(self, 'on_event'):     self.data.signals.add_listener(signal, self.on_event)
