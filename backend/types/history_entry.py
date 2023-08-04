from definitions import MAX_HISTORY_ENTRIES


class HistoryEntry:
    def __init__(self, data, undo, redo, parent=None):
        self.data = data
        self.undo = undo
        self.redo = redo
        self.children = []
        if parent is None:
            self.data.history_entries.append(self)
            if len(self.data.history_entries) > MAX_HISTORY_ENTRIES: self.data.history_entries[0].delete()
            self.data.current_history_entry += 1
        else:
            parent.children.append(self)
        self.reversed = False

    def reverse(self):
        if self.reversed:
            self.reversed = False
            self.data.signal_handlers['history'].add_ignore(self.redo['ignore'][0], self.redo['ignore'][1],
                                                            {'count': 1, 'type': 'block'})
            self.redo['function'](*self.redo['args'])
        else:
            self.reversed = True
            self.data.signal_handlers['history'].add_ignore(self.undo['ignore'][0], self.undo['ignore'][1],
                                                            {'count': 1, 'type': 'block'})
            self.undo['function'](*self.undo['args'])

        for child in self.children: child.reverse()

    def delete(self):
        self.data.history_entries.remove(self)
