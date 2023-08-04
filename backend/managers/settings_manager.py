from backend.types.settings import Settings


class SettingsManagerMixin:
    def __init__(self, *args, **kwargs):
        self.settings = Settings()
        super(SettingsManagerMixin, self).__init__(*args, **kwargs)
