from utils.dict_place_or_create import dict_place_or_create


class Keyframe:
    def __init__(self, data, uid, frame, attribute, value, collection, *args, **kwargs):
        self.data = data
        self.uid = uid
        self.frame = frame
        self.value = value
        self.attribute = attribute
        self.collection = collection
        dict_place_or_create(self.data.keyframes, frame, uid, attribute.name, self)
        dict_place_or_create(self.collection, frame, attribute.name, self)
        dict_place_or_create(self.attribute.keyframes, frame, self)
        self.data.signals.call_signal('keyframe_added', self)
        self.deleted = False

    def delete(self):
        if self.deleted: return
        self.deleted = True
        self.data.keyframes[self.frame][self.uid].pop(self.attribute.name)
        if not self.data.keyframes[self.frame][self.uid]:
            self.data.keyframes[self.frame].pop(self.uid)
            if not self.data.keyframes[self.frame]:
                self.data.keyframes.pop(self.frame)
        self.attribute.keyframes.pop(self.frame)
        self.collection[self.frame].pop(self.attribute.name)
        self.data.signals.call_signal('keyframe_deleted', self)

    def __str__(self):
        return f'{self.uid} {self.frame} {self.attribute.name} {self.value}'

    def __repr__(self):
        return self.__str__()
