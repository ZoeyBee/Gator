from backend.types.keyframe import Keyframe


class KeyframeManagerMixin:
    def __init__(self, *args, **kwargs):
        super(KeyframeManagerMixin, self).__init__(*args, **kwargs)
        self.keyframes = {}
        self.max_frame = 1

    def add_keyframe(self, frame, uid, attribute_name, value):
        attribute = self.objects[uid].attributes[attribute_name]
        if not attribute.animated and frame > 1: frame = 1
        Keyframe(self, uid, frame, attribute, value, self.objects[uid].keyframes)
        if frame > self.max_frame:
            self.max_frame = frame

    def delete_keyframe(self, frame, uid, attribute_name):
        self.keyframes[frame][uid][attribute_name].delete()

    def get_max_frame(self, animator_uid=None, attribute_name=None):
        if animator_uid is not None:
            return max(list(self.objects[animator_uid].attributes[attribute_name].keyframes))
        elif self.keyframes:
            return max(list(self.keyframes))
        return 1

    def get_keyframes(self):
        for frame, animators in self.keyframes.items():
            for animator_uid, keyframes in animators.items():
                for attribute_name, keyframe in keyframes.items():
                    yield(frame, animator_uid, attribute_name, keyframe)
