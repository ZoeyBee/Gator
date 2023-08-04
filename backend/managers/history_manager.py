from utils.min_max import min_max

from backend.signal_handlers.history_signal_handler import HistorySignalHandler
from backend.types.history_entry import HistoryEntry


class HistoryManagerMixin:
    def __init__(self, *args, **kwargs):
        super(HistoryManagerMixin, self).__init__(*args, **kwargs)
        self.add_signal_handler(HistorySignalHandler, 'history')
        self.history_entries = []
        self.current_history_entry = 0

    def add_history_entry(self, parent, undo, redo):
        _entry = HistoryEntry(self, undo, redo, parent)
        if self.current_history_entry < len(self.history_entries) - 1:
            for entry in list(self.history_entries[self.current_history_entry+1:]): entry.delete()
        self.current_history_entry = len(self.history_entries) - 1
        return _entry

    def undo(self):
        if not self.history_entries[self.current_history_entry].reversed:
            self.history_entries[self.current_history_entry].reverse()
            self.current_history_entry = min_max(self.current_history_entry - 1, 0, len(self.history_entries) - 1)

    def redo(self):
        self.current_history_entry = min_max(self.current_history_entry + 1, 0, len(self.history_entries) - 1)
        if self.history_entries[self.current_history_entry].reversed:
            self.history_entries[self.current_history_entry].reverse()
