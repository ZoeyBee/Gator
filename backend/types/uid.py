class UID(int):
    next_id = 1

    def __new__(self, id=None):
        if id is None: id = UID.next_id; UID.next_id += 1
        return super(UID, self).__new__(self, id)
